from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
import json
from .models import User,HitCount
from django.db import transaction
import openai
from django.http import Http404
from django.db.models import Count
from django.db.models.functions import TruncDate
from master.models import *
import http.client
import os
from dotenv import load_dotenv, find_dotenv
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from billing.models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from jose import jwt
from datetime import datetime, timedelta
from .constants import *
from master.views import authenticate_user, encrypt_message, decrypt_message

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

conn = http.client.HTTPSConnection("api.openai.com")
openai.api_key = os.getenv('CHAT_GPT_KEY')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# Create your views here.



class Login(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    

def logout_view(request):
    logout(request)
    return render(request,'login.html')
    

class AddUser(TemplateView):

    def get(self, request, *args, **kwargs):
        projects_name = User.objects.filter().values()
        return HttpResponse(json.dumps(list(projects_name)), 'application/json')
    
    def post(self, request, *args, **kwargs):
        projects_name = HitCount.objects.filter(isDeleted=False).values('name')
        return HttpResponse(json.dumps(list(projects_name)), 'application/json')
    

class APIhitCount(TemplateView):

    def get(self, request, *args, **kwargs):
        projects_name = HitCount.objects.filter().values('name')
        return HttpResponse(json.dumps(list(projects_name)), 'application/json')
    
    def post(self, request, *args, **kwargs):
        projects_name = HitCount.objects.filter(isDeleted=False).values('name')
        return HttpResponse(json.dumps(list(projects_name)), 'application/json')


class GetResponse(TemplateView):

    def post(self,request, *args, **kwargs):
        status_code = authenticate_user(request.headers['Authorization'].split(' ')[1])
        print("Response",request.headers['Authorization'].split(' ')[1])
        if status_code != 200:
             return HttpResponse("Unauthorized", status = 401)
        role = request.POST['role']
        sentiment = request.POST['sentiment']
        tone = request.POST['tone']
        prompt_txt = request.POST['prompt_txt']
        organization_id= request.POST['organization_id']
        email = request.POST['email']
        users = User.objects.filter(zendeskOrganizationId=organization_id)
        admin_user = users.filter(role='admin')
        subs_obj = Subscription.objects.filter(userId__in=admin_user)
        prompt_txt = "Rewrite the following text as a "+role +" talking to a " + sentiment +" customer in a "+tone+" tone : "+prompt_txt
        if subs_obj.exists():
            if subs_obj.last().stripeStatus == 'active' or subs_obj.last().stripeStatus == 'canceled':
                pricingkey = subs_obj.last().priceId
                rewords = Plan.objects.get(PlanKey =pricingkey).noOfRewordsPerDay
                if (HitCount.objects.filter(user__in=users, hitTime__date=datetime.today().date()).count()) < rewords:
                    return HttpResponse(GPTResponse(prompt_txt))
                else:
                    return HttpResponse(messages['ExceedLimit'])
            else:
                return HttpResponse(messages['InActiveUsers'])
        else:
            if (date.today() - admin_user.first().createdOnUtc.date()).days > trial_period_days:
                return HttpResponse(messages['InActiveUsers'])
            else:
                return HttpResponse(GPTResponse(prompt_txt))

            
            

class GetYesResponse(TemplateView):

    def post(self,request, *args, **kwargs):
        print("1",request)
        status_code = authenticate_user(request.headers['Authorization'].split(' ')[1])
        print("2",request.headers['Authorization'].split(' ')[1])
        if status_code != 200:
            print("3","401")
            return HttpResponse("Unauthorized", status = 401)
        print("5")
        txt = request.POST['prompt_txt']
        print("request::",request)
        print("6",txt)
        organization_id= request.POST['organization_id']
        print("7",organization_id)
        email = request.POST['email']
        print(email)
        try:
            phase2 = request.POST['phase2']
        except:
            phase2 = None
        users = User.objects.filter(zendeskOrganizationId=organization_id)
        print("8",users)
        admin_user = users.filter(role='admin')
        print("9",admin_user)
        subs_obj = Subscription.objects.filter(userId__in=admin_user)
        print("10",subs_obj)
        if RoleSentimentToneMapping.objects.filter(zendeskOrganizationId = organization_id, isDefault=True,isDeleted=False).exists():
            mapping_obj = RoleSentimentToneMapping.objects.filter(zendeskOrganizationId = organization_id, isDefault=True,isDeleted=False).last()
            language = mapping_obj.language.replylanguageAPI
            yni_tone = mapping_obj.yni_tone.yniToneAPI
        else:
            language = 'American English'
            yni_tone = 'Polite'
        prompt_txt = 'Create a {} response to the following so the customer knows the answer to their question is a Yes. Write in {} language. "{}"'.format(yni_tone,language, txt)
        if phase2 == None:
            prompt_txt = 'Create a polite response to the following so the customer knows the answer to their question is a Yes "{}"'.format(txt)
        print("11",prompt_txt)
        print("12")
        if subs_obj.exists():
            print("13")
            if subs_obj.last().stripeStatus == 'active' or subs_obj.last().stripeStatus == 'canceled':
                print("14")
                pricingkey = subs_obj.last().priceId
                print("15",pricingkey)
                rewords = Plan.objects.get(PlanKey =pricingkey).noOfRewordsPerDay
                print("16",rewords)
                if (HitCount.objects.filter(user__in=users, hitTime__date=datetime.today().date()).count()) < rewords:
                    print("17")
                    response = GPTResponse(prompt_txt)
                    print("18",response)
                    return HttpResponse(response.replace('\n\n','<p><br data-cke-filler="true"></p>').replace('\n','<p><br data-cke-filler="true"></p>'))
                else:
                    print("19",messages['ExceedLimit'])
                    return HttpResponse(messages['ExceedLimit'])
            else:
                print("20",messages['InActiveUsers'])
                return HttpResponse(messages['InActiveUsers'])
        else:
            print("21")
            if (date.today() - admin_user.first().createdOnUtc.date()).days > trial_period_days:
                print("22")
                return HttpResponse(messages['InActiveUsers'])
            else:
                print("23")
                response = GPTResponse(prompt_txt)
                return HttpResponse(response.replace('\n\n','<p><br data-cke-filler="true"></p>').replace('\n','<p><br data-cke-filler="true"></p>'))
            
    
class GetNoResponse(TemplateView):

    def post(self,request, *args, **kwargs):
        status_code = authenticate_user(request.headers['Authorization'].split(' ')[1])
        print("No Response",request.headers['Authorization'].split(' ')[1])
        if status_code != 200:
             return HttpResponse("Unauthorized", status = 401)
        txt = request.POST['prompt_txt']
        organization_id= request.POST['organization_id']
        email = request.POST['email']
        try:
            phase2 = request.POST['phase2']
        except:
            phase2 = None
        users = User.objects.filter(zendeskOrganizationId=organization_id)
        admin_user =users.filter(role='admin')
        subs_obj = Subscription.objects.filter(userId__in=admin_user)
        if RoleSentimentToneMapping.objects.filter(zendeskOrganizationId = organization_id, isDefault=True,isDeleted=False).exists():
            mapping_obj = RoleSentimentToneMapping.objects.filter(zendeskOrganizationId = organization_id, isDefault=True,isDeleted=False).last()
            language = mapping_obj.language.replylanguageAPI
            yni_tone = mapping_obj.yni_tone.yniToneAPI
        else:
            language = 'American English'
            yni_tone = 'Polite'
        prompt_txt = 'Create a {} response to the following so the customer knows the answer to their question is a No. Write in {} language."{}"'.format(yni_tone,language,txt)
        if phase2 == None:
            prompt_txt = 'Create a polite response to the following so the customer knows the answer to their question is a No"{}"'.format(txt)
        if subs_obj.exists():
            if subs_obj.last().stripeStatus == 'active' or subs_obj.last().stripeStatus == 'canceled':
                pricingkey = subs_obj.last().priceId
                rewords =Plan.objects.get(PlanKey =pricingkey).noOfRewordsPerDay
                if (HitCount.objects.filter(user__in=users, hitTime__date=datetime.today().date()).count()) < rewords:
                    response = GPTResponse(prompt_txt)
                    return HttpResponse(response.replace('\n\n','<p><br data-cke-filler="true"></p>').replace('\n','<p><br data-cke-filler="true"></p>'))
                else:
                    return HttpResponse(messages['ExceedLimit'])
            else:
                return HttpResponse(messages['InActiveUsers'])
        else:
            if (date.today() - admin_user.first().createdOnUtc.date()).days > trial_period_days:
                return HttpResponse(messages['InActiveUsers'])
            else:
                response = GPTResponse(prompt_txt)
                return HttpResponse(response.replace('\n\n','<p><br data-cke-filler="true"></p>').replace('\n','<p><br data-cke-filler="true"></p>'))
            
            

class GetInstructResponse(TemplateView):

    def post(self,request, *args, **kwargs):
        status_code = authenticate_user(request.headers['Authorization'].split(' ')[1])
        print("Instruct",request.headers['Authorization'].split(' ')[1])
        if status_code != 200:
             return HttpResponse("Unauthorized", status = 401)
        txt = request.POST['prompt_txt']
        agent_response = request.POST['agent_response']
        organization_id= request.POST['organization_id']
        email = request.POST['email']
        try:
            phase2 = request.POST['phase2']
        except:
            phase2 = None
        users = User.objects.filter(zendeskOrganizationId=organization_id)
        admin_user =users.filter(role='admin')
        if RoleSentimentToneMapping.objects.filter(zendeskOrganizationId = organization_id, isDefault=True,isDeleted=False).exists():
            mapping_obj = RoleSentimentToneMapping.objects.filter(zendeskOrganizationId = organization_id, isDefault=True,isDeleted=False).last()
            language = mapping_obj.language.replylanguageAPI
            yni_tone = mapping_obj.yni_tone.yniToneAPI
            is_language_ignored = mapping_obj.isLanguageIgnoredForInstruct
            is_yni_tone_ignored = mapping_obj.isYniToneIgnoredForInstruct
        else:
            language = 'American English'
            yni_tone = 'Polite'
            is_language_ignored = False
            is_yni_tone_ignored = False
        subs_obj = Subscription.objects.filter(userId__in=admin_user)
        if is_language_ignored and is_yni_tone_ignored:
            prompt_txt = 'Create a polite response to the following "{}" and incorporate the following "{}"'.format(txt,agent_response)
        elif is_language_ignored == True and is_yni_tone_ignored == False:
            prompt_txt = 'Create a {} response to the following "{}" and incorporate the following "{}"'.format(yni_tone,txt,agent_response)
        elif is_language_ignored == False and is_yni_tone_ignored == True:
            prompt_txt = 'Create a polite response to the following "{}" and incorporate the following "{}". Write in {} language.'.format(txt,agent_response, language)
        else:
            prompt_txt = 'Create a {} response to the following "{}" and incorporate the following "{}". Write in {} language.'.format(yni_tone,txt,agent_response, language)
        if phase2 == None:
            prompt_txt='Create a polite response to the following "{}" and incorporate the following "{}"'.format(txt,agent_response)
        if subs_obj.exists():
            if subs_obj.last().stripeStatus == 'active' or subs_obj.last().stripeStatus == 'canceled':
                pricingkey = subs_obj.last().priceId
                rewords =Plan.objects.get(PlanKey =pricingkey).noOfRewordsPerDay
                if (HitCount.objects.filter(user__in=users, hitTime__date=datetime.today().date()).count()) < rewords:
                    response = GPTResponse(prompt_txt)
                    return HttpResponse(response.replace('\n\n','<p><br data-cke-filler="true"></p>').replace('\n','<p><br data-cke-filler="true"></p>'))
                else:
                    return HttpResponse(messages['ExceedLimit'])
            else:
                return HttpResponse(messages['InActiveUsers'])
        else:
            if (date.today() - admin_user.first().createdOnUtc.date()).days > trial_period_days:
                return HttpResponse(messages['InActiveUsers'])
            else:
                response = GPTResponse(prompt_txt)
                return HttpResponse(response.replace('\n\n','<p><br data-cke-filler="true"></p>').replace('\n','<p><br data-cke-filler="true"></p>'))

class GetMoreInfoResponse(TemplateView):

    def post(self,request, *args, **kwargs):
        status_code = authenticate_user(request.headers['Authorization'].split(' ')[1])
        print("more response",request.headers['Authorization'].split(' ')[1])
        if status_code != 200:
             return HttpResponse("Unauthorized", status = 401)
        txt = request.POST['prompt_txt']
        organization_id= request.POST['organization_id']
        email = request.POST['email']
        try:
            phase2 = request.POST['phase2']
        except:
            phase2 = None
        users = User.objects.filter(zendeskOrganizationId=organization_id)
        admin_user =users.filter(role='admin')
        if RoleSentimentToneMapping.objects.filter(zendeskOrganizationId = organization_id, isDefault=True,isDeleted=False).exists():
            mapping_obj = RoleSentimentToneMapping.objects.filter(zendeskOrganizationId = organization_id, isDefault=True,isDeleted=False).last()
            language = mapping_obj.language.replylanguageAPI
        else:
            language = 'American English'
        subs_obj = Subscription.objects.filter(userId__in=admin_user)
        prompt_txt = 'Respond to the following to gather more information and create a list of five questions to ask based on the following message. Write in {} language. "{}"'.format(language, txt)
        if phase2 == None:
            prompt_txt = 'Respond to the following to gather more information and create a list of five questions to ask based on the following message. "{}"'.format(txt)     
        if subs_obj.exists():
            if subs_obj.last().stripeStatus == 'active' or subs_obj.last().stripeStatus == 'canceled':
                pricingkey = subs_obj.last().priceId
                rewords =Plan.objects.get(PlanKey =pricingkey).noOfRewordsPerDay
                if (HitCount.objects.filter(user__in=users, hitTime__date=datetime.today().date()).count()) < rewords:
                    response = GPTResponse(prompt_txt)
                    return HttpResponse(response.replace('\n\n','<p><br data-cke-filler="true"></p>').replace('\n','<p><br data-cke-filler="true"></p>'))
                else:
                    return HttpResponse(messages['ExceedLimit'])
            else:
                return HttpResponse(messages['InActiveUsers'])
        else:
            if (date.today() - admin_user.first().createdOnUtc.date()).days > trial_period_days:
                return HttpResponse(messages['InActiveUsers'])
            else:
                response = GPTResponse(prompt_txt)
                return HttpResponse(response.replace('\n\n','<p><br data-cke-filler="true"></p>').replace('\n','<p><br data-cke-filler="true"></p>'))
    

        
class CountHits(TemplateView):

    def get(self,request, *args, **kwargs):
        # encoded_token = request.headers['Authorization'].split(' ')[1]
        # status_code = authenticate_user(encoded_token)
        # if status_code != 200:
        #      return HttpResponse("Unauthorized", status = 401)
        email = request.GET['email']
        userid = request.GET['user_id']
        organization_id = request.GET['organization_id']
        prompt_txt = request.GET['prompt_txt']
        users = User.objects.filter(zendeskOrganizationId=organization_id)
        admin_user = users.filter(role='admin')
        subs_obj = Subscription.objects.filter(userId__in=admin_user)
        if subs_obj.exists():
            if subs_obj.last().stripeStatus == 'active' or subs_obj.last().stripeStatus == 'canceled':
                pricingkey = subs_obj.last().priceId
                rewords = Plan.objects.get(PlanKey=pricingkey).noOfRewordsPerDay
                if (HitCount.objects.filter(user__in=users,hitTime__date=datetime.today().date()).count()) < rewords:
                    hitcount = HitCount.objects.create(user = User.objects.get(zendeskUserid=userid),promptText = prompt_txt)
                    return HttpResponse(hitcount)
                else:
                    return HttpResponse("error")
            else:
                return HttpResponse("error")
        else:
            if (date.today() - admin_user.first().createdOnUtc.date()).days > trial_period_days:
                return HttpResponse(messages['InActiveUsers'])
            else:
                hitcount = HitCount.objects.create(user=User.objects.get(zendeskUserid=userid), promptText=prompt_txt)
                return HttpResponse(hitcount)

class UpdateUser(TemplateView):

    def get(self,request, *args, **kwargs):
        print("update_user")
        user_obj=User.objects.get(email='pawansinghania@creativebuffer.com')
        print("user_obj")
        user_obj.createdOnUtc = datetime.now() - timedelta(days=3)
        user_obj.save()
        print("user_obj")
        return JsonResponse({'success':'success'})
    


class SaveUser(TemplateView):

    def get(self,request, *args, **kwargs):
        # print("1")
        # status_code =  authenticate_user(request.headers['Authorization'].split(' ')[1])
        # if status_code != 200:
        #      print("2","unauthorize")
        #      return HttpResponse("Unauthorized", status = 401)



        # plan will not inactive because of recurring payment.
        # subs = Subscription.objects.all()
        # for s in subs:
        #     if (date.today() > s.subscriptionEndsAt.date() or date.today() == s.subscriptionEndsAt.date()):
        #         s.stripeStatus = 'inactive'
        #         s.save()
        #     else:
        #         continue
        user_id = request.GET['user_id']
        print("3",user_id)
        email = request.GET['email']
        print("4",email)
        name = request.GET['name']
        print("5",name)
        role = request.GET['role']
        print("6",role)
        organization_id = request.GET['organization_id']
        print("7",organization_id)
        if User.objects.filter(email = email,zendeskOrganizationId=organization_id).exists():
            print("8","User and org exist")
            pass
        else:
            print("14","user createddd")
            User.objects.create(
                name = name,
                email = email,
                role = role,
                zendeskUserid = user_id,
                zendeskOrganizationId = organization_id,
            )
            print("15","success")
        # if Subscription.objects.filter(userId__in=User.objects.filter(role='admin', zendeskOrganizationId=organization_id)).exists():
        #     subs_obj = Subscription.objects.filter(userId__in=User.objects.filter(role='admin', zendeskOrganizationId=organization_id)).last().stripeStatus
        #     if subs_obj == 'active' or subs_obj == 'canceled':
        #         show = True
        #     elif subs_obj == 'inactive':
        #         show = False
        # else:
        #     user = User.objects.filter(role='admin', zendeskOrganizationId=organization_id).first()
        #     delta = datetime.today().date() - user.createdOnUtc.date()
        #     if (delta.days > trial_period_days):
        #         show = False
        #     else:
        #         show =True
        return JsonResponse({'success':'success'})



class FetchUserToken(TemplateView):

    def get(self, request):
        # roles = RoleSentimentToneMapping.objects.filter()
        # for r in roles:
        #     r.language = Language.objects.filter().first()
        #     r.yni_tone = YesNoInstructTone.objects.filter().first()
        #     r.save()
        token = request.headers['Authorization'].split(' ')[1]
        encoded_token = encrypt_message(token)
        return JsonResponse({'encoded_token':encoded_token})
    
class GetJWTToken(TemplateView):

    def get(self, request):
        email = request.GET['email']
        name = request.GET['name']
        organization_id = request.GET['organization_id']
        payload = {
            'name': name,
            'email': email,
            'iat': datetime.now().timestamp(),
            'exp': datetime.now().timestamp() + timedelta(days=1).total_seconds(),
            'org_id': organization_id
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
        return JsonResponse({'token':token})
    

class GetJWTTokenById(TemplateView):

    def get(self, request):
        user_id = request.GET['user_id']
        payload = {
            'user_id': user_id,
            'iat': datetime.now().timestamp(),
            'exp': datetime.now().timestamp() + timedelta(days=1).total_seconds(),
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
        return JsonResponse({'token':token})

class APIHitsInfo(BaseDatatableView):
    
    order_columns = ["date","date","hit_count"]

    def get_initial_queryset(self):
        # try:
        #     print(self.request.headers)
        #     encoded_token = self.request.headers['Authorization'].split(' ')[1]
        #     print(self.request.headers['Authorization'].split(' ')[1])
        #     status_code = authenticate_user(encoded_token)
        #     if status_code != 200:
        #         return HttpResponse("Unauthorized", status = 401)
        # except:
        #     return HttpResponse("Unauthorized", status = 401)
        role = self.request.GET['role']
        try:
            organization_id = self.request.GET['org']
            if role == 'admin':
                if User.objects.filter(zendeskOrganizationId = organization_id).exists():
                    users = User.objects.filter(zendeskOrganizationId = organization_id)
                    hitcount = (
                        HitCount.objects.filter(user__in = users)
                        .annotate(date=TruncDate('hitTime')).values('date')
                        .annotate(hit_count=Count('hitCountId')).order_by('-date')
                    )
        except:
            user_id = self.request.GET['user_id']
            if role == 'admin':
                user_obj = User.objects.filter(userId = user_id)
                if user_obj.exists():
                    users = user_obj
                    hitcount = (
                        HitCount.objects.filter(user__in = users)
                        .annotate(date=TruncDate('hitTime')).values('date')
                        .annotate(hit_count=Count('hitCountId')).order_by('-date')
                    )
        return hitcount

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        to_date = self.request.GET.get('search[to_date]')
        from_date = self.request.GET.get('search[from_date]')
        if search:
            qs = qs.filter(Q(hit_count__icontains=search)|Q(date__icontains=search))
        if from_date and to_date:
            qs = qs.filter(Q(date__range=[from_date, to_date]))
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                "date": item['date'],
                "hit_count":item['hit_count'],
            })

        return json_data
        
        
class GetAdminData(TemplateView):
    
    def get(self, request, *args, **kwargs):
        status_code = authenticate_user(request.headers['Authorization'].split(' ')[1])
        if status_code != 200:
             return HttpResponse("Unauthorized", status = 401)
        organization_id = kwargs['organizatin_id']
        user = User.objects.filter(zendeskOrganizationId=organization_id,role='admin')
        subs = Subscription.objects.filter(userId__in=user)
        if subs.exists():
            if subs.last().stripeStatus == 'active':
                status= 'active'
            elif subs.last().stripeStatus == 'canceled':
                status = 'canceled'
            else:
                status= 'inactive'
        else:
            status= 'inactive'
        return JsonResponse({'subs':status})
        
        

# No use of this function
class FetchAllUsers(TemplateView):

    def get(self,request, *args, **kwargs):
        status_code = authenticate_user(request.headers['Authorization'].split(' ')[1])
        if status_code != 200:
             return HttpResponse("Unauthorized", status = 401)
        role = request.GET['user_info[role]']
        organization_id = request.GET['user_info[organizations][0][id]']
        if role == 'admin':
            users = User.objects.filter(zendeskOrganizationId = organization_id).values('name','email','role')
            return HttpResponse(json.dumps(list(users)), 'application/json')
        else:
             raise Http404
        

class CheckPricing(TemplateView):

    def get(self,request, *args, **kwargs):
        status_code = authenticate_user(request.headers['Authorization'].split(' ')[1])
        if status_code != 200:
             return HttpResponse("Unauthorized", status = 401)
        organization_id = request.GET['org_id']
        admin_user = User.objects.filter(role='admin',zendeskOrganizationId=organization_id)
        subs_obj = Subscription.objects.filter(userId__in=admin_user)
        if subs_obj.exists():
            if subs_obj.last().stripeStatus == 'active' or subs_obj.last().stripeStatus == 'canceled':
                return JsonResponse({"status":"paid"})
            else:
                return JsonResponse({"status":"unpaid"})
        else:
            if (date.today() - admin_user.first().createdOnUtc.date()).days > trial_period_days:
                return JsonResponse({"status":"unpaid"})
            else:
                return JsonResponse({"status":"paid"})
             
     


class AdminDashboard(TemplateView):
    template_name = "admin_dash.html"

    def get(self,request, *args, **kwargs):
        if request.user.is_authenticated :
            context = {}
            return render(request, self.template_name, context)
        else:
            return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        formData = request.body.decode().split('&')
        username = formData[0].split('username=')[1]
        password=formData[1].split('password=')[1]
        try:
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request, self.template_name)
        except:
            return render(request, 'login.html')



