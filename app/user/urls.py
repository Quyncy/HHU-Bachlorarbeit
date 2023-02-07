"""
Ansicht für die User API
"""
from django.urls import path

from user import views

urlpatterns = [
    # User
    path('create-user/', views.CreateUserView.as_view(), name='create-user'),
    path('list-user/', views.UserListView.as_view(), name='list-user'),
    path('detail-user/<str:pk>', views.UserDetailView.as_view(), name='detail-user'),

    # Kursleiter
    path('create-kursleiter/', views.CreateKursleiterView.as_view(), name='create-kursleiter'),
    path('list-kursleiter/', views.KursleiterListView.as_view(), name='list-kursleiter'),
    path('detail-kursleiter/<str:pk>', views.KursleiterDetailView.as_view(), name='detail-kursleiter'),

    # Tutor
    path('create-tutor/', views.CreateTutorView.as_view(), name='create-tutor'),
    path('list-tutor/', views.TutorListView.as_view(), name='list-tutor'),
    path('detail-tutor/<str:pk>', views.TutorDetailView.as_view(), name='detail-tutor'),

    # Dozent
    path('create-dozent/', views.CreateDozentView.as_view(), name='create-dozent'),
    path('list-dozent/', views.DozentListView.as_view(), name='list-dozent'),
    path('detail-dozent/<str:pk>', views.DozentDetailView.as_view(), name='detail-dozent'),
]