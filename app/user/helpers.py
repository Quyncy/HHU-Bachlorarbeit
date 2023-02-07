"""
Hilfsfunktionen
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from core.models import *
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

import uuid
import string, secrets

def password_generator():
    letters = string.ascii_letters
    digits = string.digits
    special_char = string.punctuation

    alphabet = letters + digits + special_char  # Das komplette Alphabet

    password_length = 12

    pwd = ''
    for i in range(password_length):
        pwd += ''.join(secrets.choice(alphabet))

    return pwd


def send_password_mail(email, token):
    subject = 'HHU System - Passwort.'
    message = f'Willkommen im HHU System, mit dem folgenden Link können Sie ihr Passwort setzen: http://127.0.0.1:8000/change-password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


def setPassword(email):
    """ Funktion zum versenden des Passworts """

    try:
        if email:
            user = settings.AUTH_USER_MODEL.objects.get(email=email)
            token = str(uuid.uuid4())
            profile = Profile.objects.get(user=user)
            profile.token = token
            profile.save()
            send_password_mail(profile.user.email, token)
    except Exception as e:
        print(e)


def setPassword(request):
    try:
        User = get_user_model()
        if request.method == "POST":
            email = request.POST.get('email')

            user = User.objects.get(email=email)
            token = str(uuid.uuid4())
            # profile = Profile.objects.get(user=user)
            # profile.token = token
            # profile.token_is_valid = True

            # profile.save()
            # Email wird verschickt
            # send_password_mail(profile.user.email, token)

            messages.success(request, 'Die Email wurde versendet.')
            return redirect('set-password')

    except Exception as e:
        messages.success(request, 'Kein Benutzer mit dieser Email vorhanden')
        print(e)

    # ungefähr so. communication django frontend backend
    # payload = {'param1':1, 'param2':2}
    # r = request.post('https://domain.tld', data=payload)

    return render(request, 'user/set-password.html')