class AccountOwnerDashboard(TemplateView):
    template_name = "account_owner_dash.html"

    def get(self,request, *args, **kwargs):
        status_code = authenticate_user(request.headers['Authorization'].split(' ')[1])
        if status_code != 200:
             return HttpResponse("Unauthorized", status = 401)
        context = {}
        return render(request, self.template_name, context)
    

class AdminSettings(TemplateView):
    template_name = "admin_dash.html"

    def get(self,request, *args, **kwargs):
        if request.user.is_superuser:
            context = {}
            role = list(Role.objects.filter(accountOwnerID=0,isDeleted = False).values('roleId','agentRoleUI','agentRoleAPI'))
            sentiment = list(Sentiment.objects.filter(accountOwnerID=0,isDeleted = False).values('sentimentId','customerSentimentUI','customerSentimentAPI'))
            tone = list(Tone.objects.filter(accountOwnerID=0,isDeleted = False).values('toneId','replyToneUI','replyToneAPI'))
            language = list(Language.objects.filter(accountOwnerID=0,isDeleted = False).values('languageId','replylanguageUI','replylanguageAPI'))
            yni_tone = list(YesNoInstructTone.objects.filter(accountOwnerID=0,isDeleted = False).values('yniId','yniToneUI','yniToneAPI'))
            context.update({'role':json.dumps(role)})
            context.update({'sentiment':json.dumps(sentiment)})
            context.update({'tone':json.dumps(tone)})
            context.update({'language':json.dumps(language)})
            context.update({'yni_tone':json.dumps(yni_tone)})
            return JsonResponse(context)
        else:
            return redirect('admin_dashboard')


