from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from core.views import *

urlpatterns = [
    path('' , Index , name="index"),
    path('login/' , loginPage , name="login"),

    # Erstelle Daten
    path('create-user/', createUser, name='create-user'),
    path('create-kursleiter/', createKursleiter, name='create-kursleiter'),
    path('create-tutor/', createTutor, name='create-tutor'),
    path('create-dozent/', createDozent, name='create-dozent'),
    
    path('create-kurs/', createKurs, name='create-kurs'),
    path('create-blatt/', createBlatt, name='create-blatt'),

    # Liste ansehen
    path('list-user/', listUser, name='list-user'),
      
    path('list-tutor/', listTutor, name='list-tutor'),

    path('list-kurs/', listKurs, name='list-kurs'),

]