from django.contrib.auth.models import User
from geopy.distance import distance
from dentist.models import User as DentistUser, User_translation, Clinic, Clinic_translation, Service


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


def get_results(services):
    results = []
    for service in services:
        service_obj = Service.objects.get(pk=service.service_id)
        dentist = DentistUser.objects.get(pk=service_obj.dentist_id)
        dentist_extra = User_translation.objects.filter(dentist=dentist, language__pk=service.language_id)[0]
        clinic = Clinic.objects.get(pk=dentist.clinic_id)
        clinic_extra = Clinic_translation.objects.filter(clinic=clinic, language__pk=service.language_id)[0]
        results.append({
            'dentist': dentist,
            'dentist_extra': dentist_extra,
            'clinic': clinic,
            'clinic_extra': clinic_extra,
        })
    return results
