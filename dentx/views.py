from django.conf import settings as global_settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from appointment.models import *
from dentist.models import User as DentistUser, Reminder
from mydentist.handler import *


def board(request):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL_DENTX}?next={request.path}")
        else:
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        check_language(request, "dentist")
    user = User.objects.get(username=request.user.username)
    dentist = DentistUser.objects.get(user=user)
    notifications = get_notifications(request, "dentist")
    queries = get_queries(Query.objects.filter(dentist=dentist))
    appointments = get_appointments(Appointment.objects.filter(dentist=dentist))
    return render(request, "dentx/board.html", {
        'dentist': dentist,
        'notifications': notifications,
        'notifications_count': len(notifications),
        'queries': queries,
        'appointments': appointments,
    })


def reminders(request):
    dentist = DentistUser.objects.get(user__username=request.user.username)
    if request.method == "POST":
        reminder = Reminder.objects.create(
            dentist=dentist,
            name=request.POST['name'],
            category=request.POST['category'],
            is_done=False
        )
    reminders_do = get_reminders(Reminder.objects.filter(
        dentist=dentist,
        category="do"
    ))
    reminders_buy = get_reminders(Reminder.objects.filter(
        dentist=dentist,
        category="buy"
    ))
    return JsonResponse({
        "do": reminders_do,
        "buy": reminders_buy
    }, safe=False)
