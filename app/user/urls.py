"""
Ansicht für die User API
"""
from django.urls import path
from user import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.apiOverView, name='apiOverView'),

    path('login/', obtain_auth_token, name='token'),

    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('token/', views.CreateTokenView.as_view(), name='token'),

    # User
    path('create-user/', views.CreateUserView.as_view(), name='create-user'),
    path('list-user/', views.UserListView.as_view(), name='list-user'),
    path('get-user/<str:pk>/', views.UserDetailView.as_view(), name='get-user'),
    path('update-user/<str:pk>/', views.UserDetailView.as_view(), name='update-user'),
    path('delete-user/<str:pk>/', views.UserDetailView.as_view(), name='delete-user'),


    # Kursleiter
    path('create-kursleiter/', views.CreateKursleiterView.as_view(), name='create-kursleiter'),
    path('list-kursleiter/', views.KursleiterListView.as_view(), name='list-kursleiter'),
    path('get-kursleiter/<str:pk>/', views.KursleiterDetailView.as_view(), name='get-kursleiter'),
    path('update-kursleiter/<str:pk>/', views.KursleiterDetailView.as_view(), name='update-kursleiter'),
    path('delete-kursleiter/<str:pk>/', views.KursleiterDetailView.as_view(), name='delete-kursleiter'),
    

    # Tutor
    path('create-tutor/', views.CreateTutorView.as_view(), name='create-tutor'),
    path('list-tutor/', views.TutorListView.as_view(), name='list-tutor'),
    path('get-tutor/<str:pk>/', views.TutorDetailView.as_view(), name='get-tutor'),
    path('update-tutor/<str:pk>/', views.TutorDetailView.as_view(), name='update-tutor'),
    path('delete-tutor/<str:pk>/', views.TutorDetailView.as_view(), name='delete-tutor'),


    # Dozent
    path('create-dozent/', views.CreateDozentView.as_view(), name='create-dozent'),
    path('list-dozent/', views.DozentListView.as_view(), name='list-dozent'),
    path('get-dozent/<str:pk>/', views.DozentDetailView.as_view(), name='get-dozent'),
    path('update-dozent/<str:pk>/', views.DozentDetailView.as_view(), name='update-dozent'),
    path('delete-dozent/<str:pk>/', views.DozentDetailView.as_view(), name='delete-dozent'),




    # path('create-kursleiterprofile/', views.CreateKursleiterView.as_view(), name='create-kursleiterprofile'),
    # path('create-tutorprofile/', views.CreateTutorView.as_view(), name='create-tutorprofile'),
    # path('detail-dozent/<str:pk>/', views.DozentDetailView.as_view(), name='detail-dozent'),
]