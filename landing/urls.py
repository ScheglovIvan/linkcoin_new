from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('policy/<str:page_name>', policy),
    path('general_info', generalInfo),
    path('payment/plan/<int:plan>', paymentPage),
]
