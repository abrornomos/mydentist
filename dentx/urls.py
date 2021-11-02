from django.urls import path
from appointment import views as appointment_views
from login import views as login_views
from patient import views as patient_views
from . import views as dentx_views

urlpatterns = [
    path('auth/login/', login_views.dentx_login, name='login'),
    path('auth/logout/', login_views.dentx_logout, name='logout'),
    path('appointments/', appointment_views.appointments, name='appointments'),
    path('table/', appointment_views.table, name='table'),
    path('patients/list', appointment_views.patients, name='patients_list'),
    path('board/', dentx_views.board, name='board'),
    path('patients/', patient_views.patients, name='patients'),
]
