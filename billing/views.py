from django.shortcuts import render
from django.views.generic import TemplateView
import stripe
import os
from django.http import HttpResponse, JsonResponse
from .models import *
from datetime import datetime, timedelta
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.db import transaction
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv, find_dotenv
import json
from master.views import authenticate_user
from master.views import decrypt_message
from adminapp.constants import *

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

class AccountOwnerDashboard(TemplateView):
    template_name = "account_owner_dash.html"

    def get(self,request, *args, **kwargs):
        context = {}
        user_id = request.GET['id']
        try:
            encoded_token = request.GET['token']
            decrypted_token = decrypt_message(encoded_token)
            status_code = authenticate_user(decrypted_token)
            if status_code != 200:
                return HttpResponse("Unauthorized", status = 401)
        except:
            return HttpResponse("Unauthorized", status = 401)
        try:
            session_id = request.GET['session_id']
            print(session_id)
            checkout_session = stripe.checkout.Session.retrieve(session_id)
            subscription_info = stripe.Subscription.retrieve(checkout_session.subscription)
            if Subscription.objects.filter(customerId = subscription_info['customer'], stripeStatus = 'active').exists():
                pass
            elif Subscription.objects.filter(customerId = subscription_info['customer'], stripeStatus = 'canceled').exists():
                pass
            else:
                with transaction.atomic():
                    subs = Subscription.objects.filter(userId=User.objects.get(zendeskUserid=user_id),stripeStatus='active')
                    if subs.exists():
                        for i in subs:
                            i.stripeStatus = 'inactive'
                            i.save()
                            try:
                                stripe.Subscription.delete(i.stripeSubscriptionId)
                                # stripe.Subscription.cancel(i.stripeSubscriptionId)
                            except:
                                pass
                    if Plan.objects.get(PlanKey=subscription_info['plan']['id']).interval == 'month':
                        interval = timedelta(days=30)
                    else:
                        interval = relativedelta(years=1)
                    Subscription.objects.create(
                        userId = User.objects.get(zendeskUserid = user_id),
                        stripeSubscriptionId = subscription_info['id'],
                        stripeStatus = subscription_info['status'],
                        customerId = subscription_info['customer'],
                        productId = subscription_info['plan']['product'],
                        priceId = subscription_info['plan']['id'],
                        trialEndsAt = datetime.fromtimestamp(subscription_info['start_date'])+timedelta(days=trial_period_days),
                        subscriptionStartsAt = datetime.fromtimestamp(subscription_info['start_date']),
                        subscriptionEndsAt =  datetime.fromtimestamp(subscription_info['start_date'])+ interval,
                        invoiceId = subscription_info['latest_invoice'],
                    )
        except:
            pass
        return render(request, self.template_name, context)
    

class AccountOwnerInfo(TemplateView):
    template_name = "account_owner_dash.html"

    def get(self,request, *args, **kwargs):
        context = {}
        try:
            encoded_token = request.headers['Authorization'].split(' ')[1]
            decrypted_token = decrypt_message(encoded_token)
            status_code = authenticate_user(decrypted_token)
            if status_code != 200:
                return HttpResponse("Unauthorized", status = 401)
        except:
            return HttpResponse("Unauthorized", status = 401)
        try:
            user_id = request.GET['user_id']
            org_id = User.objects.get(zendeskUserid=user_id).zendeskOrganizationId
            context.update({'user_email':User.objects.get(zendeskUserid=user_id).email})
        except:
            context.update({'error':'Something went wrong,  Kindly close this tab, refresh your Zendesk account, and return here.'})
            return JsonResponse({'context':context})
        try:
            subscription_list = stripe.Subscription.list(limit=10)
            context.update({'subscription_list':subscription_list})
        except:
            context.update({'subscription_list':''})
        if Subscription.objects.filter(userId__in=User.objects.filter(role="admin" ,zendeskOrganizationId=org_id)).exists():
            subs_obj = Subscription.objects.filter(userId__in=User.objects.filter(role="admin",zendeskOrganizationId=org_id)).last()
            plan = Plan.objects.get(PlanKey=subs_obj.priceId)
            if subs_obj.stripeStatus == 'active':
                stripe_status = 'active'
                plan = plan.title +' ('+ plan.interval + 'ly)'
            elif subs_obj.stripeStatus == 'canceled':
                stripe_status = 'canceled'
                if date.today() > subs_obj.subscriptionEndsAt.date():
                    plan = 'No Active Plan'
                else:
                    plan =plan.title +' ('+ plan.interval + 'ly)'
            elif subs_obj.stripeStatus == 'inactive':
                stripe_status = 'inactive'
                plan = 'No Active Plan'
            else:
                stripe_status='no_plan'
                plan = 'No Active Plan'
            context.update({'subscription': stripe_status,'active_plan':plan})
        else:
            context.update({'subscription': 'No Plan','active_plan':'No Plan'})
        return JsonResponse({'context':context})
    

#No use of this class
class CheckOutSession(TemplateView):

    def get(self,request, *args, **kwargs):
        status_code = authenticate_user(request.headers['Authorization'].split(' ')[1])
        if status_code != 200:
             return HttpResponse("Unauthorized", status = 401)
        id = request.args.get('sessionId')
        checkout_session = stripe.checkout.Session.retrieve(id)
        return JsonResponse(checkout_session)


