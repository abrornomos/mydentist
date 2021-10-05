from geopy.distance import distance
from geopy.units import kilometers
from dentist.models import *


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
                        pk=Dentist.objects.get(
                            pk=service.dentist_id
                        ).clinic_id
                    ).latitude,
                    Clinic.objects.get(
                        pk=Dentist.objects.get(
                            pk=service.dentist_id
                        ).clinic_id
                    ).longitude,
                ),
                location
            ).kilometers <= distance(
                (
                    Clinic.objects.get(
                        pk=Dentist.objects.get(
                            pk=middle.dentist_id
                        ).clinic_id
                    ).latitude,
                    Clinic.objects.get(
                        pk=Dentist.objects.get(
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
                        pk=Dentist.objects.get(
                            pk=service.dentist_id
                        ).clinic_id
                    ).latitude,
                    Clinic.objects.get(
                        pk=Dentist.objects.get(
                            pk=service.dentist_id
                        ).clinic_id
                    ).longitude,
                ),
                location
            ).kilometers > distance(
                (
                    Clinic.objects.get(
                        pk=Dentist.objects.get(
                            pk=middle.dentist_id
                        ).clinic_id
                    ).latitude,
                    Clinic.objects.get(
                        pk=Dentist.objects.get(
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
        dentist = Dentist.objects.get(pk=service.dentist_id)
        clinic = Clinic.objects.get(pk=dentist.clinic_id)
        results.append({
            'dentist': dentist,
            'clinic': clinic
        })
    return results
