from django.urls import path

from .views import *

urlpatterns = [
    # path('/payout', GetPayout),
    path('/create/order/<str:order_id>/<int:plan_id>', CreateOrder),
    path('/webhooks/subscription', subscription),
]
