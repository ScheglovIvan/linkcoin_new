import datetime
import operator
import json

from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_datetime
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from controlled_data.models import Rank
from register.models import Invitation, PartnerProgram
from .models import Payout, Payment, PayoutMethod, Ref_Link
from paypal_app.views import PaypalPayout
from coinbase_app.views import CoinbasePayout

from controlled_data.models import Plan

User = get_user_model()

@login_required
@require_http_methods(['GET', 'POST'])
def user_profile(request):
    current_site = get_current_site(request)

    user = request.user


    email = user.email.split("@")[0] if len(user.email) > 22 else user.email

    sub_data = user.get_sub_exp_time()

    error_messages = []

    if request.method == 'POST':
        data = request.POST

        email = data['email']

        try:
            validate_email(email)
        except ValidationError:
            error_messages.append('Invalid email address')

        try:
            second_user = User.objects.get(email=email)
            if second_user.id != user.id:
                error_messages.append('Email is taken')
        except User.DoesNotExist:
            if not len(error_messages):
                user.change_email(email)

        password = data['password']

        if len(password) and len(password) < User.password.field.max_length:
            user.set_password(password)
        else:
            error_messages.append('Invalid password length')

        user.save()

        login(request, user)

    elif 'error_message' in request.GET:
        error_messages.append(request.GET['error_message'])

    avatar_url = user.get_avatar_url()

    today = datetime.datetime.utcnow()
    
    invitations = Invitation.objects.filter(date__year=today.year, date__month=today.month, inviter=request.user)

    try:
        today = datetime.datetime.now()
        # today = datetime.datetime(2020, 4, 26)

        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        # today_str = datetime.datetime(2020, 4, 26).strftime("%Y-%m-%d")

        week_day = datetime.datetime.strptime(today_str, '%Y-%m-%d').isoweekday() - 1

        days = ["mon","tue","wed","thu","fri","sat","sun"]
        btn_date = {"mon": "","tue": "","wed": "","thu": "","fri": "","sat": "","sun": ""}
        today_bar = {"mon": "","tue": "","wed": "","thu": "","fri": "","sat": "","sun": ""}

        i = 0
        search_bar = True
        while(True):
            btn_date[days[week_day]] = (today - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            i += 1
            week_day -= 1
            if search_bar:
                today_bar[days[week_day+1]] = "today-bar-stat"
                search_bar = False
            if(week_day < 0):
                break

        # inviters = {}


        # for invitation in invitations:
        #     inviter = invitation.inviter
        #     inviter_id = inviter.id

        #     if inviter_id in inviters:
        #         inviters[inviter_id] += 1
        #     else:
        #         inviters[inviter_id] = 1

        # sorted_inviters = sorted(inviters.items(), key=operator.itemgetter(1))
        # sorted_inviters.reverse()
        # print(invitations)
        # sorted_inviters = [ inviter[0] for inviter in sorted_inviters ]

        # rank = sorted_inviters.index(user.id)
        rank = user.id
        

    except Invitation.DoesNotExist:
        rank = User.objects.count()

    try:
        controlled_rank = Rank.objects.get(id=1)
        add_to_rank = controlled_rank.add
    except Rank.DoesNotExist:
        add_to_rank = 0

    rank += add_to_rank


    total_earned = 0
    subscriber = user.users_invited

    invitations = Invitation.objects.filter(inviter=request.user)
    for invitation in invitations:
        payments = Payment.objects.filter(user=invitation.invited, share=True)
        for payment in payments:
          total_earned += int(int(payment.plan.days / 30) * user.reward)


    payout_methods = PayoutMethod.objects.filter(user=user, active=True)
    height_counter = 0
    for i in payout_methods:
        height_counter += 106
    # payout_method_window_height = str(214 + height_counter) + 'px'
    payout_method_window_height = str(278 + height_counter) + 'px'

    if user.special_user:
        sub_data['days'] = sub_data['days'] % 100

    ref_links = Ref_Link.objects.filter(user=user, active=True)

    height_ref_link_settings = 161
    for i in ref_links:
      height_ref_link_settings += 58

    return render(request, 'user_profile/profile.html', context={
        'current_site': current_site,
        'error_messages': error_messages,
        'sub_data': sub_data,
        'avatar_url': avatar_url,
        'rank': rank,
        "btn_date": btn_date,
        "today_bar": today_bar,
        "email": email,
        "total_earned": total_earned,
        "subscriber": subscriber,
        "payout_methods": payout_methods,
        "payout_method_window_height": payout_method_window_height,
        "total_payout": user.balance - 1.50,
        "ref_links": ref_links,
        "height_ref_link_settings": height_ref_link_settings,
    })

@login_required
@require_POST
def PayLinkcoinBalance(request):
    data = request.POST

    try:
        plan = Plan.objects.filter(id=data["plan"])[0]
    except:
        return HttpResponse(status=400)

    user = request.user

    if User.PayLinkcoinBalance(id=user.id, days=plan.days, price=plan.price):
        payment = Payment()
        payment.amount = plan.price
        payment.currency = "USD"
        payment.status = "completed"
        payment.user = user
        payment.plan = plan
        payment.method = "Linkcoin balance"

        try:
            invitation = Invitation.objects.filter(invited=user)[0]

            months_count = int(plan.days / 30)

            if User.getReward(invitation.inviter.id, months_count):
                payment.share = True

        except:
            pass
        
        payment.save()

        if PartnerProgram.objects.filter(user=invitation.inviter):
          clickId = user.pp_user_id
          partner = PartnerProgram.objects.filter(user=invitation.inviter)[0]
          partner.sendData(clickId, "buy")
        
        return HttpResponse(status=200)


@csrf_exempt
@require_POST
def addPayoutMethod(request):
  user = request.user
  data = request.POST

  method = data["payout_method"]
  recipient = data["recipient"]
  confirm_recipient = data["confirm_recipient"]

  if len(recipient) < 7:
    return HttpResponse(status=400)

  if recipient != confirm_recipient:
    return HttpResponse(status=401)

  methods = PayoutMethod.objects.filter(user=user, name=method, recipient=recipient, active=True)
  if not methods:
    if "@" in recipient or "." in recipient:
      recipient_type = "email"
    else:
      recipient_type = "phone"
    
    payout_method = PayoutMethod()

    payout_method.name = method
    payout_method.user = user
    payout_method.recipient_type = recipient_type
    payout_method.recipient = recipient
    payout_method.name = method

    methods = PayoutMethod.objects.filter(user=user, active=True)
    if not methods:
      payout_method.default = True

    payout_method.save()
    return HttpResponse(status=200)
  else:
    return HttpResponse(status=402)

@csrf_exempt
@require_POST
def removePayoutMethod(request):
  if not request.is_ajax():
    return HttpResponse('User is not authenticated', status=403)
  
  user = request.user
  data = request.POST

  recipient = data["recipient"]
  method = data["method"]

  try:
    payout_method = PayoutMethod.objects.filter(user=user, name=method, recipient=recipient, active=True)[0]
    
    payout_method.active = False
    payout_method.save()

    if payout_method.default:
      payout_methods = PayoutMethod.objects.filter(user=user, active=True)
      if not payout_methods == False:
        method = payout_methods[0]
        method.default = True
        method.save()

    return HttpResponse(status=200)
  except:
    return HttpResponse(status=400)

@require_GET
def getPayoutMethod(request):
  payout_methods = PayoutMethod.objects.filter(user=request.user, active=True)

  data = []
  for payout_method in payout_methods:
    method = {
      "name": payout_method.name,
      "recipient": payout_method.recipient,
      "default": payout_method.default,
    }
    data.append(method)
  
  return JsonResponse({
        'data': data,
    })

@csrf_exempt
@require_POST
@transaction.atomic
def GetPayout(request):
  if not request.is_ajax():
    return HttpResponse('User is not authenticated', status=400)
    
  user = request.user

  if user.balance <= 0:
    return HttpResponse(status=401)

  data = request.POST

  method = data["method"]
  recipient = data["recipient"]
  
  try:
    payout_method = PayoutMethod.objects.filter(user=user, name=method, recipient=recipient, active=True)[0]
  except:
    return HttpResponse(status=402)

  if payout_method.name == "PayPal" or payout_method.name == "Venmo":
    payout_func = PaypalPayout
  elif payout_method.name == "BTC":
    payout_func = CoinbasePayout
  else:
    payout_func = lambda *args, **kwargs: False

  currency = "USD"

  payout_response = User.payout(id=user.id, payout_method=payout_method, payout_func=payout_func)

  if payout_response == True:
    payout = Payout.create(amount=user.balance, currency=currency, status="complated", user=user, method=payout_method)

    return HttpResponse(status=200)

  return payout_response


@csrf_exempt
@require_POST
def CreatRefLink(request):
  user = request.user

  if len(Ref_Link.objects.filter(user=user, active=True)) >= 3:
    return HttpResponse(status=400)

  EN_SYMBOL = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
  ref_link = request.POST["ref_link"]

  if not ref_link:
    return HttpResponse(status=401)

  for char in ref_link:
    if char in EN_SYMBOL:
      pass
    else:
      return HttpResponse(status=402)

  search_ref_link = Ref_Link.objects.filter(ref_link=ref_link, active=True)
  if not search_ref_link:
    if Ref_Link.create(user=user, ref_link=ref_link):
      return HttpResponse(status=200)

  return HttpResponse(status=403)