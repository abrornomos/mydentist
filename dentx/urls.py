from django.urls import path
from . import views

urlpatterns = [
    path('auth/login/', views.auth_login, name='auth_login'),
    path('auth/logout/', views.auth_logout, name='auth_logout'),
    path('appointments/', views.appointments, name='appointments'),
    path('board/', views.board, name='board'),
    path('patients/', views.patients, name='patients'),
]
