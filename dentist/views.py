from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.translation import get_language
from appointment.models import Query
from patient.models import User as UserExtra
from .forms import *
from .models import User as DentistUser, Clinic, Service, Cabinet_Image

# Create your views here.


def dentist(request, slug):
    if request.method == "POST":
        queryform = QueryForm(request.POST)
        if queryform.is_valid():
            user = User.objects.get(username=request.user.username)
            user_extra = UserExtra.objects.get(user=user)
            current_language = get_language()
            dentist_extra = DentistUser.objects.get(clinic__language__name=current_language, slug=slug)
            dentist = User.objects.get(pk=dentist_extra.user_id)
            query = Query.objects.create(
                dentist=dentist_extra,
                user=user_extra,
                reason=queryform.cleaned_data['reason'],
                comment=queryform.cleaned_data['comment'],
            )
    else:
        queryform = QueryForm()
    try:
        user = User.objects.get(username=request.user.username)
        user_extra = UserExtra.objects.get(user=user)
        query = Query.objects.get(user=user_extra)
    except:
        query = None
    current_language = get_language()
    dentist_extra = DentistUser.objects.get(clinic__language__name=current_language, slug=slug)
    dentist = User.objects.get(pk=dentist_extra.user_id)
    clinic = Clinic.objects.get(pk=dentist_extra.clinic_id)
    cabinet_images = Cabinet_Image.objects.filter(dentist__pk=dentist_extra.id)
    authenticated = request.user.username in request.session
    try:
        services = Service.objects.filter(dentist__pk=dentist_extra.id)
    except:
        services = None
    if len(cabinet_images) > 1:
        return render(request, "dentist/dentist.html", {
            'clinic': clinic,
            'dentist': dentist,
            'dentist_extra': dentist_extra,
            'services': services,
            'cabinet_image': cabinet_images[0],
            'cabinet_images': cabinet_images[1:],
            'counter': range(len(cabinet_images)),
            'queryform': queryform,
            'query': query,
            'authenticated': authenticated
        })
    elif len(cabinet_images) == 1:
        return render(request, "dentist/dentist.html", {
            'clinic': clinic,
            'dentist': dentist,
            'dentist_extra': dentist_extra,
            'services': services,
            'cabinet_image': cabinet_images[0],
            'cabinet_images': None,
            'counter': range(len(cabinet_images)),
            'queryform': queryform,
            'query': query,
            'authenticated': authenticated
        })
    else:
        return render(request, "dentist/dentist.html", {
            'clinic': clinic,
            'dentist': dentist,
            'dentist_extra': dentist_extra,
            'services': services,
            'cabinet_images': None,
            'counter': 0,
            'queryform': queryform,
            'query': query,
            'authenticated': authenticated
        })
