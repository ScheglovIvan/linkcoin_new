from django.urls import path

from .views import *

urlpatterns = [
    path('', register),
    path('/activate/<email_code>', activate_account),
    path('/reset_password', send_code),
    path('/change_password/<email_code>', change_password),
    path('/is_authenticated/change_password', change_password_is_authenticated),
]
