from django.shortcuts import redirect
from django.urls import path
from appointment import views as appointment_views
from login import views as login_views
from mydentist.handler import is_authenticated
from patient import views as patient_views
from . import views as dentx_views


def dentx_redirect(request):
    if is_authenticated(request, "dentist"):
        return redirect("dentx:appointments")
    else:
        return redirect("dentx:login")


urlpatterns = [
    path('', dentx_redirect, name='index'),
    path('auth/login/', login_views.dentx_login, name='login'),
    path('auth/logout/', login_views.dentx_logout, name='logout'),
    path('appointments/', appointment_views.appointments, name='appointments'),
    path('table/', appointment_views.table, name='table'),
    path('patients/list', appointment_views.patients, name='patients_list'),
    path('appointment', appointment_views.appointment, name='appointment'),
    path('board/', dentx_views.board, name='board'),
    path('patients/', patient_views.patients, name='patients'),
    path('patients/<int:id>', patient_views.patient, name='patient'),
]
