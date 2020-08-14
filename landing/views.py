import datetime
import operator

from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from django.contrib.auth import get_user_model
from django.conf import settings

from register.models import Invitation, PartnerProgram
from user_profile.models import Payout, Payment, Ref_Link
from controlled_data.models import *
from counter.libs.decorators import newVisit
from counter.models import Visit
import requests


User = get_user_model()

def separate_with_comas(value):
    result = list(str(int(value)))

    length = len(result) - 1

    times = length // 3

    add = 0 if length % 2 else -1

    for i in range(1, times + 1):
        result.insert(i * 3 + add, ',')

    return ''.join(result)

@require_GET
def index(request):
    today = datetime.datetime.utcnow()

    if settings.USE_CONTROLLED_DATA:

        top_inviters = []

        for inviter in Leader.objects.all()[0:3]:
            leader = {
                "username": inviter.username,
                "total_click": inviter.total_click,
                "total_signup": inviter.total_signup,
                "total_purchase": inviter.total_purchase,
                "last_month_click": inviter.last_month_click,
                "last_month_signup": inviter.last_month_signup,
                "last_month_purchase": inviter.last_month_purchase,
                "monthly_free": inviter.monthly_free,
                "bonus": inviter.bonus,
                "avatar": inviter.avatar.url.split("static/")[1]
            }

            top_inviters.append(leader)

        payout_control = PayoutControl.objects.all()

        start_payout = 0 if not len(payout_control) else payout_control[0].amount

        payouts = Payout.objects.all()
        for item in payouts:
            start_payout += int(item.amount)


    payout = separate_with_comas(start_payout)

    # has_discount = False

    if request.user.is_authenticated:
        user_purchases = Payment.objects.filter(user__exact=request.user)
        inviter = Invitation.objects.filter(invited=request.user)

    #     if len(user_purchases) <= 0:
    #         if inviter:
    #             has_discount = True

    # elif 'ref' in request.GET:
    #     has_discount = True
        

    plan = Plan.objects.all()

    email = ''
    if request.user.is_authenticated:
        if len(request.user.email) > 22:
            email = request.user.email.split("@")[0]
        else:
            email = request.user.email

    response = render(request, 'landing/index.html', context={
        'top_inviters': top_inviters,
        'payout': payout,
        # 'has_discount': has_discount,
        "plan": plan,
        "email": email,
    })

    data = request.GET

    if 'ref' in data:
        ref_link = data['ref']

        try:
            ref_link = Ref_Link.objects.filter(ref_link=ref_link, active=True)
            if ref_link:
                ref_link = ref_link[0]

                newVisit(request, ref_link)

                inviter = ref_link.user
                
                iso_formatted_date = inviter.sub_active_till.isoformat()

                splitter = '.' if '.' in iso_formatted_date else '+'

                sub_active_till = datetime.datetime.strptime(iso_formatted_date.split(splitter)[0], '%Y-%m-%dT%H:%M:%S')

                difference = sub_active_till - datetime.datetime.utcnow()

                if difference.total_seconds() > 0:
                    max_age = 31536000
                    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
                    response.set_cookie('inviter', inviter.id, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE)
                    
                    if PartnerProgram.objects.filter(user=inviter):
                        partner = PartnerProgram.objects.filter(user=inviter)[0]
                        if partner.id_name in data:
                            response.set_cookie('clickId', str(data[partner.id_name]), max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE)

            else:
                return redirect("/")
        except:
            return redirect("/")

    return response


@require_GET
def generalInfo(request):
    if request.user.is_superuser == False:
        return redirect("/")

    users = User.objects.all()

    users_count = len(users)
    active_user_count = 0
    keep_money = 0

    for user in users:
        if user.is_active:
            active_user_count += 1

        keep_money += user.balance

    return render(request, 'general_info.html', context={
        "user_count": users_count,
        "keep_money": keep_money,
        "active_user_count": active_user_count,
    })

@require_GET
def paymentPage(request, plan):
    if request.user.is_authenticated == False:
        return redirect("/#prices")
        
    plan = Plan.objects.get(id=plan)

    # try:
    #     plan = Plan.objects.get(id=plan)

    #     user_purchases = Payment.objects.filter(user__exact=request.user)
    #     inviter = Invitation.objects.filter(invited=request.user)
        # if plan.name == "1 month linkcoin subscription" and plan.price < 29 and len(user_purchases) > 0:
        #     plan = Plan.objects.filter(name="1 month linkcoin subscription", price=29.99)[0]
        #     return redirect("/payment/plan/" + str(plan.id))

        # if plan.name == "1 month linkcoin subscription" and plan.price < 29 and not inviter:
        #     plan = Plan.objects.filter(name="1 month linkcoin subscription", price=29.99)[0]
        #     return redirect("/payment/plan/" + str(plan.id))
    # except:
    #     return redirect("/#prices")



    return render(request, 'payment/payment_page.html', context={
        "plan": plan,
    })


@require_GET
def policy(request, page_name):
    email = ''
    if request.user.is_authenticated:
        if len(request.user.email) > 22:
            email = request.user.email.split("@")[0]
        else:
            email = request.user.email

    refund = False
    cookie = False
    indemnification = False
    privacy = False
    terms = False
    questions = False
    if page_name == "refund":
        page = 'policy/policy_refund.html'
        refund = True
    elif page_name == "cookie":
        page = 'policy/policy_cookie.html'
        cookie = True
    elif page_name == "indemnification":
        page = 'policy/policy_indemnification.html'
        indemnification = True
    elif page_name == "privacy":
        page = 'policy/policy_privacy.html'
        privacy = True
    elif page_name == "terms":
        page = 'policy/policy_terms.html'
        terms = True
    elif page_name == "support":
        page = 'policy/support.html'
    elif page_name == "questions":
        page = 'policy/questions.html'
        questions = True
    else:
        return redirect("/policy/refund")


    return render(request, page, context={
        "email": email,
        "refund": refund,
        "cookie": cookie,
        "indemnification": indemnification,
        "privacy": privacy,
        "terms": terms,
        "questions": questions,
    })

