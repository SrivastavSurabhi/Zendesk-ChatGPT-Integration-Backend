from django.contrib import admin
from .models import *

# Register your models here.
class RoleAdmin(admin.ModelAdmin):
    list_display = ('agentRoleAPI', 'agentRoleUI', 'accountOwnerID','createdOnUtc')

class SentimentAdmin(admin.ModelAdmin):
    list_display =  ('customerSentimentAPI', 'customerSentimentUI', 'accountOwnerID','createdOnUtc')

class ToneAdmin(admin.ModelAdmin):
    list_display =  ('replyToneAPI', 'replyToneUI', 'accountOwnerID','createdOnUtc')

class RoleSentimentToneMappingAdmin(admin.ModelAdmin):
    list_display =  [field.name for field in RoleSentimentToneMapping._meta.get_fields()]

class LanguageAdmin(admin.ModelAdmin):
    list_display =  ('replylanguageAPI', 'replylanguageUI', 'accountOwnerID','createdOnUtc')

class YesNoInstructToneAdmin(admin.ModelAdmin):
    list_display =  ('yniToneAPI', 'yniToneUI', 'accountOwnerID','createdOnUtc')



admin.site.register(Role,RoleAdmin)
admin.site.register(Sentiment,SentimentAdmin)
admin.site.register(Tone,ToneAdmin)
admin.site.register(RoleSentimentToneMapping,RoleSentimentToneMappingAdmin)
admin.site.register(Language,LanguageAdmin)
admin.site.register(YesNoInstructTone,YesNoInstructToneAdmin)