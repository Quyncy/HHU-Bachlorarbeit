from django.urls import path

from kurs import views

app_name = 'kurs'

urlpatterns = [
    path('', views.kursApiOverView, name='kurs-api-overview'),
    
    path('create-kurs/', views.CreateKursView.as_view(), name='create-kurs'),
    path('list-kurs/', views.KursList.as_view(), name='list-kurs'),
    path('get-kurs/<str:pk>', views.KursDetail.as_view(), name='get-kurs'),
    #path('update-kurs/<str:pk>', views.KursDetail.as_view(), name='update-kurs'),
    #path('delete-kurs/<str:pk>', views.KursDetail.as_view(), name='delete-kurs'),

    path('create-blatt/', views.CreateBlattView.as_view(), name='create-blatt'),
    path('list-blatt/', views.BlattList.as_view(), name='list-blatt'),
    path('get-blatt/<str:pk>', views.BlattDetail.as_view(), name='get-blatt'),
    #path('update-blatt/<str:pk>', views.KursDetail.as_view(), name='update-blatt'),
    #path('delete-blatt/<str:pk>', views.KursDetail.as_view(), name='delete-blatt'),

    path('create-blattkorrektur/', views.CreateBlattKorrekturView.as_view(), name='create-blattkorrektur'),
]