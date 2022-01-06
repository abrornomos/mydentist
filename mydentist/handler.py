from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils import translation
from geopy.distance import distance
from baseapp.models import Language
from dentist.models import User as DentistUser, User_translation, Clinic, Clinic_translation, Service, Service_translation
from notification.models import *
from patient.models import User as PatientUser
from .var import CHOICES


def set_language(request, user_language):
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    url = redirect(request.META.get("HTTP_REFERER", "/")).url
    if "/results/" in url:
        if 'post' in request.session:
            post = request.session['post']
            post['service'] = Service_translation.objects.filter(
                service__pk=Service_translation.objects.filter(name=post['service'])[0].service_id,
                language__name=user_language
            )[0].name
    return redirect(request.META.get("HTTP_REFERER", "/"))


def is_authenticated(request, status):
    if request.user.username in request.session:
        if status == "dentist":
            try:
                user = DentistUser.objects.get(user__username=request.user.username)
                return True
            except:
                return False
        elif status == "patient":
            try:
                user = PatientUser.objects.get(user__username=request.user.username)
                return True
            except:
                return False
    else:
        return False


def check_language(request, status):
    if status == "dentist":
        dentist = DentistUser.objects.get(user__username=request.user.username)
        language = Language.objects.get(pk=dentist.language_id).name
        if translation.get_language() != language:
            translation.activate(language)
            request.session[translation.LANGUAGE_SESSION_KEY] = language
    elif status == "patient":
        patient = PatientUser.objects.get(user__username=request.user.username)
        language = Language.objects.get(pk=patient.language_id).name
        if translation.get_language() != language:
            translation.activate(language)
            request.session[translation.LANGUAGE_SESSION_KEY] = language


def get_queries(queries):
    results = []
    for query in queries:
        dentist_extra = DentistUser.objects.get(pk=query.dentist_id)
        results.append({
            'dentist': User.objects.get(pk=dentist_extra.user_id),
            'dentist_extra': dentist_extra,
            'patient': PatientUser.objects.get(pk=query.patient_id),
            'query': query
        })
    return results


def get_appointments(appointments):
    results = []
    for appointment in appointments:
        dentist_extra = DentistUser.objects.get(pk=appointment.dentist_id)
        results.append({
            'dentist': User.objects.get(pk=dentist_extra.user_id),
            'dentist_extra': dentist_extra,
            'patient': PatientUser.objects.get(pk=appointment.patient_id),
            'service': Service_translation.objects.filter(service__pk=appointment.service_id)[0],
            'appointment': appointment
        })
    return results


def get_reminders(reminders):
    results = []
    for reminder in reminders:
        results.append({
            'id': reminder.id,
            'name': reminder.name,
            'category': reminder.category,
            'is_done': reminder.is_done
        })
    return results


def sort_by_distance(services, location):
    if len(services) < 2:
        return services
    else:
        middle = services[0]
        less = [
            service for service in services[1:]
            if distance(
                (
                    Clinic.objects.get(
                        pk=DentistUser.objects.get(
                            pk=Service.objects.get(pk=service.service_id).dentist_id
                        ).clinic_id
                    ).latitude,
                    Clinic.objects.get(
                        pk=DentistUser.objects.get(
                            pk=Service.objects.get(pk=service.service_id).dentist_id
                        ).clinic_id
                    ).longitude,
                ),
                location
            ).kilometers <= distance(
                (
                    Clinic.objects.get(
                        pk=DentistUser.objects.get(
                            pk=Service.objects.get(pk=middle.service_id).dentist_id
                        ).clinic_id
                    ).latitude,
                    Clinic.objects.get(
                        pk=DentistUser.objects.get(
                            pk=Service.objects.get(pk=middle.service_id).dentist_id
                        ).clinic_id
                    ).longitude,
                ),
                location
            ).kilometers
        ]
        greater = [
            service for service in services[1:]
            if distance(
                (
                    Clinic.objects.get( 
                        pk=DentistUser.objects.get(
                            pk=Service.objects.get(pk=service.service_id).dentist_id
                        ).clinic_id
                    ).latitude,
                    Clinic.objects.get(
                        pk=DentistUser.objects.get(
                            pk=Service.objects.get(pk=service.service_id).dentist_id
                        ).clinic_id
                    ).longitude,
                ),
                location
            ).kilometers > distance(
                (
                    Clinic.objects.get(
                        pk=DentistUser.objects.get(
                            pk=Service.objects.get(pk=middle.service_id).dentist_id
                        ).clinic_id
                    ).latitude,
                    Clinic.objects.get(
                        pk=DentistUser.objects.get(
                            pk=Service.objects.get(pk=middle.service_id).dentist_id
                        ).clinic_id
                    ).longitude,
                ),
                location
            ).kilometers
        ]
        return sort_by_distance(less, location) + [middle] + sort_by_distance(greater, location)


