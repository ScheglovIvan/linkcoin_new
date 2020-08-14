import json
import time
import datetime

from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import stripe

from .models import Plan
from register.models import Invitation
from user_profile.models import Transaction

stripe.api_key = settings.STRIPE_API_KEY

User = get_user_model()

@csrf_exempt
@require_POST
def subscription_updated(request):
    payload = request.body

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError:
        return HttpResponse(status=400)

    if event.type != 'customer.subscription.updated':
        return HttpResponse(status=400)

    data = event.data.object

    try:
        # user = User.objects.get(stripe_user_id=data.customer)
        users = User.objects.filter(stripe_user_id=data.customer)
        for i in users:
            user = i
            break

    except User.DoesNotExist:
        return HttpResponse(status=400)


    plan = data['items']['data'][0]['plan']

    months = plan['interval_count']


    if plan['interval'] == 'year':
        months *= 12

    user.renew_subscription(months)

    subs = list(stripe.Subscription.list(customer=user.stripe_user_id, status='active'))

    subs.reverse()

    for index, sub in enumerate(subs):
        if index + 1 == len(subs):
            break

        sub_id = sub['id']

        stripe.Subscription.delete(sub_id)


    try:
        today = datetime.datetime.now()

        invitation = Invitation.objects.get(invited=user)

        inviter = invitation.inviter
        
        if inviter.sub_active_till.date() >= today.date():
            inviter.balance += settings.REWARD * months
            inviter.save()

    except Invitation.DoesNotExist:
        pass

    transaction = Transaction()
    transaction.currency = 'USD'
    transaction.amount = plan['amount']
    transaction.status = 'completed'
    transaction.stripe_id = event['id']
    transaction.type = 'charge'
    transaction.user = user

    transaction.save()
    return HttpResponse(status=200)

@csrf_exempt
@require_POST
def session_complete(request):
    payload = request.body

    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.SESSION_COMPLETE_SECRET)
    except ValueError:
        return HttpResponse(status=422)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=403)

    if event['type'] != 'checkout.session.completed':
        return HttpResponse(status=400)

    time.sleep(10)

    return HttpResponse(status=200)

@login_required
def subscribe(request, plan_id):
    try:
        plan = Plan.objects.get(id=plan_id)
    except Plan.DoesNotExist:
        return redirect('/#prices')

    current_site = get_current_site(request)

    protocol = 'https' if request.is_secure() else 'http'

    session = stripe.checkout.Session.create(
      payment_method_types=['card'],
      client_reference_id=request.user.id,
      customer=request.user.stripe_user_id,
      subscription_data={
        'items': [{
          'plan': plan.plan_id
        }]
      },
      metadata={
        'plan_id': plan.plan_id
      },
      success_url=f'{protocol}://{current_site.domain}' + '/profile?session_id={CHECKOUT_SESSION_ID}',
      cancel_url=f'{protocol}://{current_site.domain}/#prices',
    )

    return render(request, 'stripe_app/pay.html', context={
        'STRIPE_API_TOKEN': settings.STRIPE_API_TOKEN,
        'session_id': session['id']
    })