class CreateCheckOutSession(TemplateView):

    def post(self,request, *args, **kwargs):
        try:
            encoded_token = request.headers['Authorization'].split(' ')[1]
            decrypted_token = decrypt_message(encoded_token)
            status_code = authenticate_user(decrypted_token)
            if status_code != 200:
                 return HttpResponse("Unauthorized", status = 401)
        except:
            return HttpResponse("Unauthorized", status=401)
        data = json.loads(request.body.decode())
        price = Plan.objects.get(title=data['pricePlan'],interval=data['interval']).PlanKey
        user_id=request.GET['user_id']
        #domain_url = 'http://127.0.0.1:8000'
        domain_url = 'https://word-wand.creativebuffer.com'

        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url+'/billing/accoun_owner?id='+user_id+'&session_id={CHECKOUT_SESSION_ID}&token='+encoded_token,
                mode='subscription',
                line_items=[{
                    'price': price,
                    'quantity': 1
                }],
            )
            return JsonResponse({"checkout_session":checkout_session.url})
        except Exception as e:
            return JsonResponse({'error': {'message': str(e)}})


class Invoices(BaseDatatableView):
    order_columns = ['subsId','stripeStatus',"subscriptionStartsAt","subscriptionEndsAt","invoiceId"]

    def get_initial_queryset(self):
        # encoded_token = decrypt_message(self.request.headers['Authorization'].split(' ')[1])
        # status_code = authenticate_user(encoded_token)
        # if status_code != 200:
        #      return HttpResponse("Unauthorized", status = 401)
        user_id = self.request.GET['user_id']
        org_id = User.objects.get(zendeskUserid =user_id).zendeskOrganizationId
        subscription = Subscription.objects.filter(userId__in=User.objects.filter(zendeskOrganizationId =org_id, role="admin")).values()
        return subscription

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = Subscription.objects.filter(Q(subscriptionStartsAt__icontains=search)|Q(subscriptionEndsAt__icontains=search)|Q(stripeStatus__icontains=search)).values()
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                "invoice_id":item['invoiceId'],
                "plan_name":Plan.objects.get(PlanKey=item['priceId']).title,
                "status":item['stripeStatus'],
                "start_date": item['subscriptionStartsAt'].date(),
                "end_date": item['subscriptionEndsAt'].date(),
            })
        return json_data
    

class CancelPlan(TemplateView):
   
    def get(request, self, *args,**kwargs):
        try:
            encoded_token = request.request.headers['Authorization'].split(' ')[1]
            decrypted_token = decrypt_message(encoded_token)
            status_code = authenticate_user(decrypted_token)
            if status_code != 200:
                return HttpResponse("Unauthorized", status = 401)
        except:
            return HttpResponse("Unauthorized", status=401)
        user_id = request.request.GET['user_id']
        user = User.objects.get(zendeskUserid=user_id).zendeskOrganizationId
        try:
            subs = Subscription.objects.filter(userId__in = User.objects.filter(role='admin',zendeskOrganizationId=user)).last()
            subs.stripeStatus = 'canceled'
            subs.save()
            stripe.Subscription.modify(subs.stripeSubscriptionId, cancel_at_period_end=True)
            # stripe.Subscription.cancel(subs.stripeSubscriptionId)
            return JsonResponse({'success':True})
        except:
            return JsonResponse({'success':False})


class GetInvoiceDetail(TemplateView):

    def get(request, self, *args,**kwargs):
        try:
            encoded_token = request.request.headers['Authorization'].split(' ')[1]
            decrypted_token = decrypt_message(encoded_token)
            status_code = authenticate_user(decrypted_token)
            if status_code != 200:
                return HttpResponse("Unauthorized", status = 401)
        except:
            return HttpResponse("Unauthorized", status=401)
        invoice_id = request.request.GET['invoice_id']
        pdf_url = stripe.Invoice.retrieve(invoice_id)['invoice_pdf']
        return JsonResponse({'pdf_url':pdf_url})


class UpdateSubscription(TemplateView):
    template_name = "login.html"

    def post(request, self, *args,**kwargs):
        webhook_cust=''
        webhook_data = json.loads(request.request.body.decode())
        webhook_type = webhook_data['type']
        if webhook_type == 'invoice.paid':
            webhook_cust = webhook_data['data']['object']['customer']
            print(webhook_cust)
            if webhook_cust:
                subs_obj = Subscription.objects.filter(customerId = webhook_cust).exclude(stripeStatus = 'canceled')
                print(subs_obj)
                if subs_obj.exists():
                    sub_obj = subs_obj.last()
                    interval = Plan.objects.get(PlanKey = sub_obj.priceId).interval
                    print(interval)
                    print(sub_obj.subscriptionStartsAt.date())
                    print(date.today())
                    if sub_obj.subscriptionStartsAt.date() != date.today():
                        print(sub_obj)
                        print(sub_obj.subscriptionEndsAt)
                        if interval == 'month':
                            print(sub_obj.subscriptionEndsAt +timedelta(days=30))
                            sub_obj.subscriptionEndsAt = sub_obj.subscriptionEndsAt + timedelta(days=30)
                        else:
                            print(sub_obj.subscriptionEndsAt +timedelta(days=365))
                            sub_obj.subscriptionEndsAt = sub_obj.subscriptionEndsAt + timedelta(days=365)
                        sub_obj.renewPlanDate = datetime.now()
                        sub_obj.save() #Save do not works properly need to do R&d in this
        print('invoice.paid')
        return JsonResponse({'success': 'success'})