class UpdateConfig(TemplateView):
    template_name = "admin_dash.html"

    def post(self,request, *args, **kwargs):
        if request.user.is_superuser :
            context = json.loads(request.body.decode())
            role = context['role']
            sentiment = context['sentiment']
            tone = context['tone']
            language = context['language']
            yni_tone = context['yni_tone']
            try:
                configurations = context['configurations']
            except:
                configurations = None
            if context['user_id'] == 0:
                user_id = 0
            else:
                user_id= User.objects.get(userId = context['user_id']).zendeskOrganizationId
            with transaction.atomic():
                if configurations != None:
                    roles =RoleSentimentToneMapping.objects.filter(isDeleted=False, zendeskOrganizationId=user_id,isDefault=True)
                    user = User.objects.filter(role='admin', zendeskOrganizationId=user_id).first()
                    role_1 = Role.objects.filter(agentRoleAPI=configurations['role'])
                    sentiment_1 = Sentiment.objects.filter(customerSentimentAPI=configurations['sentiment'])
                    tone_1 = Tone.objects.filter(replyToneAPI=configurations['tone'])
                    language_1 = Language.objects.filter(replylanguageAPI=configurations['language'])
                    yni_tone_1 = YesNoInstructTone.objects.filter(yniToneAPI=configurations['yni_tone'])
                    if role_1.filter(accountOwnerID=user_id).exists():
                        role1 = role_1.get(accountOwnerID=user_id)
                    else:
                        role1 = role_1.get(accountOwnerID=0)
                    if sentiment_1.filter(accountOwnerID=user_id).exists():
                        sentiment1 = sentiment_1.get(accountOwnerID=user_id)
                    else:
                        sentiment1 = sentiment_1.get(accountOwnerID=0)
                    if tone_1.filter(accountOwnerID=user_id).exists():
                        tone1 = tone_1.get(accountOwnerID=user_id)
                    else:
                        tone1 = tone_1.get(accountOwnerID=0)
                    if language_1.filter(accountOwnerID=user_id).exists():
                        language_1 = language_1.get(accountOwnerID=user_id)
                    else:
                        language_1 = language_1.get(accountOwnerID=0)
                    if yni_tone_1.filter(accountOwnerID=user_id).exists():
                        yni_tone1 = yni_tone_1.get(accountOwnerID=user_id)
                    else:
                        yni_tone1 = yni_tone_1.get(accountOwnerID=0)
                    for r in roles:
                        r.isDefault = False
                        r.save()
                    RoleSentimentToneMapping.objects.create(
                        zendeskOrganizationId=user_id,
                        user_id=user,
                        role=role1,
                        sentiment=sentiment1,
                        tone=tone1,
                        language=language_1,
                        yni_tone=yni_tone1,
                        isDefault=True,
                        createdBy=1,
                        modifiedBy=1
                    )
            with transaction.atomic():
                if Role.objects.filter(accountOwnerID=user_id).exists():
                    for i in role:
                        role_obj = Role.objects.get(accountOwnerID=user_id ,roleId=i['id'],isDeleted=False)
                        role_obj.agentRoleAPI = i['api_wording']
                        role_obj.agentRoleUI = i['ui_wording']
                        role_obj.save()
                else:
                    for i in role:
                        Role.objects.create(
                            agentRoleAPI = i['api_wording'],
                            agentRoleUI = i['ui_wording'],
                            accountOwnerID=user_id
                        )
                if Sentiment.objects.filter(accountOwnerID=user_id).exists():
                    for i in sentiment:
                        sentiment_obj = Sentiment.objects.get(accountOwnerID=user_id,sentimentId=i['id'],isDeleted=False)
                        sentiment_obj.customerSentimentAPI = i['api_wording']
                        sentiment_obj.customerSentimentUI = i['ui_wording']
                        sentiment_obj.save()
                else:
                    for i in sentiment:
                        Sentiment.objects.create(
                            customerSentimentAPI = i['api_wording'],
                            customerSentimentUI = i['ui_wording'],
                            accountOwnerID=user_id
                        )
                if Tone.objects.filter(accountOwnerID=user_id).exists():
                    for i in tone:
                        tone_obj = Tone.objects.get(accountOwnerID=user_id,toneId=i['id'],isDeleted=False)
                        tone_obj.replyToneAPI = i['api_wording']
                        tone_obj.replyToneUI = i['ui_wording']
                        tone_obj.save()
                else:
                    for i in tone:
                        Tone.objects.create(
                        replyToneAPI = i['api_wording'],
                        replyToneUI = i['ui_wording'],
                        accountOwnerID=user_id
                        )      
                if Language.objects.filter(accountOwnerID=user_id).exists():
                    for i in language:
                        language_obj = Language.objects.get(accountOwnerID=user_id,languageId=i['id'],isDeleted=False)
                        language_obj.replylanguageAPI = i['api_wording']
                        language_obj.replylanguageUI = i['ui_wording']
                        language_obj.save()
                else:
                    for i in language:
                        Language.objects.create(
                        replylanguageAPI = i['api_wording'],
                        replylanguageUI = i['ui_wording'],
                        accountOwnerID=user_id
                        )      
                if YesNoInstructTone.objects.filter(accountOwnerID=user_id).exists():
                    for i in yni_tone:
                        yni_obj = YesNoInstructTone.objects.get(accountOwnerID=user_id,yniId=i['id'],isDeleted=False)
                        yni_obj.yniToneAPI = i['api_wording']
                        yni_obj.yniToneUI = i['ui_wording']
                        yni_obj.save()
                else:
                    for i in yni_tone:
                        YesNoInstructTone.objects.create(
                        yniToneAPI = i['api_wording'],
                        yniToneUI = i['ui_wording'],
                        accountOwnerID=user_id
                        )      
                return JsonResponse({"success":"success"})
        else:
            return redirect('admin_dashboard')

    

