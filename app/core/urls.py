from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from core.views import *

urlpatterns = [
    # Erstelle Daten
    path('create-dozent/', createDozent, name='create-dozent'),
    # path('create-kurs/', createKurs, name='create-kurs'),
    # path('create-tutor/', createTutor, name='create-tutor'),
    # path('create-kursleiter/', createKursleiter, name='create-kursleiter'),
    # path('create-user/', createUser, name='create-user'),

    path('create-blatt/', createBlatt, name='create-blatt'),
]