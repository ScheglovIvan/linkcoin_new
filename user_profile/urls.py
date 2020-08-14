from django.urls import path

from .views import *

urlpatterns = [
    path('', user_profile),
    path('/payment/linkcoin_balance', PayLinkcoinBalance),
    path('/payout_method/add', addPayoutMethod),
    path('/payout_method/remove', removePayoutMethod),
    path('/get_payout_method', getPayoutMethod),
    path('/payout', GetPayout),
    path('/create_ref_link', CreatRefLink),
]
