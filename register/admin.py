from django.contrib import admin

from .models import *

class AccountAdmin(admin.ModelAdmin):
    search_fields = ("email", "username", "date_joined",)
    list_filter = ("is_active", "special_user", "is_staff", "is_superuser")

class InvitationAdmin(admin.ModelAdmin):
    search_fields = ("inviter__email",)
    list_filter = ['date']

admin.site.register(User, AccountAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(PartnerProgram)
