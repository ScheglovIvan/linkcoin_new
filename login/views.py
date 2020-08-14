from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, get_user_model
from django.conf import settings
from django.db import OperationalError

User = get_user_model()

@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == 'GET':
        return render(request, 'login/login.html')

    error_messages = []

    data = request.POST

    username = data['login-name']
    password = data['login-pass']

    try:
        user = User.objects.get(email=username)
    except (User.DoesNotExist, OperationalError):
        error_messages.append('User with the given email has not been found')
        return render(request, 'login/login.html', context={
            'error_messages': error_messages
        }, status=404)

    user = authenticate(username=user.username, password=password)

    if not user or not user.is_active:
        error_messages.append('Invalid password or your profile is inactive')

        return render(request, 'login/login.html', context={
            'error_messages': error_messages
        }, status=404)

    if not 'remember' in data:
        request.session.set_expiry(0)

    login(request, user)

    return redirect(settings.LOGIN_REDIRECT_URL)
    # return render(request, "login/login.html", status=200)
