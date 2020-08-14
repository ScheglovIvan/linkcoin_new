from django.urls import path

from .views import *

urlpatterns = [
    path('/create/order', Order),
    path('/webhooks/subscription/', subscription),
]
