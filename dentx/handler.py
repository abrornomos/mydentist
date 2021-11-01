from django.contrib.auth.models import User
from dentist.models import User as DentistUser, Service_translation
from patient.models import User as PatientUser

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
