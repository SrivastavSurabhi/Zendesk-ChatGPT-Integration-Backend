from django.db import models
from adminapp.models import User

# Create your models here.

class Role(models.Model):
    roleId = models.BigAutoField(primary_key=True)
    agentRoleAPI = models.CharField(max_length=500,null=True, blank=True)
    agentRoleUI = models.CharField(max_length=500,null=True, blank=True)
    accountOwnerID = models.CharField(max_length=50,default=1)
    createdBy = models.IntegerField(null=True, blank=True)
    createdOnUtc = models.DateTimeField(auto_now_add=True)
    modifiedBy = models.IntegerField(null=True, blank=True)
    modifiedOnUtc = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False)


class Sentiment(models.Model):
    sentimentId = models.BigAutoField(primary_key=True)
    customerSentimentAPI = models.CharField(max_length=500,null=True, blank=True)
    customerSentimentUI = models.CharField(max_length=500,null=True, blank=True)
    accountOwnerID = models.CharField(max_length=50,default=1)
    createdBy = models.IntegerField(null=True, blank=True)
    createdOnUtc = models.DateTimeField(auto_now_add=True)
    modifiedBy = models.IntegerField(null=True, blank=True)
    modifiedOnUtc = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False)


class Tone(models.Model):
    toneId = models.BigAutoField(primary_key=True)
    replyToneAPI = models.CharField(max_length=500,null=True, blank=True)
    replyToneUI = models.CharField(max_length=500,null=True, blank=True)
    accountOwnerID = models.CharField(max_length=50,default=1)
    createdBy = models.IntegerField(null=True, blank=True)
    createdOnUtc = models.DateTimeField(auto_now_add=True)
    modifiedBy = models.IntegerField(null=True, blank=True)
    modifiedOnUtc = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False)


class Language(models.Model):
    languageId = models.BigAutoField(primary_key=True)
    replylanguageAPI = models.CharField(max_length=500,default="American English")
    replylanguageUI = models.CharField(max_length=500,default="American English")
    accountOwnerID = models.CharField(max_length=50,default=1)
    createdBy = models.IntegerField(null=True, blank=True)
    createdOnUtc = models.DateTimeField(auto_now_add=True)
    modifiedBy = models.IntegerField(null=True, blank=True)
    modifiedOnUtc = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False)


class YesNoInstructTone(models.Model): #Tone for Yes, No , Instruct and More Info
    yniId = models.BigAutoField(primary_key=True)
    yniToneAPI = models.CharField(max_length=500,default="Polite")
    yniToneUI = models.CharField(max_length=500,default="Polite")
    accountOwnerID = models.CharField(max_length=50,default=1)
    createdBy = models.IntegerField(null=True, blank=True)
    createdOnUtc = models.DateTimeField(auto_now_add=True)
    modifiedBy = models.IntegerField(null=True, blank=True)
    modifiedOnUtc = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False)



class RoleSentimentToneMapping(models.Model):
    rstId = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    zendeskOrganizationId = models.CharField(max_length=200, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    sentiment = models.ForeignKey(Sentiment, on_delete=models.CASCADE)
    tone = models.ForeignKey(Tone, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE,default=1)
    yni_tone = models.ForeignKey(YesNoInstructTone, on_delete=models.CASCADE,default=1)
    isLanguageIgnoredForInstruct = models.BooleanField(default=False)
    isYniToneIgnoredForInstruct = models.BooleanField(default=False)
    isDefault = models.BooleanField(default=False)
    createdBy = models.IntegerField(null=True, blank=True)
    createdOnUtc = models.DateTimeField(auto_now_add=True)
    modifiedBy = models.IntegerField(null=True, blank=True)
    modifiedOnUtc = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False)