class GetAccountOwnerInfo(TemplateView):
    template_name = "admin_dash.html"

    def get(self,request, *args, **kwargs):
        if request.user.is_superuser:
            context = {}
            user_id = kwargs['user_id']
            print(user_id)
            org_id = User.objects.get(userId = user_id).zendeskOrganizationId
            mapping = list(RoleSentimentToneMapping.objects.filter(zendeskOrganizationId = org_id, isDefault=True,isDeleted=False)\
            .values('role__agentRoleAPI','sentiment__customerSentimentAPI','tone__replyToneAPI','language__replylanguageAPI','yni_tone__yniToneAPI'))
            languages= Language.objects.filter(isDeleted=False)
            yni_tones = YesNoInstructTone.objects.filter(isDeleted=False)
            if Role.objects.filter(accountOwnerID=org_id ,isDeleted=False).exists():
                role = Role.objects.filter(accountOwnerID=org_id ,isDeleted=False).values('roleId','agentRoleUI','agentRoleAPI')
            else:
                role = Role.objects.filter(accountOwnerID=0 ,isDeleted=False).values('roleId','agentRoleUI','agentRoleAPI')
            if Sentiment.objects.filter(accountOwnerID=org_id,isDeleted=False).exists():
                sentiment = Sentiment.objects.filter(accountOwnerID=org_id,isDeleted=False).values('sentimentId','customerSentimentUI','customerSentimentAPI')
            else:
                sentiment = Sentiment.objects.filter(accountOwnerID=0,isDeleted=False).values('sentimentId','customerSentimentUI','customerSentimentAPI')
            if Tone.objects.filter(accountOwnerID=org_id,isDeleted=False).exists():
                tone = Tone.objects.filter(accountOwnerID=org_id,isDeleted=False).values('toneId','replyToneUI','replyToneAPI')
            else:
                tone = Tone.objects.filter(accountOwnerID=0,isDeleted=False).values('toneId','replyToneUI','replyToneAPI')
            if languages.filter(accountOwnerID=org_id).exists():
                language = languages.filter(accountOwnerID=org_id).values('languageId','replylanguageUI','replylanguageAPI')
            else:
                language = languages.filter(accountOwnerID=0).values('languageId','replylanguageUI','replylanguageAPI')
            if yni_tones.filter(accountOwnerID=org_id).exists():
                yni_tone =yni_tones.filter(accountOwnerID=org_id).values('yniId','yniToneUI','yniToneAPI')
            else:
                yni_tone = yni_tones.filter(accountOwnerID=0).values('yniId','yniToneUI','yniToneAPI')
            context.update({"users_configure":json.dumps(mapping)})
            context.update({"role":json.dumps(list(role))})
            context.update({"sentiment":json.dumps(list(sentiment))})
            context.update({"tone":json.dumps(list(tone))})
            context.update({"language":json.dumps(list(language))})
            context.update({"yni_tone":json.dumps(list(yni_tone))})
            return JsonResponse(context)
        else:
            return redirect('admin_dashboard')
       
    
