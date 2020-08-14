from django.contrib import admin
from .models import Visit

class VisitAdmin(admin.ModelAdmin):
    search_fields = ('ref_link__ref_link', 'ref_link__user__email',)
    list_filter = ('date',)


admin.site.register(Visit, VisitAdmin)
