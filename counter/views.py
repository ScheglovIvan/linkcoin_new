import datetime
import calendar

import dateutil.parser
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET

from .models import Visit
from user_profile.models import Payment, Payout, Ref_Link
from register.models import Invitation
from controlled_data.models import Plan

User = get_user_model()

def add_model_statistics(model, dates, type):
    if type == "devices":
        date = dateutil.parser.parse(model["date"].isoformat())
    else:
        date = dateutil.parser.parse(model.date.isoformat())
        
    if not "total" in dates:
        dates["total"] = {
            'clicks': 0,
            'purchases': 0,
            'signups': 0,
        }

    if not "devices" in dates:
        dates["devices"] = {
            'pc': 0,
            'mobile': 0,
            'tablet': 0,
        }

    if type != "devices":
        dates["date"][date.strftime("%Y-%m-%d")][type] += 1
        dates["total"][type] += 1
    else:
        for i in model:
            if i != "date":
                if model[i] > 0:
                    device_type = i 
        dates["devices"][device_type] += 1



@require_GET
@login_required
def get_monthly_stats(request, api_version, period):
    today = datetime.datetime.now() + datetime.timedelta(days=1)
    reg_date = request.user.date_joined
    max_range = (today - reg_date).days + 2

    if period == 1:
        days_count = datetime.datetime.now().day
    elif period > 10:
        days_count = max_range
    elif period > 1:
        days_count = datetime.datetime.now().day
        month = today.month
        for i in range(period):
            if month - (i + 1) <= 0:
                month = 12
            days_count += calendar.monthrange(today.year, month - (i + 1))[1]

    if days_count > max_range:
        days_count = max_range


    start_date = datetime.datetime.now() - datetime.timedelta(days=days_count)
    end_date = today

    if not request.is_ajax():
        return HttpResponse('User is not authenticated', status=403)
    
    data = request.GET
    # if request.user.ref_link:
    #     ref_link = request.user.ref_link
    # else:
    #     # Специально задаю несущестуещую ссылку
    #     ref_link = "!@#$%^^"

    # visits = Visit.objects.filter(ref_link=ref_link, date__range=(start_date, end_date))
    visits = Visit.objects.filter(user=request.user, date__range=(start_date, end_date))
    invitees = Invitation.objects.filter(inviter=request.user, date__range=(start_date, end_date))

    date = {
        "date": {},
        "total" : {
            'clicks': 0,
            'purchases': 0,
            'signups': 0,
        },
        "devices": {
            "pc": 0,
            "mobile": 0,
            "tablet": 0,
        }
    }

    date_iter = start_date + datetime.timedelta(days=1)
    stop_date = (end_date - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    while True:            
        date["date"][date_iter.strftime("%Y-%m-%d")] = {
            'clicks': 0,
            'purchases': 0,
            'signups': 0,
        }

        if date_iter.strftime("%Y-%m-%d") == stop_date:
            break

        date_iter = date_iter + datetime.timedelta(days=1)

    devices = {
        'pc': 0,
        'tablet': 0,
        'mobile': 0
    }

    for visit in visits:
        add_model_statistics(visit, date, 'clicks')

        devices[visit.device_type] += 1

        devices["date"] = visit.date
        add_model_statistics(devices, date, 'devices')

        devices[visit.device_type] = 0

        
    user_continue = []
    for invited in invitees:
        add_model_statistics(invited, date, 'signups')
        payments = Payment.objects.filter(user=invited.invited, date__range=(start_date, end_date), share=True)
        for payment in payments:
            if payment in user_continue:
                continue

            user_continue.append(payment)
            add_model_statistics(payment, date, 'purchases')

    return JsonResponse({
        'data': date,
    })


@login_required
@require_GET
def get_weekly_stats(request, api_version, year, month, day):
    if not request.is_ajax():
        return HttpResponse('', status=403)
        
    days = [
        {
            'clicks': 0,
            'signups': 0,
            'purchases': 0
        },
        {
            'clicks': 0,
            'signups': 0,
            'purchases': 0
        },
        {
            'clicks': 0,
            'signups': 0,
            'purchases': 0
        },
        {
            'clicks': 0,
            'signups': 0,
            'purchases': 0
        },
        {
            'clicks': 0,
            'signups': 0,
            'purchases': 0
        },
        {
            'clicks': 0,
            'signups': 0,
            'purchases': 0
        },
        {
            'clicks': 0,
            'signups': 0,
            'purchases': 0
        }
    ]

    start_date = datetime.datetime(year=year, month=month, day=day)
    end_date = start_date + datetime.timedelta(days=6)

    signups = User.objects.filter(date_joined__range=(start_date, end_date))
    purchases = Payment.objects.filter(date__range=(start_date, end_date), share=True)
    visits = Visit.objects.filter(date__range=(start_date, end_date))

    for signup in signups:
        date = dateutil.parser.parse(signup.date_joined.isoformat())
        days[date.weekday()]['signups'] += 1

    for purchase in purchases:
        date = dateutil.parser.parse(purchase.date.isoformat())
        days[date.weekday()]['purchases'] += 1

    for visit in visits:
        date = dateutil.parser.parse(visit.date.isoformat())
        days[date.weekday()]['clicks'] += 1

    return JsonResponse({
        'signups': list(signups.values()),
        'purchases': list(purchases.values()),
        'visits': list(visits.values()),
        'days': days
    })

@login_required
@require_GET
def get_day_stats(request, api_version, year, month, day):

    if not request.is_ajax():
        return HttpResponse('', status=403)

    user = request.user
    
    day_stats = []

    start_date = datetime.datetime(year, month, day)

    try:
        end_date = datetime.datetime(year, month, day+1)
    except:
        end_date = datetime.datetime(year, month+1, 1)


    visits = Visit.objects.filter(user=user, date__range=(start_date, end_date))
    totol_data = {
        "click": 0,
        "signup": 0,
        "purchase": 0
    }
    chart_day = {
        "click": [0, 0, 0, 0, 0, 0],
        "signup": [0, 0, 0, 0, 0, 0],
        "purchase": [0, 0, 0, 0, 0, 0],
    }

    # signups_black_list = []
    # payments_black_list = []
    # for visit in visits:
    #     new_visit = {
    #         "ip": visit.ip,
    #         "device": visit.device_type,
    #         "country": visit.country,
    #         "region": visit.region,
    #         "city": visit.city,
    #         "time": visit.date.strftime('%H:%M'),
    #         "type": "click"
    #     }
    #     totol_data["click"] += 1
    #     day_stats.append(new_visit)
        
    #     sort_hour = int(visit.date.strftime('%H'))
        
    #     if sort_hour >= 0 and sort_hour <= 4:
    #         chart_day["click"][0] += 1
    #     elif sort_hour >= 5 and sort_hour <= 8:
    #         chart_day["click"][1] += 1
    #     elif sort_hour >= 9 and sort_hour <= 12:
    #         chart_day["click"][2] += 1
    #     elif sort_hour >= 13 and sort_hour <= 16:
    #         chart_day["click"][3] += 1
    #     elif sort_hour >= 17 and sort_hour <= 20:
    #         chart_day["click"][4] += 1
    #     elif sort_hour >= 21 and sort_hour <= 24:
    #         chart_day["click"][5] += 1

    #     try:
    #         signups = Invitation.objects.filter(inviter=request.user, date__range=(start_date, end_date))
    #         for signup in signups:
    #             if signup in signups_black_list:
    #                 continue
    #             else:
    #                 signups_black_list.append(signup)
    #                 new_signup = {
    #                     "ip": visit.ip,
    #                     "device": visit.device_type,
    #                     "country": visit.country,
    #                     "region": visit.region,
    #                     "city": visit.city,
    #                     "time": signup.date.strftime('%H:%M'),
    #                     "type": "signup"
    #                 }
    #                 totol_data["signup"] += 1
    #                 day_stats.append(new_signup)

    #                 sort_hour = int(visit.date.strftime('%H'))
    #                 if sort_hour >= 0 and sort_hour <= 4:
    #                     chart_day["signup"][0] += 1
    #                 elif sort_hour >= 4 and sort_hour <= 8:
    #                     chart_day["signup"][1] += 1
    #                 elif sort_hour >= 9 and sort_hour <= 12:
    #                     chart_day["signup"][2] += 1
    #                 elif sort_hour >= 12 and sort_hour <= 16:
    #                     chart_day["signup"][3] += 1
    #                 elif sort_hour >= 17 and sort_hour <= 20:
    #                     chart_day["signup"][4] += 1
    #                 elif sort_hour >= 21 and sort_hour <= 24:
    #                     chart_day["signup"][5] += 1
    #                 try:
    #                     payments = Payment.objects.filter(user=signup.invited, status="completed", date__range=(start_date, end_date), share=True)
    #                     for payment in payments:
    #                         if payment in payments_black_list:
    #                             continue
    #                         else:
    #                             payments_black_list.append(payment)

    #                             amout = 10
    #                             if payment.amount == 7499:
    #                                 amout = 30
    #                             elif payment.amount == 23999:
    #                                 amout = 120

    #                             new_payment = {
    #                                 "ip": visit.ip,
    #                                 "device": visit.device_type,
    #                                 "country": visit.country,
    #                                 "region": visit.region,
    #                                 "city": visit.city,
    #                                 "time": payment.date.strftime('%H:%M'),
    #                                 "amout": amout,
    #                                 "type": "purchase"
    #                             }
    #                             totol_data["purchase"] += 1
    #                             day_stats.append(new_payment)

    #                             sort_hour = int(visit.date.strftime('%H'))
    #                             if sort_hour >= 0 and sort_hour <= 4:
    #                                 chart_day["purchase"][0] += 1
    #                             elif sort_hour >= 5 and sort_hour <= 8:
    #                                 chart_day["purchase"][1] += 1
    #                             elif sort_hour >= 9 and sort_hour <= 12:
    #                                 chart_day["purchase"][2] += 1
    #                             elif sort_hour >= 13 and sort_hour <= 16:
    #                                 chart_day["purchase"][3] += 1
    #                             elif sort_hour >= 17 and sort_hour <= 20:
    #                                 chart_day["purchase"][4] += 1
    #                             elif sort_hour >= 21 and sort_hour <= 24:
    #                                 chart_day["purchase"][5] += 1
    #                             break
    #                 except:
    #                     pass

    #                 break
    #     except:
    #         pass

    for visit in visits:
        new_visit = {
            "ip": visit.ip,
            "device": visit.device_type,
            "country": visit.country,
            "region": visit.region,
            "city": visit.city,
            "time": visit.date.strftime('%H:%M'),
            "type": "click"
        }
        totol_data["click"] += 1
        day_stats.append(new_visit)
        
        sort_hour = int(visit.date.strftime('%H'))
        
        if sort_hour >= 0 and sort_hour <= 4:
            chart_day["click"][0] += 1
        elif sort_hour >= 5 and sort_hour <= 8:
            chart_day["click"][1] += 1
        elif sort_hour >= 9 and sort_hour <= 12:
            chart_day["click"][2] += 1
        elif sort_hour >= 13 and sort_hour <= 16:
            chart_day["click"][3] += 1
        elif sort_hour >= 17 and sort_hour <= 20:
            chart_day["click"][4] += 1
        elif sort_hour >= 21 and sort_hour <= 24:
            chart_day["click"][5] += 1

        
    signups = Invitation.objects.filter(inviter=user, date__range=(start_date, end_date))
    for signup in signups:
        new_signup = {
            "ip": visit.ip,
            "device": visit.device_type,
            "country": visit.country,
            "region": visit.region,
            "city": visit.city,
            "time": signup.date.strftime('%H:%M'),
            "type": "signup"
        }
        totol_data["signup"] += 1
        day_stats.append(new_signup)

        sort_hour = int(visit.date.strftime('%H'))
        if sort_hour >= 0 and sort_hour <= 4:
            chart_day["signup"][0] += 1
        elif sort_hour >= 4 and sort_hour <= 8:
            chart_day["signup"][1] += 1
        elif sort_hour >= 9 and sort_hour <= 12:
            chart_day["signup"][2] += 1
        elif sort_hour >= 12 and sort_hour <= 16:
            chart_day["signup"][3] += 1
        elif sort_hour >= 17 and sort_hour <= 20:
            chart_day["signup"][4] += 1
        elif sort_hour >= 21 and sort_hour <= 24:
            chart_day["signup"][5] += 1

    signups = Invitation.objects.filter(inviter=user)
    for signup in signups:

        payments = Payment.objects.filter(user=signup.invited, status="completed", date__range=(start_date, end_date), share=True)
        for payment in payments:
            amout = 0

            if payment.share:               
                plan = payment.plan
                amout = int(plan.days / 30) * user.reward

                    
            new_payment = {
                "ip": visit.ip,
                "device": visit.device_type,
                "country": visit.country,
                "region": visit.region,
                "city": visit.city,
                "time": payment.date.strftime('%H:%M'),
                "amout": amout,
                "type": "purchase"
            }
                    
            totol_data["purchase"] += 1
            day_stats.append(new_payment)
                
            sort_hour = int(visit.date.strftime('%H'))
                
            if sort_hour >= 0 and sort_hour <= 4:
                chart_day["purchase"][0] += 1
            elif sort_hour >= 5 and sort_hour <= 8:
                chart_day["purchase"][1] += 1
            elif sort_hour >= 9 and sort_hour <= 12:
                chart_day["purchase"][2] += 1
            elif sort_hour >= 13 and sort_hour <= 16:
                chart_day["purchase"][3] += 1
            elif sort_hour >= 17 and sort_hour <= 20:
                chart_day["purchase"][4] += 1
            elif sort_hour >= 21 and sort_hour <= 24:
                chart_day["purchase"][5] += 1


    return JsonResponse({
        'day_stats': sorted(day_stats, key=lambda i: i["time"]),
        'total': totol_data,
        'chart': chart_day
    })