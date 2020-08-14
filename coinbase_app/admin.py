from django.contrib import admin
from .models import *

class CoinbaseOrderAdmin(admin.ModelAdmin):
    search_fields = ("user__email",)
    list_filter = ("plan",)



admin.site.register(CoinbaseOrder, CoinbaseOrderAdmin)
