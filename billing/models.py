from django.db import models
from adminapp.models import User
from datetime import datetime, timedelta, date

# Create your models here.
class Plan(models.Model):
    # planId = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    productKey =  models.CharField(max_length=200, null=True, blank=True)
    PlanKey = models.CharField(max_length=200, null=True, blank=True)
    noOfRewordsPerDay = models.IntegerField(default=0)
    suitableForTeam = models.IntegerField(default=0)
    price = models.IntegerField(default=0) #in USD
    discount = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=5000, null=True, blank=True)
    interval = models.CharField(max_length=30, null=True, blank=True) #Yearly or monthly


class UserPlan(models.Model):
    # userPlanId = models.BigAutoField(primary_key=True)
    accounOwner = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    createdTime = models.DateTimeField(auto_now_add=True, editable=True)

    def valid(self):
        if self.plan.mode == 'Yearly':
            return datetime.now()+timedelta(days=365)
        else:
            return datetime.now()+timedelta(days=30)


class Subscription(models.Model):
    subsId = models.BigAutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    stripeSubscriptionId = models.CharField(max_length=200, null=True, blank=True)
    stripeStatus = models.CharField(max_length=200, null=True, blank=True)
    customerId = models.CharField(max_length=200, null=True, blank=True)
    productId = models.CharField(max_length=200, null=True, blank=True)
    priceId = models.CharField(max_length=200, null=True, blank=True)
    trialEndsAt = models.DateTimeField()
    subscriptionStartsAt = models.DateTimeField(null=True, blank=True)
    subscriptionEndsAt = models.DateTimeField()
    renewPlanDate = models.DateTimeField(null=True, blank=True)
    invoiceId = models.CharField(max_length=200, null=True, blank=True)
    invoiceDetail = models.CharField(max_length=200, null=True, blank=True)
    createdOnUTC = models.DateTimeField(auto_now_add=True, editable=True)
    updatedOnUTC = models.DateTimeField(auto_now=True, editable=True)