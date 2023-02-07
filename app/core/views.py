from django.shortcuts import render

from .forms import (
    DozentForm,
    BlattForm,
    KursleiterForm,
    TutorForm,
    LoginForm,
    KursForm
)

import requests
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model,login,logout
from core.auth import EmailBackend
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth


@login_required(login_url='/login')
def Index(request):
    return render(request, 'user/index.html')


@csrf_protect
def loginPage(request):
    form = LoginForm()
    
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = auth.authenticate(
                    username=form.cleaned_data["email"],
                    password=form.cleaned_data["password"])
            auth.login(request, user)
            return redirect('index')
        else:
            print('NO')
            form = LoginForm()

    return render(request, 'user/login.html', {'form':form})


# def loginPage(request):
#     if request.method == 'POST':
#             email = request.POST.get('email')
#             password = request.POST.get('password')

#             backend = EmailBackend()
#             user = backend.authenticate(request=request, username=email , password=password)
#             print('view.py: '+str(user))
#             print('User:')
#             print(user)
#     ##################!!!!!!!!!!!!!!!!!!!!!!            ##################
#             # login(request, user, 'apps.core.api.backeds.EmailAuthBackend')
#             login(request, user)

#             return redirect('index')
#             # try:
#             #     return redirect('index')
#             # except:
#             #     messages.success(request, 'Email oder Passwort falsch.')

#     context = {}
#     return render(request , 'user/login.html', context)

############################
from django.shortcuts import render, redirect
from .forms import UserCreateForm

from django.contrib.auth.hashers import make_password

def createUser(request):
    form = UserCreateForm()

    if request.POST:
        url = 'http://127.0.0.1:8000/api/user/create-user/'
        form = UserCreateForm(request.POST)

        if form.is_valid():
            payload={
                'email':form.cleaned_data['email'],
                'vorname':form.cleaned_data['vorname'],
                'nachname':form.cleaned_data['nachname'],
                'rolle':form.cleaned_data['rolle'],
                'is_active':form.cleaned_data['is_active'],
                'is_staff':form.cleaned_data['is_staff'],
                'is_superuser':form.cleaned_data['is_superuser'],
                'password': make_password(form.cleaned_data['password1']),
            }
            print(payload)
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                return Response(status=status.HTTP_201_CREATED)
    return render(request, 'user/form.html', {'form': form})


def createKursleiter(request):
    kursleiter_form = KursleiterForm()
    
    if request.POST:
        kursleiter_form = KursleiterForm(request.POST)
        url = 'http://127.0.0.1:8000/api/user/create-kursleiter/'

        if kursleiter_form.is_valid():
            password = str(uuid)
            payload = {
                'email': kursleiter_form.cleaned_data['email'],
                'vorname': kursleiter_form.cleaned_data['vorname'],
                'nachname': kursleiter_form.cleaned_data['nachname'],
                'rolle': 'Kursleiter',
                'is_active': kursleiter_form.cleaned_data['is_active'],
                'is_staff':kursleiter_form.cleaned_data['is_staff'],
                'is_superuser': kursleiter_form.cleaned_data['is_superuser'],
                # 'groups': kursleiter_form.cleaned_data['groups'],
                # 'user_permissions': kursleiter_form.cleaned_data['user_permissions'],
                'password': make_password(password),
            }
            print(payload)

            response = requests.post(url, data=payload)
            
            if response.status_code == 200:
                return Response("Kursleiter erfolreich gespeichert.", status=status.HTTP_200_OK)

    context={'form': kursleiter_form, }
    return render(request, 'user/createkursleiter.html', context)

import uuid 
def createTutor(request):
    tutor_form = TutorForm()
    
    if request.POST:
        tutor_form = TutorForm(request.POST)
        url = 'http://127.0.0.1:8000/api/user/create-tutor/'

        if tutor_form.is_valid():
            password = str(uuid)
            payload = {
                'email': tutor_form.cleaned_data['email'],
                'vorname': tutor_form.cleaned_data['vorname'],
                'nachname': tutor_form.cleaned_data['nachname'],
                'rolle': 'Tutor',
                'is_active': tutor_form.cleaned_data['is_active'],
                'is_staff':tutor_form.cleaned_data['is_staff'],
                'is_superuser': tutor_form.cleaned_data['is_superuser'],
                # 'groups': tutor_form.cleaned_data['groups'],
                # 'user_permissions': tutor_form.cleaned_data['user_permissions'],
                'password': make_password(password),
            }
            print(payload)

            response = requests.post(url, data=payload)
            
            if response.status_code == 200:
                return Response("Tutor erfolreich gespeichert.", status=status.HTTP_200_OK)

    context={'form':tutor_form, }
    return render(request, 'user/createtutor.html', context)


def createDozent(request):
    dozent_form = DozentForm()
    
    if request.POST:
        dozent_form = DozentForm(request.POST)
        url = 'http://127.0.0.1:8000/api/user/create-dozent/'

        if dozent_form.is_valid():
            password = str(uuid)
            payload = {
                'email': dozent_form.cleaned_data['email'],
                'vorname': dozent_form.cleaned_data['vorname'],
                'nachname': dozent_form.cleaned_data['nachname'],
                'rolle': 'Dozent',
                'is_active': dozent_form.cleaned_data['is_active'],
                'is_staff':dozent_form.cleaned_data['is_staff'],
                'is_superuser': dozent_form.cleaned_data['is_superuser'],
                # 'groups': dozent_form.cleaned_data['groups'],
                # 'user_permissions': dozent_form.cleaned_data['user_permissions'],
                'password': make_password(password),
            }
            print(payload)

            response = requests.post(url, data=payload)
            
            if response.status_code == 200:
                return Response("Dozent erfolreich gespeichert.", status=status.HTTP_200_OK)

    context={'form':dozent_form, }
    return render(request, 'user/createdozent.html', context)


############################
def createKurs(request):
    kurs_form = KursForm()

    if request.POST:
        kurs_form = KursForm(request.POST)
        url = 'http://127.0.0.1:8000/api/kurs/create-kurs/'

        if kurs_form.is_valid():
            payload={
                'kurs': kurs_form.cleaned_data['kurs'],
                'beschreibung': kurs_form.cleaned_data['beschreibung'],
                'ref_id': kurs_form.cleaned_data['ref_id'],
            }
            print(payload)
            response = requests.post(url, data=payload)
            if response.status_code ==200:
                return Response(status=status.HTTP_201_CREATED)

    context={'form': kurs_form}
    return render(request, 'user/createkurs.html', context)


def createBlatt(request):
    blatt_form = BlattForm

    if request.POST:
        blatt_form = BlattForm(request.POST)
        url = 'http://localhost:8000/api/kurs/create-blatt/'

        if blatt_form.is_valid():
            payload = {
                'ass_name': blatt_form.cleaned_data['ass_name'],
                'ass_id': blatt_form.cleaned_data['ass_id'],
                'kurs': blatt_form.cleaned_data['kurs'].id,
            }

            response = requests.post(url, data=payload)
            if response.status_code == '200':
                return Response(status=status.HTTP_200_OK)
    
    context={'form': blatt_form, }
    return render(request, 'user/createblatt.html', context)



##########################
################

def listUser(request):
    pass


def listTutor(request):
    pass


def listKurs(request):
    pass