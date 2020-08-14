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

from .models import *
from controlled_data.models import Plan


from register.models import Invitation, PartnerProgram
from user_profile.models import Payment, Payout, PayoutMethod

from coinbase_commerce.client import Client as CommerceClient

import requests
import hmac, hashlib
from requests.auth import AuthBase


commerce_client = CommerceClient(settings.COMMERCE_COINBASE_API_KEY)

@csrf_exempt
@require_POST
def subscription(request):
    data = json.loads(request.body)

    # print(data["event"]["data"]["payments"][0]["value"]["crypto"]["currency"])
    event_type = data['event']['type']
    if event_type == "charge:confirmed" or event_type == "charge:delayed":

        status = data["event"]["data"]["payments"][0]["status"]
        if status == "CONFIRMED" or status == "DELAYED":
            pass
        else:
            return HttpResponse(status=400)

        try:
            order = CoinbaseOrder.objects.filter(order_id=data["event"]["data"]["id"])[0]
            # order = CoinbaseOrder.objects.filter(order_id="06bcc595-dbc5-4f36-93a1-522992dd193c")[0]
            if order.paid == False:
                user = order.user
                plan = order.plan

                user.renew_subscription(days=plan.days)

                payment = Payment()
                payment.amount = plan.price
                payment.currency = data["event"]["data"]["payments"][0]["value"]["crypto"]["currency"]
                payment.status = "completed"
                payment.user = user
                payment.plan = plan
                payment.method = "Coinbase"

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
                order.paid = True
                order.save()
            else:
                return HttpResponse(status=400)
        except:
            return HttpResponse(status=400)

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


@csrf_exempt
@require_POST
def Order(request):
    data = request.POST

    try:
        plan = Plan.objects.filter(id=data["plan"])[0]

        charge_info = {
            "name": plan.name + " subscription to thelinkcoin.com",
            # "description": "Linkcoin LLC",
            "local_price": {
                "amount": plan.price,
                "currency": "USD"
            },
            "pricing_type": "fixed_price"
        }
        
        charge = commerce_client.charge.create(**charge_info)

        order = CoinbaseOrder()
        order.user = request.user
        order.order_id = charge.id
        order.plan = plan
        order.save()
        
        return HttpResponse(charge.hosted_url, status=200)
    except:
        return HttpResponse(status=400)


# Before implementation, set environmental variables with the names API_KEY and API_SECRET
API_KEY = settings.COINBASE_API_KEY
API_SECRET = settings.COINBASE_SECRET_KEY

# Create custom authentication for Coinbase API
class CoinbaseWalletAuth(AuthBase):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
        timestamp = str(requests.get("https://api.coinbase.com/v2/time").json()['data']['epoch'])

        if request.body == None:
            req_body = ''
        else:
            req_body = str(request.body, 'utf-8')

        message = timestamp + request.method + request.path_url + req_body
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()

        
        request.headers.update({
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-VERSION': datetime.datetime.now().strftime("%Y-%m-%d")
        })
        return request


def CoinbasePayout(payout_method, balance):
    api_url = 'https://api.coinbase.com/v2/'
    auth = CoinbaseWalletAuth(API_KEY, API_SECRET)

    # r = requests.get(api_url + 'user', auth=auth)
    # print(r.json())
    btc_rate = requests.get('https://api.coinbase.com/v2/exchange-rates?currency=BTC').json()['data']['rates']['USD']
    amount = str(float('{:.7f}'.format(1 / (float(btc_rate) / balance))))
    
    tx = {
        "type": "send",
        "to": payout_method.recipient,
        "amount": amount,
        "currency": "BTC",
    }

    try:
        r = requests.post(api_url + 'accounts/primary/transactions', json=tx, auth=auth)

        if r.json()["errors"]:
            # message = r.json()["errors"][0]["message"]
            # if message == "У вас нет столько средств.":
            #     print(400)
            #     pass
            
            # if message == "Введите допустимый адрес электронной почты или Биткойн-адрес":
            #     print(401)
            #     pass

            return False

        if r.json()['data']['status'] == 'pending' or r.json()['data']['status'] == 'completed':
            return True
        else:
            return False
    except:
        return False