class GetAllAccountOwners(BaseDatatableView):

    order_columns = ["userId","name","email"]

    def get_initial_queryset(self):
        users = User.objects.filter(role = 'admin').values('userId','name','email','zendeskUserid','createdOnUtc')
        print("1", users)
        return users

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        print("2", search)
        if search:
            qs = qs.filter(Q(name__icontains=search)|Q(email__icontains=search))
        print("3", qs)
        return qs

    def prepare_results(self, qs):
        json_data = []
        subs = Subscription.objects.filter()
        print("4", subs)
        for item in qs:
            print("5", item)
            hit_counts = HitCount.objects.filter(user=item['userId']).last()
            print("6", hit_counts)
            user_id = User.objects.get(zendeskUserid=item['zendeskUserid'])
            print("7", user_id)
            if(subs.filter(stripeStatus="active", userId=user_id).exists()):
                print("8")
                plan = Plan.objects.get(PlanKey = subs.filter(stripeStatus="active",userId=user_id).last().priceId)
                print("9", plan)
                subs1 = subs.filter(stripeStatus="active",userId=user_id).last()
                print("10", subs1)
            elif(subs.filter(stripeStatus="inactive", userId=user_id).exists()):
                print('11')
                plan = 'Expired'
                subs1 = subs.filter(stripeStatus="inactive",userId=user_id).last()
                print('12',subs1)
            elif(subs.filter(stripeStatus="canceled", userId=user_id).exists()):
                print('13')
                plan = Plan.objects.get(PlanKey = subs.filter(stripeStatus="canceled",userId=user_id).last().priceId)
                print('14',plan)
                subs1 = subs.filter(stripeStatus="canceled",userId=user_id).last()
                print('15', subs1)
            else:
                print('16')
                plan = 'No Plan'
                subs1 = None
            print('17',item['userId'])
            print('18',item['name'])
            print('19',item['email'])
            print('20', plan.title if type(plan) != str else plan)
            print('21',plan.interval if type(plan) != str else '-')
            print('22',(subs1.subscriptionStartsAt).date() if subs1 else '-')
            print('23',subs1.stripeStatus if subs1 else 'No Plan')
            print('24',hit_counts.hitTime.date() if hit_counts else '-')
            json_data.append({
                "id": item['userId'],
                "name": item['name'],
                "email":item['email'],
                "subs_plan": plan.title if type(plan) != str else plan,
                "subs_interval":plan.interval if type(plan) != str else '-',
                "billing_date":(subs1.subscriptionStartsAt).date() if subs1 else '-',
                "status":subs1.stripeStatus if subs1 else 'No Plan',
                # "install_date": item['createdOnUtc'].date(),
                "last_date_api_call": hit_counts.hitTime.date() if hit_counts else '-'
            })
        print('25', json_data)
        return json_data


class GetPlans(BaseDatatableView):

    order_columns = ["id","title","interval","price","noOfRewordsPerDay"]

    def get_initial_queryset(self):
        plan = Plan.objects.filter().values()
        return plan

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        print(search)
        if search:
            qs = qs.filter(Q(title__icontains=search)|Q(noOfRewordsPerDay__icontains=search)|Q(interval__icontains=search)|Q(price__icontains=search))
        return qs

    def prepare_results(self, qs):
        json_data = []
        subs = Subscription.objects.filter()
        for item in qs:
            json_data.append({
                "title": item['title'],
                "rewords_per_day":item['noOfRewordsPerDay'],
                "interval": item['interval'],
                "price":str(item['price'])+'$',
                "total_users":subs.filter(stripeStatus='active',priceId=item['PlanKey']).count()
            })
        return json_data
    

def GPTResponse(prompt_txt):
    print("25")
    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature= 1,
        max_tokens= 1050,
        top_p= 1,
        frequency_penalty= 0.75,
        presence_penalty= 0,
        messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_txt},
            ]
        ).choices[0]["message"]['content']
        print(response)
        print("26",response)
    except:
        print("27","exeption error")
        response = "Sorry, AI is currently unable to generate content. Please try again later."
    print("28",response)
    return response