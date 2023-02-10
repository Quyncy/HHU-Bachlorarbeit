from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views

from core.views import *

urlpatterns = [
    path('' , Index , name="index-admin"),
    path('login/' , loginView , name="login"),
    path('logout/', logoutView, name="logout"),

    # Erstelle Daten
    path('create-user/', createUser, name='create-user'),
    path('create-kursleiter/', createKursleiter, name='create-kursleiter'),
    path('create-tutor/', createTutor, name='create-tutor'),
    path('create-dozent/', createDozent, name='create-dozent'),
    
    path('create-kurs/', createKurs, name='create-kurs'),
    path('create-blatt/', createBlatt, name='create-blatt'),

    # Liste Daten
    path('list-user/', listUser, name='list-user'),
    path('list-kursleiter/', listKursleiter, name='list-kursleiter'),
    path('list-tutor/', listTutor, name='list-tutor'),
    path('list-dozent/', listDozent, name='list-dozent'),
    
    path('list-kurs/', listKurs, name='list-kurs'),
    path('list-blatt/', listBlatt, name='list-blatt'),

    # Erhalte Profil
    path('get-user/<str:id>/', get_user_profile, name='get-user'),
    path('get-kursleiter/<str:id>/', get_kursleiter_profile, name='get-kursleiter'),
    path('get-tutor/<str:id>/', get_tutor_profile, name='get-tutor'),
    path('get-dozent/<str:id>/', get_dozent_profile, name='get-dozent'),

    path('get-kurs/<str:id>/', get_kurs_info, name='get-kurs'),
    path('get-blatt/<str:id>/', get_blatt_info, name='get-blatt'),

    # Update Profil
    
    # Lösche Profil

    
]