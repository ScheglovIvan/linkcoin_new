from django.contrib import admin

from .models import *

admin.site.register(Leader, admin.ModelAdmin)
admin.site.register(PayoutControl, admin.ModelAdmin)
admin.site.register(Rank, admin.ModelAdmin)
admin.site.register(Plan, admin.ModelAdmin)
