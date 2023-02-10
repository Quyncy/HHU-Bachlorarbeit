"""
Ansicht für die User API
"""
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user import views

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # User
    path('create-user/', views.CreateUserView.as_view(), name='create-user'),
    path('list-user/', views.UserListView.as_view(), name='list-user'),
    path('get-user/<str:pk>/', views.UserDetailView.as_view(), name='get-user'),
    # path('update-user/<str:pk>', views.UserDetailView.as_view(), name='update-user'),
    # path('delete-user/<str:pk>', views.UserDetailView.as_view(), name='delete-user'),

    # Kursleiter
    path('create-kursleiter/', views.CreateKursleiterView.as_view(), name='create-kursleiter'),
    path('list-kursleiter/', views.KursleiterListView.as_view(), name='list-kursleiter'),
    path('get-kursleiter/<str:pk>/', views.KursleiterDetailView.as_view(), name='get-kursleiter'),
    #path('create-kursleiterprofile/', views.CreateKursleiterView.as_view(), name='create-kursleiterprofile'),
    
    
    # Tutor
    path('create-tutor/', views.CreateTutorView.as_view(), name='create-tutor'),
    path('list-tutor/', views.TutorListView.as_view(), name='list-tutor'),
    path('get-tutor/<str:pk>/', views.TutorDetailView.as_view(), name='get-tutor'),
    # path('create-tutorprofile/', views.CreateTutorView.as_view(), name='create-tutorprofile'),
    

    # Dozent
    path('create-dozent/', views.CreateDozentView.as_view(), name='create-dozent'),
    path('list-dozent/', views.DozentListView.as_view(), name='list-dozent'),
    path('get-dozent/<str:pk>/', views.DozentDetailView.as_view(), name='get-dozent'),
    # path('detail-dozent/<str:pk>/', views.DozentDetailView.as_view(), name='detail-dozent'),
]