from django.db import models

# Create your models here.

class User(models.Model): #ZENDESK USER
    userId = models.BigAutoField(primary_key=True)
    authOUid = models.CharField(max_length=20,null=True, blank=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    role = models.CharField(max_length=50)
    createdBy = models.IntegerField(null=True, blank=True)
    createdOnUtc = models.DateTimeField(auto_now_add=True)
    modifiedBy = models.IntegerField(null=True, blank=True)
    modifiedOnUtc = models.DateTimeField(auto_now=True)
    zendeskUserid = models.IntegerField(null=True, blank=True)
    zendeskOrganizationId = models.CharField(max_length=2000, null=True, blank=True)
    zendeskOrganizationName = models.CharField(max_length=300, null=True, blank=True)
    zendeskCreatedUserTime =  models.DateTimeField(null=True, blank=True)
    zendeskUserUrl = models.CharField(max_length=1000, null=True, blank=True)
    isSuspended = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)


class HitCount(models.Model):
    hitCountId = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hitTime = models.DateTimeField(auto_now_add=True)
    promptText = models.CharField(max_length=10000, null=True, blank=True)

