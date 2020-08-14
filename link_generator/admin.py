from django.contrib import admin
from django.conf import settings

from .models import *

class LinkAdmin(admin.ModelAdmin):
    class Media:
        js = [ f'{settings.STATIC_URL}link_generator/js/link_generator.js' ]

admin.site.register(Link, LinkAdmin)
