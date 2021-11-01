from datetime import timedelta
from django.contrib.auth.models import User
from dentist.models import User as DentistUser, Service_translation
from patient.models import User as PatientUser


def compare_time(datetime, appointments):
    for appointment in appointments:
        if datetime - appointment.begin >= timedelta() and appointment.end - datetime > timedelta():
            if datetime - appointment.begin == timedelta():
                patient = PatientUser.objects.get(pk=appointment.patient_id)
                service = Service_translation.objects.filter(
                    service__pk=appointment.service_id,
                    language__pk=DentistUser.objects.get(pk=appointment.dentist_id).language_id
                )[0]
                duration = appointment.end - appointment.begin
                minutes = duration.seconds // 60
                return f"<td rowspan=\"{minutes // 15}\"><div>{patient}<br>{service.name}</div></td>"
            else:
                return ""
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
