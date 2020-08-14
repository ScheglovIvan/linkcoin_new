import json
import time
import datetime

from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.db import transaction

from .models import Order
from controlled_data.models import Plan


from register.models import Invitation, PartnerProgram
from user_profile.models import Payment, Payout, PayoutMethod

import paypalrestsdk

User = get_user_model()


paypalrestsdk.configure({
  'mode': settings.PAYPAL_MODE,
  'client_id': settings.PAYPAL_CLIENT_ID,
  'client_secret': settings.PAYPAL_SECRET_KEY
  })
paypal = paypalrestsdk


@csrf_exempt
@require_POST
def subscription(request):
  try:
    data = json.loads(request.body)

    order_id = data["resource"]["id"]
    order = Order.objects.filter(order_id=order_id)[0]

    if order:
      plan = order.plan
      user = order.user

      user.renew_subscription(days=plan.days)

      payment = Payment()
      payment.amount = plan.price
      payment.currency = "USD"
      payment.status = "completed"
      payment.user = user
      payment.plan = plan
      payment.method = "PayPal"

      try:
        invitation = Invitation.objects.filter(invited=user)[0]

        months_count = ((plan.days - (plan.days % 10)) / 30)

        if User.getReward(invitation.inviter.id, months_count):
          payment.share = True

        if PartnerProgram.objects.filter(user=invitation.inviter):
          clickId = user.pp_user_id
          partner = PartnerProgram.objects.filter(user=invitation.inviter)[0]
          partner.sendData(clickId, "buy")

      except:
        pass
        
      payment.save()

    else:
      return HttpResponse(status=400)

    return HttpResponse(status=200)
  except:
    return HttpResponse(status=400)

@csrf_exempt
@require_POST
def CreateOrder(request, order_id, plan_id):
  try:
    plan = Plan.objects.filter(id=plan_id)[0]

    order = Order()
    order.order_id = order_id
    order.user = request.user
    order.plan = plan
    order.save()
    
    return HttpResponse(status=200)
  except:
    return HttpResponse(status=400)

def PaypalPayout(payout_method, balance):
  recipient_wallet = payout_method.name

  if payout_method.recipient_type == "email":
    recipient_type = "EMAIL"
  elif payout_method.recipient_type == "phone":
    recipient_type = "PHONE"

  currency = "USD"
  recipient = payout_method.recipient

  paypalrestsdk.configure({
    'mode': settings.PAYPAL_MODE,
    'client_id': settings.PAYPAL_CLIENT_ID,
    'client_secret': settings.PAYPAL_SECRET_KEY
    })
  
  paypal = paypalrestsdk
  
  payout = paypal.Payout({
    "sender_batch_header": {
      "email_subject": "Thank you for continuing to work with linkcoin, it is very important for us"
      },
      "items": [{
        "recipient_type": recipient_type,
        "amount": {
          "value": balance,
          "currency": currency
          },
          "receiver": recipient,
          "note": "Thank you for continuing to work with linkcoin, it is very important for us",
          "recipient_wallet": recipient_wallet
          }]
  })

  if payout.create(sync_mode=False):
    return True
  
  return False
  
