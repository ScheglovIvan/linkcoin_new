from django.contrib import admin

from .models import *

class PayoutAdmin(admin.ModelAdmin):
    search_fields = ("user__email",)
    list_filter = ("method__name",)

class PaymentAdmin(admin.ModelAdmin):
    search_fields = ("user__email", "amount",)
    list_filter = ("share", "amount",)

class PayoutMethodAdmin(admin.ModelAdmin):
    search_fields = ("user__email",)
    list_filter = ("active", "name",)

class Ref_LinkAdmin(admin.ModelAdmin):
    search_fields = ("user__email", "ref_link",)
    list_filter = ("active",)

admin.site.register(Ref_Link, Ref_LinkAdmin)
admin.site.register(PayoutMethod, PayoutMethodAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Payout, PayoutAdmin)
