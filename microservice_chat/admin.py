from django.contrib import admin
from microservice_chat.models import User, Profile, ChatMessage

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id_origin', 'name', 'last_name']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name' ,'image']

class ChatMessageAdmin(admin.ModelAdmin):
    list_editable = ['is_read', 'message']
    list_display = ['user','sender', 'receiver', 'is_read', 'message']

admin.site.register( User, UserAdmin)
admin.site.register( Profile,ProfileAdmin)
admin.site.register( ChatMessage,ChatMessageAdmin)