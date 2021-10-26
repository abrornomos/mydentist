from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.translation import get_language
from appointment.models import Appointment, Query
from mydentist.handler import check_language
from patient.models import User as UserExtra
from .forms import *
from .models import User as DentistUser, User_translation, Clinic, Clinic_translation, Service, Service_translation, Cabinet_Image

# Create your views here.


def dentist(request, slug):
    current_language = get_language()
    if request.method == "POST":
        queryform = QueryForm(request.POST)
        if queryform.is_valid():
            user = User.objects.get(username=request.user.username)
            user_extra = UserExtra.objects.get(user=user)
            dentist_extra = User_translation.objects.get(language__name=current_language, dentist__slug=slug)
            dentist = DentistUser.objects.get(pk=dentist_extra.dentist_id)
            query = Query.objects.create(
                dentist=dentist,
                patient=user_extra,
                reason=queryform.cleaned_data['reason'],
                comment=queryform.cleaned_data['comment'],
            )
    else:
        queryform = QueryForm()
    try:
        user = User.objects.get(username=request.user.username)
        user_extra = UserExtra.objects.get(user=user)
        appointment = None
        query = Query.objects.get(patient=user_extra)
    except:
        try:
            user = User.objects.get(username=request.user.username)
            user_extra = UserExtra.objects.get(user=user)
            appointment = Appointment.objects.get(patient=user_extra)
            query = None
        except:
            appointment = None
            query = None
    dentist_extra = User_translation.objects.get(language__name=current_language, dentist__slug=slug)
    dentist = DentistUser.objects.get(pk=dentist_extra.dentist_id)
    clinic = Clinic.objects.get(pk=dentist.clinic_id)
    clinic_extra = Clinic_translation.objects.get(language__name=current_language, clinic=clinic)
    cabinet_images = Cabinet_Image.objects.filter(dentist=dentist)
    authenticated = request.user.username in request.session
    if authenticated:
        check_language(request)
    try:
        services_obj = Service_translation.objects.filter(language__name=current_language, service__dentist=dentist)
        services = []
        for service_extra in services_obj:
            services.append({
                'service': Service.objects.get(pk=service_extra.service_id),
                'service_extra': service_extra
            })
    except:
        services = None
    if len(cabinet_images) > 1:
        return render(request, "dentist/dentist.html", {
            'clinic': clinic,
            'clinic_extra': clinic_extra,
            'dentist': dentist,
            'dentist_extra': dentist_extra,
            'services': services,
            'cabinet_image': cabinet_images[0],
            'cabinet_images': cabinet_images[1:],
            'counter': range(len(cabinet_images)),
            'queryform': queryform,
            'appointment': appointment,
            'query': query,
            'authenticated': authenticated
        })
    elif len(cabinet_images) == 1:
        return render(request, "dentist/dentist.html", {
            'clinic': clinic,
            'clinic_extra': clinic_extra,
            'dentist': dentist,
            'dentist_extra': dentist_extra,
            'services': services,
            'cabinet_image': cabinet_images[0],
            'cabinet_images': None,
            'counter': range(len(cabinet_images)),
            'queryform': queryform,
            'appointment': appointment,
            'query': query,
            'authenticated': authenticated
        })
    else:
        return render(request, "dentist/dentist.html", {
            'clinic': clinic,
            'clinic_extra': clinic_extra,
            'dentist': dentist,
            'dentist_extra': dentist_extra,
            'services': services,
            'cabinet_images': None,
            'counter': 0,
            'queryform': queryform,
            'appointment': appointment,
            'query': query,
            'authenticated': authenticated
        })
