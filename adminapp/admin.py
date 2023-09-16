from django.contrib import admin
from .models import User, HitCount


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'role','zendeskUserid','zendeskOrganizationId','createdOnUtc']

class HitCountAdmin(admin.ModelAdmin):
    list_display = ('user','hitTime','promptText')

admin.site.register(User, UserAdmin)
admin.site.register(HitCount, HitCountAdmin)