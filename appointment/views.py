from django.conf import settings as global_settings
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import get_language
from datetime import datetime, date, timedelta
from baseapp.models import Language
from dentist.models import User as DentistUser, User_translation as DentistUserTranslation, Service, Service_translation
from patient.forms import PatientForm
from patient.models import User as PatientUser
from mydentist.handler import *
from mydentist.var import *
from patient.views import patient
from .forms import *
from .models import *

# Create your views here.


def appointments(request):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL_DENTX}?next={request.path}")
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        check_language(request, "dentist")
    user = User.objects.get(username=request.user.username)
    dentist = DentistUser.objects.get(user=user)
    dentist_translation = DentistUserTranslation.objects.filter(
        dentist=dentist,
        language__name=Language.objects.get(pk=dentist.language_id)
    )[0]
    if request.method == "POST":
        patientform = PatientForm(request.POST)
        appointmentform = AppointmentForm(request.POST)
        if patientform.is_valid() and appointmentform.is_valid():
            name = patientform.cleaned_data['name'].split(" ")
            if len(name) == 2:
                phone_number = patientform.cleaned_data['phone_number']
                patient = PatientUser.objects.get(phone_number=phone_number)
                patient_user = User.objects.get(pk=patient.user_id)
                if name[0] == patient_user.last_name and name[1] == patient_user.first_name and phone_number == patient.phone_number and str(patient.birthday) == patientform.cleaned_data['birthday'] and patient.gender_id == int(patientform.cleaned_data['gender']) and patient.address == patientform.cleaned_data['address']:
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
    patientform = PatientForm()
    appointmentform = AppointmentForm()
    return render(request, "appointment/appointments.html", {
        'patientform': patientform,
        'appointmentform': appointmentform,
        'dentist': dentist,
        'dentist_translation': dentist_translation,
        'services': services,
        'times': times
    })


def appointments_update(request):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL_DENTX}?next={request.path}")
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        check_language(request, "dentist")
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        dentist = DentistUser.objects.get(user=user)
        dentist_translation = DentistUserTranslation.objects.filter(
            dentist=dentist,
            language__name=Language.objects.get(pk=dentist.language_id)
        )[0]
        patientform = PatientForm(request.POST)
        appointmentform = AppointmentForm(request.POST)
        if patientform.is_valid() and appointmentform.is_valid():
            name = patientform.cleaned_data['name'].split(" ")
            if len(name) == 2:
                phone_number = patientform.cleaned_data['phone_number']
                patient = PatientUser.objects.get(phone_number=phone_number)
                patient_user = User.objects.get(pk=patient.user_id)
                if name[0] == patient_user.last_name and name[1] == patient_user.first_name and phone_number == patient.phone_number and str(patient.birthday) == patientform.cleaned_data['birthday'] and patient.gender_id == int(patientform.cleaned_data['gender']) and patient.address == patientform.cleaned_data['address']:
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
                    try:
                        last_begin = request.session['date']
                        last_begin_day = int(last_begin.split("-")[0])
                        last_begin_month = MONTHS.index(last_begin.split("-")[1].split(" ")[0].capitalize()) + 1
                        last_begin_year = int(last_begin.split(" ")[1])
                        last_begin_hour = int(request.session['time'].split(":")[0])
                        last_begin_minute = int(request.session['time'].split(":")[1])
                        last_begin = datetime(last_begin_year, last_begin_month, last_begin_day, last_begin_hour, last_begin_minute, tzinfo=timezone.now().tzinfo)
                        appointment = Appointment.objects.get(
                            dentist=dentist,
                            begin=last_begin,
                        )
                        print(appointment)
                        appointment.patient_id = patient.id
                        appointment.service_id = service.id
                        appointment.begin = begin
                        appointment.end = end
                        appointment.comment = appointmentform.cleaned_data["comment"]
                        appointment.status = "waiting"
                        appointment.save()
                    except Exception as E:
                        print(str(E))
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
        patientform = PatientForm()
        appointmentform = AppointmentForm()
        return redirect("dentx:appointments")


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
    return JsonResponse(patients, safe=False)


def appointment(request):
    try:
        date = request.POST['date'].split("<br>")[0]
        request.session['date'] = date
        day = date.split("-")[0]
        month = MONTHS.index(date.split("-")[1].split(" ")[0].capitalize()) + 1
        year = date.split(" ")[1]
        time = request.POST['time']
        request.session['time'] = time
        hour = time.split(":")[0]
        minute = time.split(":")[1]
        appointment = Appointment.objects.get(
            dentist__user__username=request.user.username,
            begin__year=year,
            begin__month=month,
            begin__day=day,
            begin__hour=hour,
            begin__minute=minute,
        )
        patient = PatientUser.objects.get(pk=appointment.patient_id)
        service = Service_translation.objects.get(
            service__pk=appointment.service_id,
            language__name=get_language()
        )
        return JsonResponse({
            'name': str(patient),
            'phone_number': patient.phone_number,
            'birthday': str(patient.birthday),
            'gender': patient.gender_id,
            'address': patient.address,
            'service': service.name,
            'duration': (appointment.end - appointment.begin).seconds // 60,
            'comment': appointment.comment,
            'date': request.POST['date'],
            'time': time
        }, safe=False)
    except:
        return JsonResponse({}, safe=False)
