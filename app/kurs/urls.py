from django.urls import path

from kurs import views

app_name = 'kurs'

urlpatterns = [
    path('', views.kursApiOverView, name='kurs-api-overview'),
    
    path('create-kurs/', views.CreateKursView.as_view(), name='create-kurs'),
    path('list-kurs/', views.KursList.as_view(), name='list-kurs'),
    path('detail-kurs/<str:pk>', views.KursDetail.as_view(), name='detail-kurs'),

    path('create-blatt/', views.CreateBlattView.as_view(), name='create-blatt'),
    path('list-blatt/', views.BlattList.as_view(), name='list-blatt'),
    path('detail-blatt/<str:pk>', views.BlattDetail.as_view(), name='detail-blatt'),
]