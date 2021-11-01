from django.conf import settings as global_settings
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import get_language
from datetime import datetime, date, timedelta, tzinfo
from baseapp.models import Language
from dentist.models import User as DentistUser, User_translation as DentistUserTranslation, Service, Service_translation
from patient.models import User as PatientUser
from mydentist.var import *
from .forms import *
from .handler import *
from .models import *

# Create your views here.


def appointments(request):
    print(timezone.now().tzinfo)
    if request.user.username not in request.session:
        return redirect(f"{global_settings.LOGIN_URL}?next={request.path}")
    user = User.objects.get(username=request.user.username)
    dentist = DentistUser.objects.get(user=user)
    dentist_translation = DentistUserTranslation.objects.filter(
        dentist=dentist,
        language__name=Language.objects.get(pk=dentist.language_id)
    )[0]
    if request.method == "POST":
        appointmentform = AppointmentForm(request.POST)
        if appointmentform.is_valid():
            name = appointmentform.cleaned_data['name'].split(" ")
            if len(name) == 2:
                phone_number = appointmentform.cleaned_data['phone_number']
                patient = PatientUser.objects.get(phone_number=phone_number)
                patient_user = User.objects.get(pk=patient.user_id)
                if name[0] == patient_user.last_name and name[1] == patient_user.first_name and phone_number == patient.phone_number and str(patient.birthday) == appointmentform.cleaned_data['birthday'] and patient.gender_id == int(appointmentform.cleaned_data['gender']) and patient.address == appointmentform.cleaned_data['address']:
                    service_translation = Service_translation.objects.filter(
                        name=appointmentform.cleaned_data['service'],
                        language__pk=dentist.language_id
                    )[0]
                    service = Service.objects.get(pk=service_translation.service_id)
                    begin = appointmentform.cleaned_data['begin_day']
                    begin_day = int(begin.split("-")[0])
                    begin_month = MONTHS.index(begin.split("-")[1].split(" ")[0].capitalize()) + 1
                    begin_year = int(begin.split(" ")[1])
                    begin_hour = int(appointmentform.cleaned_data['begin_time'].split(":")[0])
                    begin_minute = int(appointmentform.cleaned_data['begin_time'].split(":")[1])
                    begin = datetime(begin_year, begin_month, begin_day, begin_hour, begin_minute, tzinfo=timezone.now().tzinfo)
                    duration = int(appointmentform.cleaned_data['duration'])
                    duration = timedelta(hours=duration // 60, minutes=duration % 60)
                    end = begin + duration
                    if compare_appointment(begin, end, Appointment.objects.filter(
                        begin__year=begin_year,
                        begin__month=begin_month,
                        begin__day=begin_day
                    )):
                        appointment = Appointment.objects.create(
                            dentist=dentist,
                            patient=patient,
                            service=service,
                            begin=begin,
                            end=end,
                            comment=appointmentform.cleaned_data['comment'],
                            status="waiting"
                        )
                    else:
                        print("Cannot register appointment")
                else:
                    print(False)
            elif len(name) == 1:
                pass
    services = get_services(
        Service.objects.filter(dentist=dentist),
        dentist.language_id
    )
    today = date.today()
    times = []
    day_begin = datetime(
        today.year,
        today.month,
        today.day,
        dentist.worktime_begin.hour,
        dentist.worktime_begin.minute
    )
    day_end = datetime(
        today.year,
        today.month,
        today.day,
        dentist.worktime_end.hour,
        dentist.worktime_end.minute
    )
    while day_begin < day_end:
        times.append(day_begin.strftime('%H:%M'))
        day_begin += timedelta(minutes=15)
    appointmentform = AppointmentForm()
    return render(request, "appointment/appointments.html", {
        'appointmentform': appointmentform,
        'dentist': dentist,
        'dentist_translation': dentist_translation,
        'services': services,
        'times': times
    })


def table(request):
    if request.method == "POST":
        if request.POST['direction'] == "left":
            day = date(
                int(request.POST['year']),
                int(request.POST['month']),
                int(request.POST['day'])
            ) - timedelta(weeks=1)
        elif request.POST['direction'] == "right":
            temp = date(
                int(request.POST['year']),
                int(request.POST['month']),
                int(request.POST['day'])
            )
            day = temp + timedelta(days=temp.weekday(), weeks=1)
    else:
        temp = date.today()
        day = temp - timedelta(days=temp.weekday())
    days = [day]
    html = f"<table class=\"time-table table-bordered text-center\"><thead><tr class=\"text-center\"><th>Time</th><th>{day.day}-{MONTHS[day.month - 1].lower()} {day.year}<br>{DAYS[day.weekday()]}</th>"
    for i in range(6):
        temp = days[len(days) - 1] + timedelta(days=1)
        days.append(temp)
        html += f"<th>{temp.day}-{MONTHS[temp.month - 1].lower()} {temp.year}<br>{DAYS[temp.weekday()]}</th>"
    html += "</tr></thead><tbody>"
    user = User.objects.get(username=request.user.username)
    dentist = DentistUser.objects.get(user=user)
    day_begin = datetime(
        days[0].year,
        days[0].month,
        days[0].day,
        dentist.worktime_begin.hour,
        dentist.worktime_begin.minute
    )
    day_end = datetime(
        days[0].year,
        days[0].month,
        days[0].day,
        dentist.worktime_end.hour,
        dentist.worktime_end.minute
    )
    while day_begin <= day_end:
        html += f"<tr><th>{day_begin.strftime('%H:%M')}</th>"
        for day in days:
            time = datetime(
                day.year,
                day.month,
                day.day,
                day_begin.hour,
                day_begin.minute,
                tzinfo=timezone.now().tzinfo
            )
            html += compare_time(time, Appointment.objects.filter(
                begin__year=time.year,
                begin__month=time.month,
                begin__day=time.day
            ))
        day_begin += timedelta(minutes=15)
        html += "</tr>"
    html += "</tbody></table>"
    return HttpResponse(html)


def patients(request):
    patients = []
    temp = PatientUser.objects.all()
    for patient in temp:
        patients.append({
            'image': str(patient.image),
            'name': str(patient),
            'phone_number': patient.phone_number,
            'birthday': str(patient.birthday),
            'gender': patient.gender_id,
            'address': patient.address
        })
    print(patients)
    return JsonResponse(patients, safe=False)
