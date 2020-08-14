from django.urls import path

from .views import *

urlpatterns = [
    path('/subscribe/<int:plan_id>', subscribe),
    path('/webhooks/session_completed', session_complete),
    path('/webhooks/subscription_updated', subscription_updated)
]
