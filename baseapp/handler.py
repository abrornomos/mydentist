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
