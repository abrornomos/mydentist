from django.conf import settings as global_settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from appointment.models import *
from dentist.models import User as DentistUser
from mydentist.handler import *

# Create your views here.


def board(request):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL}?next={request.path}")
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        check_language(request, "dentist")
    user = User.objects.get(username=request.user.username)
    dentist = DentistUser.objects.get(user=user)
    queries = get_queries(Query.objects.filter(dentist=dentist))
    appointments = get_appointments(Appointment.objects.filter(dentist=dentist))
    return render(request, "dentx/board.html", {
        'dentist': dentist,
        'queries': queries,
        'appointments': appointments,
    })
