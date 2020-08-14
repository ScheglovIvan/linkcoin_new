from django.urls import path

from .views import *

urlpatterns = [
    path('/get_monthly_stats/<int:period>', get_monthly_stats),
    path('/get_weekly_stats/<int:year>/<int:month>/<int:day>', get_weekly_stats),
    path('/get_day_stats/<int:year>/<int:month>/<int:day>', get_day_stats)
]
