from django.views.generic import TemplateView
from django.http import HttpResponse
from django.db import transaction
from django.http import Http404
from .models import *
import json
from adminapp.models import User
import requests
from cryptography.fernet import Fernet


def load_key():
    """
    Load the previously generated key
    """
    return open("master/secret.key", "rb").read()


def authenticate_user(token):
    headers =  {"Authorization": "Bearer " + token}
    r = requests.get('https://dev-nn662qqnxm3h1yhm.us.auth0.com/userinfo',headers=headers)
    print("authentication_code",r.status_code)
    return r.status_code


def encrypt_message(message):
    """
    Encrypts a message
    """
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)

    print(encrypted_message)
    return encrypted_message.decode()

def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    print(decrypted_message)
    return decrypted_message.decode()


class GetConfiguration(TemplateView):

    def get(self,request, *args, **kwargs):
        status_code = authenticate_user(request.headers['Authorization'].split(' ')[1])
        if status_code != 200:
             return HttpResponse("Unauthorized", status = 401)        
        context = {}
        try:
            organization_id = kwargs['organization_id']
        except:
            organization_id = None
        if organization_id != None:
            mapping = RoleSentimentToneMapping.objects.filter(zendeskOrganizationId = organization_id, isDefault=True,isDeleted=False)\
            .values('role__agentRoleAPI', 'sentiment__customerSentimentAPI','tone__replyToneAPI','language__replylanguageAPI','yni_tone__yniToneAPI','isYniToneIgnoredForInstruct','isLanguageIgnoredForInstruct')
            context.update({'selected_txt':json.dumps(list(mapping))})
        user_id = User.objects.filter(role='admin',zendeskOrganizationId = organization_id)
        if Role.objects.filter(accountOwnerID=organization_id).exists():
            role = Role.objects.filter(accountOwnerID=organization_id, isDeleted=False).values('agentRoleUI','agentRoleAPI')
        else:
            role = Role.objects.filter(accountOwnerID=0, isDeleted=False).values('agentRoleUI','agentRoleAPI')
        if Sentiment.objects.filter(accountOwnerID=organization_id).exists():
            sentiment = Sentiment.objects.filter(accountOwnerID=organization_id,isDeleted=False).values('customerSentimentUI','customerSentimentAPI')
        else:
            sentiment = Sentiment.objects.filter(accountOwnerID=0, isDeleted=False).values('customerSentimentUI','customerSentimentAPI')
        if Tone.objects.filter(accountOwnerID=organization_id).exists():
            tone = Tone.objects.filter(accountOwnerID=organization_id,isDeleted=False).values('replyToneUI','replyToneAPI')
        else:
            tone = Tone.objects.filter(accountOwnerID=0,isDeleted=False).values('replyToneUI','replyToneAPI')
        if Language.objects.filter(accountOwnerID=organization_id).exists():
            language = Language.objects.filter(accountOwnerID=organization_id,isDeleted=False).values('replylanguageUI','replylanguageAPI')
        else:
            language = Language.objects.filter(accountOwnerID=0,isDeleted=False).values('replylanguageUI','replylanguageAPI')
        if YesNoInstructTone.objects.filter(accountOwnerID=organization_id).exists():
            yni_tone = YesNoInstructTone.objects.filter(accountOwnerID=organization_id,isDeleted=False).values('yniToneUI','yniToneAPI')
        else:
            yni_tone = YesNoInstructTone.objects.filter(accountOwnerID=0,isDeleted=False).values('yniToneUI','yniToneAPI')
        context.update({"role":json.dumps(list(role))})
        context.update({"sentiment":json.dumps(list(sentiment))})
        context.update({"tone":json.dumps(list(tone))})
        context.update({"language":json.dumps(list(language))})
        context.update({"yni_tone":json.dumps(list(yni_tone))})
        if context:
            return HttpResponse(json.dumps(context))
        else:
            raise Http404
    

class SaveDefaultConfiguration(TemplateView):

    def post(self,request, *args, **kwargs):
        # status_code = authenticate_user(request.headers['Authorization'].split(' ')[1])
        # if status_code != 200:
        #      return HttpResponse("Unauthorized", status = 401)
        role = request.POST['role']
        sentiment = request.POST['sentiment']
        tone = request.POST['tone']
        try:
            language = request.POST['language']
            ignore_language = request.POST['ignore_language']
            yni_tone = request.POST['yni_tone']
            ignore_yni_tone = request.POST['ignore_yni_tone']
        except:
            pass
        organizationId = request.POST['organization_id']
        roles = RoleSentimentToneMapping.objects.filter(isDeleted= False , zendeskOrganizationId=organizationId,isDefault = True)
        user = User.objects.filter(role='admin',zendeskOrganizationId=organizationId).first()
        role_obj = Role.objects.filter(agentRoleAPI = role)
        sentiment_obj = Sentiment.objects.filter(customerSentimentAPI = sentiment)
        tone_obj = Tone.objects.filter(replyToneAPI = tone)
        try:
            language_obj = Language.objects.filter(replylanguageAPI = language)
            yni_tone_obj = YesNoInstructTone.objects.filter(yniToneAPI = yni_tone)
        except:
            pass
        if role_obj.filter(accountOwnerID=organizationId).exists():
            role = role_obj.get(accountOwnerID=organizationId)
        else:
            role = role_obj.get(accountOwnerID=0)
        if sentiment_obj.filter(accountOwnerID=organizationId).exists():
            sentiment = sentiment_obj.get(accountOwnerID=organizationId)
        else:
            sentiment = sentiment_obj.get(accountOwnerID=0)
        if tone_obj.filter(accountOwnerID=organizationId).exists():
            tone = tone_obj.get(accountOwnerID=organizationId)
        else:
            tone = tone_obj.get(accountOwnerID=0)
        try:
            if language_obj.filter(accountOwnerID=organizationId).exists():
                language = language_obj.get(accountOwnerID=organizationId)
            else:
                language = language_obj.get(accountOwnerID=0)
            if yni_tone_obj.filter(accountOwnerID=organizationId).exists():
                yni_tone = yni_tone_obj.get(accountOwnerID=organizationId)
            else:
                yni_tone = yni_tone_obj.get(accountOwnerID=0)
        except:
            ignore_language = 'false'
            ignore_yni_tone = 'false'
            language = Language.objects.filter(accountOwnerID=0).first()
            yni_tone = YesNoInstructTone.objects.filter(accountOwnerID=0).first()
        with transaction.atomic():
            for r in roles:
                r.isDefault = False
                r.save()        
            mapping = RoleSentimentToneMapping.objects.create(
                zendeskOrganizationId = organizationId,
                user_id =user,
                role = role,
                sentiment =sentiment,
                tone = tone,
                language = language,
                yni_tone = yni_tone,
                isLanguageIgnoredForInstruct=True if ignore_language=='true' else False,
                isYniToneIgnoredForInstruct=True if ignore_yni_tone=='true' else False,
                isDefault = True,
                createdBy = 1,
                modifiedBy = 1
            )
            if mapping:
                return HttpResponse(True)
            else:
                raise Http404
    

        

