from django.shortcuts import render

from .forms import (
    DozentForm,
    BlattForm,
)

import requests

from rest_framework.response import Response
from rest_framework import status

def createDozent(request):
    dozent_form = DozentForm()
    
    if request.POST:
        dozent_form = DozentForm(request.POST)
        url = 'http://127.0.0.1:8000/api/user/create-dozent/'

        if dozent_form.is_valid():
            payload = {
                'title': dozent_form.cleaned_data['title'],
                'vorname': dozent_form.cleaned_data['vorname'],
                'nachname': dozent_form.cleaned_data['nachname'],
            }

            response = requests.post(url, data=payload)
            
            if response.status_code == 200:
                return Response("Dozent erfolreich gespeichert.", status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Methode nicht erlaubt'}, status=status.HTTP_400_BAD_REQUEST)

    context={'form':dozent_form, }
    return render(request, 'user/createdozent.html', context)



def createBlatt(request):
    blatt_form = BlattForm

    if request.POST:
        blatt_form = BlattForm(request.POST)
        url = 'http://localhost:8000/api/kurs/create-blatt/'

        if blatt_form.is_valid():
            kurs = blatt_form.cleaned_data['kurs']
            payload = {
                'ass_name': blatt_form.cleaned_data['ass_name'],
                'ass_id': blatt_form.cleaned_data['ass_id'],
                'kurs': kurs.id,
            }

            response = requests.post(url, data=payload)
            if response.status_code == '200':
                return Response(status=status.HTTP_200_OK)
    
    context={'form': blatt_form, }
    return render(request, 'user/createblatt.html', context)
