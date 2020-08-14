import string
import datetime
import urllib.parse

from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import DataError, IntegrityError
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.gis.geoip2 import GeoIP2

from django.core.mail import send_mail
from django.utils.html import strip_tags

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from .models import Invitation, PartnerProgram
from link_generator.models import Link
from counter.libs import client


from user_profile.models import Ref_Link

from random import choice
from string import ascii_uppercase

from django.template import loader

User = get_user_model()

geo_loc = GeoIP2()


@require_http_methods(['GET', 'POST'])
def send_code(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == 'GET':
        return render(request, 'register/send_code.html')
    else:
        data = request.POST

        try:
            user = User.objects.get(email=data['email'])
            if data['email'] == '':
                return render(request, 'register/send_code.html', context={
                    'errors': ['User with the given email has not been found']
                }, status=500)
        except User.DoesNotExist:
            return render(request, 'register/send_code.html', context={
                'errors': ['User with the given email has not been found']
            }, status=500)

        # difference = timezone.now() - user.last_sent_email

        # if difference.total_seconds() < 60:
        #     return render(request, 'register/send_code.html', context={
        #         'errors': ['Another email has been sent recently, please wait a minute before sending another one']
        #     })

        if not user.is_active:
            return render(request, 'register/send_code.html', context={
                'errors': ['User is not active, please verify your email first']
            })

        difference = user.code_active_till - timezone.now()

        user.email_code = user.generate_email_code(32)
        user.last_sent_email = timezone.now()
        user.code_active_till = timezone.now() + datetime.timedelta(hours=24)

        user.save()

        protocol = 'https' if request.is_secure() else 'http'

        current_site = get_current_site(request)

        html_message = loader.render_to_string('email_templates/email_template.html',
            {
                "type": "Reset password",
                "description": "To reset the password on the site, click on the button",
                "btn_name": "RESET PASSWORD",
                "URL": f'{protocol}://{current_site.domain}/register/change_password/{user.email_code}?email={user.email}',
            }
        )

        send_mail(
            'Reset password',
            f'Reset your password here: {protocol}://{current_site.domain}/register/change_password/{user.email_code}?email={user.email}',
            settings.EMAIL_HOST_USER,
            [user.email],
            html_message = html_message
        )
            
        return render(request, 'register/send_code.html', context={
            'statuses': [f'Instruction has been sent to your email ({user.email})']
        })

@require_http_methods(['GET', 'POST'])
def change_password(request, email_code):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == 'GET':
        data = request.GET

        if not 'email' in data:
            return HttpResponse(status=400)

        email = data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponse(status=404)

        if not user.is_active:
            return HttpResponse('User is not active, please verify your email first', status=400)

        if user.email_code != email_code:
            return HttpResponse(status=400)

        difference = user.code_active_till - timezone.now()
        
        if difference.total_seconds() <= 0:
            return HttpResponse('<a href="/login">Link is outdated, get a new one</a>', status=403)
        
        return render(request, 'register/change_password.html', context={
            'user_id': user.id
        })

    else:
        data = request.POST

        user = User.objects.get(id=data['user-id'])

        if data['new-pass'] != data['new-pass-conf'] or len(data['new-pass']) < 8:
            return render(request, 'register/change_password.html', context={
                'errors': ['Passwords didn\'t match']
            }, status=404)

        user.set_password(data['new-pass'])
        user.email_code = ''

        user.save()

        return redirect('/login')

@require_GET
def activate_account(request, email_code):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    data = request.GET

    if not 'email' in data:
        return HttpResponse(status=400)

    email = data['email']

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if user.email_code != email_code:
        return HttpResponse(status=400)

    user.is_active = True
    user.email_code = ''

    user.save()

    return redirect('/login')


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    context = {
        'LOGIN_URL': settings.LOGIN_URL,
        'error_messages': []
    }

    if request.method == 'GET':
        return render(request, 'register/register.html', context=context)

    data = request.POST

    email = data['reg-email']

    error_messages = context['error_messages']

    if not 'terms' in data:
        error_messages.append('You must accept the terms')

    try:
        users = User.objects.get(email=email)
        error_messages.append('Email is already taken')
        return render(request, 'register/register.html', status=400)
    except User.DoesNotExist:
        pass

# Обработка ошибок
    if len(data["reg-email"]) < 5:
        return render(request, 'register/register.html', status=401)
    elif len(data["reg-pass"]) < 8:
        return render(request, 'register/register.html', status=402)
    elif data["reg-pass-repeat"] != data["reg-pass"]:
        return render(request, 'register/register.html', status=403)

    try: 
        if data['terms']:
            pass
    except:
        return render(request, 'register/register.html', status=404)



    if data['reg-pass'] != data['reg-pass-repeat']:
        error_messages.append('Passwords must be identic')

    try:
        validate_email(data['reg-email'])
    except ValidationError as e:
        error_messages.append(e.message)

    if len(error_messages):
        return render(request, 'register/register.html', context=context)

    user_ip = client.get_client_ip(request)

    try:
        geo_data = geo_loc.city(user_ip)

        country = geo_data.get('country_name', '')
        region = geo_data.get('region', '')
        city = geo_data.get('city', '')

        country_code = geo_data.get('country_code', '')

    except Exception:
        country = region = city = ''
        country_code = 'US'

    try:
        requested_capabilities = ['transfers']

        if country_code != 'US':
            requested_capabilities.append('card_payments')

    except Exception as e:
        error_messages.append(str(e))
        return render(request, 'register/register.html', context=context)

    try:
        username = email.split("@")[0]
        user = User.objects.create_user(username=username, email=email, password=data['reg-pass'], ip=user_ip)
    except DataError:
        error_messages.append(e.args[1])

    if len(error_messages):
        return render(request, 'register/register.html', context=context)

    user.save()

    user_id = user.id

    letters = string.ascii_letters

    total_letters = len(letters)


    Ref_Link.create(user=user)
    user.country = country
    user.region = region
    user.city = city

    user.is_active = False

    user.email_code = user.generate_email_code(32)

    protocol = 'https' if request.is_secure() else 'http'

    current_site = get_current_site(request)

    parsed_uri = urllib.parse.urlparse(request.get_raw_uri())

    if len(parsed_uri.query) > 5:
        params = parsed_uri.query.split('&')

        for param in params:
            key, value = param.split('=')

            if key != 'link':
                continue

            try:
                link = Link.objects.get(value=value)
                user.sub_active_till = datetime.datetime.max
                user.special_user = True
                link.delete()
            except Link.DoesNotExist:
                pass

    cookies = request.COOKIES
    
    clickId = cookies.get('clickId')

    if clickId:
        user.pp_user_id = clickId

    user.save()

    html_message = loader.render_to_string('email_templates/email_template.html',
        {
            "type": "COMPLETION OF REGISTRATION",
            "description": "To confirm registration on the site, click on the button",
            "btn_name": "CONFIRM EMAIL",
            "URL": f'{protocol}://{current_site.domain}/register/activate/{user.email_code}?email={user.email}',
        }
    )

    send_mail(
        'Activation link',
        f'Your activation link: {protocol}://{current_site.domain}/register/activate/{user.email_code}?email={user.email}',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
        html_message = html_message
    )

    inviter_id = cookies.get('inviter')

    if inviter_id:
        try:
            inviter = User.objects.get(id=inviter_id)
            
            if inviter.get_sub_exp_time()['active']:
                invitation = Invitation()
                invitation.inviter = inviter
                invitation.invited = user
                invitation.save()

                inviter.users_invited += 1

                inviter.save()

                if PartnerProgram.objects.filter(user=inviter):
                    partner = PartnerProgram.objects.filter(user=inviter)[0]
                    partner.sendData(clickId, "register")

        except User.DoesNotExist:
            pass

    return redirect('/login')

@csrf_exempt
@require_POST
def change_password_is_authenticated(request):
    data = request.POST

    old_pass = data["old_pass"]
    new_pass = data["new_pass"]
    reply_new_pass = data["reply_new_pass"]

    user = request.user
    user = authenticate(username=user.username, password=old_pass)

    if not old_pass or not new_pass or not reply_new_pass:
        return HttpResponse(status=400)

    if not user or not user.is_active:
        return HttpResponse(status=401)
    
    if new_pass != reply_new_pass:
        return HttpResponse(status=402)

    if len(new_pass) < 8:
        return HttpResponse(status=403)

    user.set_password(new_pass)
    user.save()
    
    return HttpResponse(status=200)