def get_results(services_obj):
    results = []
    for service_obj in services_obj:
        service = Service.objects.get(pk=service_obj.service_id)
        dentist = DentistUser.objects.get(pk=service.dentist_id)
        dentist_extra = User_translation.objects.filter(dentist=dentist, language__pk=service_obj.language_id)[0]
        clinic = Clinic.objects.get(pk=dentist.clinic_id)
        clinic_extra = Clinic_translation.objects.filter(clinic=clinic, language__pk=service_obj.language_id)[0]
        worktime_begin = dentist.worktime_begin
        worktime_end = dentist.worktime_end
        results.append({
            'image': dentist.image.url,
            'clinic_name': clinic_extra.name,
            'fullname': dentist_extra.fullname,
            'address': clinic_extra.address,
            'orientir': clinic_extra.orientir,
            'latitude': clinic.latitude,
            'longitude': clinic.longitude,
            'worktime_begin': f"{worktime_begin.hour}:{worktime_begin.minute:02d}",
            'worktime_end': f"{worktime_end.hour}:{worktime_end.minute:02d}",
            'is_fullday': dentist.is_fullday,
            'phone_number': dentist.phone_number,
            'service_name': service_obj.name,
            'service_price': service.price,
            'slug': dentist.slug,
        })
    return results


def compare_time(datetime, appointments):
    for appointment in appointments:
        if datetime - appointment.begin >= timedelta() and appointment.end - datetime > timedelta():
            if datetime - appointment.begin == timedelta():
                patient = PatientUser.objects.get(pk=appointment.patient_id)
                service = Service_translation.objects.filter(
                    service__pk=appointment.service_id,
                    language__pk=DentistUser.objects.get(
                        pk=appointment.dentist_id).language_id
                )[0]
                duration = appointment.end - appointment.begin
                minutes = duration.seconds // 60
                return f"<td class=\"appointment\" rowspan=\"{minutes // 15}\"><div>{patient}<br>{service.name}</div></td>"
            else:
                return "<td class=\"d-none\"></td>"
    return f"<td class=\"time\">{datetime.strftime('%H:%M')}</td>"


def compare_appointment(begin, end, appointments):
    for appointment in appointments:
        if begin - appointment.begin >= timedelta():
            if not begin - appointment.end >= timedelta():
                return False
        elif not appointment.begin - end >= timedelta():
            return False
    return True


def get_services(services, language_id):
    results = []
    for service in services:
        results.append({
            'service': service,
            'service_name': Service_translation.objects.filter(
                service=service,
                language__pk=language_id
            )[0]
        })
    return results


def get_option(select, index):
    options = CHOICES[select]
    for option in options:
        if int(option[0]) == index:
            return option[1]
    return None


def get_notifications(request, status):
    if status == "patient":
        notifications_obj = list(Dentist2patient.objects.filter(recipient__user__username=request.user.username))[::-1]
        notifications = []
        for notification_obj in notifications_obj:
            notifications.append({
                'sender': DentistUser.objects.get(pk=notification_obj.sender_id),
                'recipient': PatientUser.objects.get(pk=notification_obj.recipient_id),
                'notification': notification_obj
            })
        return notifications
    elif status == "dentist":
        notifications_obj = list(Patient2dentist.objects.filter(recipient__user__username=request.user.username))[::-1]
        notifications = []
        for notification_obj in notifications_obj:
            notifications.append({
                'sender': PatientUser.objects.get(pk=notification_obj.sender_id),
                'recipient': DentistUser.objects.get(pk=notification_obj.recipient_id),
                'notification': notification_obj
            })
        return notifications


# def sort_by_distance(dentists, location):
#     if len(dentists) < 2:
#         return dentists
#     else:
#         middle = dentists[0]
#         less = [
#             dentist for dentist in dentists[1:]
#             if distance((dentist['latitude'], dentist['longitude']), location).kilometers <= distance((middle['latitude'], middle['longitude']), location).kilometers
#         ]
#         greater = [
#             dentist for dentist in dentists[1:]
#             if distance((dentist['latitude'], dentist['longitude']), location).kilometers <= distance((middle['latitude'], middle['longitude']), location).kilometers
#         ]
#         return sort_by_distance(less, location) + [middle] + sort_by_distance(greater, location)


# def get_ip(request):
#     address = request.META.get("HTTP_X_FORWARDED_FOR")
#     return address.split(",")[-1].strip() if address else request.META.get("REMOTE_ADDR")

# old_full_url = request.META.get("HTTP_REFERER", "/")
# old_url = f"/{'/'.join(old_full_url.split('/')[3:])}"
# prefix_exists = False
# for language in settings.EXTRA_LANGUAGES:
#     if f"/{language[0]}/" in old_url:
#         prefix_exists = True
# if not prefix_exists and user_language != settings.LANGUAGE_CODE:
#     new_url = F"/{user_language}{old_url}"
# elif user_language == settings.LANGUAGE_CODE:
#     new_url = old_url.replace(f"/{old_url.split('/')[1]}/", "/")
# else:
#     new_url = old_url.replace(f"/{old_url.split('/')[1]}/", f"/{user_language}/")
# return redirect(new_url)
