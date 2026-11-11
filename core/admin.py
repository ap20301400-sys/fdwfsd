from django.contrib import admin
from .models import (Profile , Subject, StudyRequest , PartnerRequest  ,Friendship , Message , StudySession)

admin.site.register(Profile)
admin.site.register(Subject)
admin.site.register(StudyRequest)
admin.site.register(PartnerRequest)
admin.site.register(Friendship)
admin.site.register(Message)
admin.site.register(StudySession)