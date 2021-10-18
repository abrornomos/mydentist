from django.contrib.auth.models import User
from geopy.distance import distance
from dentist.models import User as DentistUser, Clinic


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
                            pk=service.dentist_id
                        ).clinic_id
                    ).latitude,
                    Clinic.objects.get(
                        pk=DentistUser.objects.get(
                            pk=service.dentist_id
                        ).clinic_id
                    ).longitude,
                ),
                location
            ).kilometers <= distance(
                (
                    Clinic.objects.get(
                        pk=DentistUser.objects.get(
                            pk=middle.dentist_id
                        ).clinic_id
                    ).latitude,
                    Clinic.objects.get(
                        pk=DentistUser.objects.get(
                            pk=middle.dentist_id
                        ).clinic_id
                    ).longitude,
                ),
                location
            ).kilometers
        ]
        print(less)
        greater = [
            service for service in services[1:]
            if distance(
                (
                    Clinic.objects.get(
                        pk=DentistUser.objects.get(
                            pk=service.dentist_id
                        ).clinic_id
                    ).latitude,
                    Clinic.objects.get(
                        pk=DentistUser.objects.get(
                            pk=service.dentist_id
                        ).clinic_id
                    ).longitude,
                ),
                location
            ).kilometers > distance(
                (
                    Clinic.objects.get(
                        pk=DentistUser.objects.get(
                            pk=middle.dentist_id
                        ).clinic_id
                    ).latitude,
                    Clinic.objects.get(
                        pk=DentistUser.objects.get(
                            pk=middle.dentist_id
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
        dentist_extra = DentistUser.objects.get(pk=service.dentist_id)
        dentist = User.objects.get(pk=dentist_extra.user_id)
        clinic = Clinic.objects.get(pk=dentist_extra.clinic_id)
        results.append({
            'dentist': dentist,
            'dentist_extra': dentist_extra,
            'clinic': clinic
        })
    return results
