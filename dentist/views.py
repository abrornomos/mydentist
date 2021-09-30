from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.translation import get_language
from .forms import *
from .models import *
from baseapp.forms import SearchForm
from patient.models import User as UserExtra

# Create your views here.


def dentist(request, slug):
    if request.method == "POST":
        queryform = QueryForm(request.POST)
        if queryform.is_valid():
            user = User.objects.get(username=request.user.username)
            user_extra = UserExtra.objects.get(user=user)
            current_language = get_language()
            dentist = Dentist.objects.get(clinic__language__name=current_language, slug=slug)
            appointment = Appointment.objects.create(
                user=user_extra,
                reason=queryform.cleaned_data['reason'],
                comment=queryform.cleaned_data['comment'],
                dentist=dentist,
                attend="waiting"
            )
    else:
        queryform = QueryForm()
    try:
        user = User.objects.get(username=request.user.username)
        user_extra = UserExtra.objects.get(user=user)
        appointment = Appointment.objects.get(user=user_extra)
    except:
        appointment = None
    current_language = get_language()
    dentist = Dentist.objects.get(clinic__language__name=current_language, slug=slug)
    clinic = Clinic.objects.get(pk=dentist.clinic_id)
    cabinet_images = Cabinet_Image.objects.filter(dentist__pk=dentist.id)
    try:
        services = Service.objects.filter(dentist__pk=dentist.id)
    except:
        services = None
    if len(cabinet_images) > 1:
        return render(request, "dentist/dentist.html", {
            'clinic': clinic,
            'dentist': dentist,
            'services': services,
            'cabinet_image': cabinet_images[0],
            'cabinet_images': cabinet_images[1:],
            'counter': range(len(cabinet_images)),
            'queryform': queryform,
            'appointment': appointment,
        })
    elif len(cabinet_images) == 1:
        return render(request, "dentist/dentist.html", {
            'clinic': clinic,
            'dentist': dentist,
            'services': services,
            'cabinet_image': cabinet_images[0],
            'cabinet_images': None,
            'counter': range(len(cabinet_images)),
            'queryform': queryform,
            'appointment': appointment,
        })
    else:
        return render(request, "dentist/dentist.html", {
            'clinic': clinic,
            'dentist': dentist,
            'services': services,
            'cabinet_images': None,
            'counter': 0,
            'queryform': queryform,
            'appointment': appointment,
        })
