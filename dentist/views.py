from django.conf import settings as global_settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import render
from django.utils.translation import get_language
from appointment.models import Appointment, Query
from login.forms import PasswordUpdateForm
from mydentist.handler import *
from mydentist.var import *
from patient.forms import LanguageForm
from patient.models import User as UserExtra
from .forms import *
from .models import User as DentistUser, User_translation as DentistUserTranslation, Clinic, Clinic_translation, Service, Service_translation, Cabinet_Image

# Create your views here.


def dentist(request, slug):
    current_language = get_language()
    if request.method == "POST":
        queryform = QueryForm(request.POST)
        if queryform.is_valid():
            user = User.objects.get(username=request.user.username)
            user_extra = UserExtra.objects.get(user=user)
            dentist_extra = DentistUserTranslation.objects.get(language__name=current_language, dentist__slug=slug)
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
    dentist_extra = DentistUserTranslation.objects.get(language__name=current_language, dentist__slug=slug)
    dentist = DentistUser.objects.get(pk=dentist_extra.dentist_id)
    clinic = Clinic.objects.get(pk=dentist.clinic_id)
    clinic_extra = Clinic_translation.objects.get(language__name=current_language, clinic=clinic)
    cabinet_images = Cabinet_Image.objects.filter(dentist=dentist)
    authenticated = is_authenticated(request, "patient") or is_authenticated(request, "dentist")
    if authenticated:
        try:
            user = PatientUser.objects.get(
                user__username=request.user.username)
            authenticated = "patient"
            check_language(request, "patient")
        except:
            try:
                user = DentistUser.objects.get(
                    user__username=request.user.username)
                authenticated = "dentist"
            except:
                pass
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


def settings(request, active_tab="profile"):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL_DENTX}?next={request.path}")
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        check_language(request, "dentist")
    if 'success_message' in request.session:
        if request.session['success_message'] == "Updated successfully":
            success_message = "Updated successfully"
        elif request.session['success_message'] == "Passwords do not match":
            success_message = "Passwords do not match"
        del request.session['success_message']
    else:
        success_message = None
    user = User.objects.get(username=request.user.username)
    dentist = DentistUser.objects.get(user=user)
    dentist_translation = DentistUserTranslation.objects.filter(
        dentist=dentist,
        language__name=Language.objects.get(pk=dentist.language_id)
    )[0]
    clinic = Clinic.objects.get(pk=dentist.clinic_id)
    clinic_uzbek = Clinic_translation.objects.get(
        clinic=clinic,
        language__name="uz"
    )
    clinic_russian = Clinic_translation.objects.get(
        clinic=clinic,
        language__name="ru"
    )
    cabinet_images = Cabinet_Image.objects.filter(dentist=dentist)
    if len(cabinet_images) > 1:
        cabinet_image = cabinet_images[0]
        cabinet_images = cabinet_images[1:]
        counter = range(len(cabinet_images))
    elif len(cabinet_images) == 1:
        cabinet_image = cabinet_images[0]
        cabinet_images = None
        counter = range(1)
    else:
        cabinet_image = None
        cabinet_images = None
        counter = range(len(cabinet_images))
    userform = UserForm({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'gender': dentist.gender_id,
        'birth_year': dentist.birthday.year,
        'birth_month': MONTHS[dentist.birthday.month - 1],
        'birth_day': dentist.birthday.day,
        'phone_number': dentist.phone_number,
        'email': user.email,
    })
    languageform = LanguageForm({
        'language': dentist.language_id
    })
    clinicform = ClinicForm({
        'name_uzbek': clinic_uzbek.name,
        'name_russian': clinic_russian.name,
        'region': clinic.region_id,
        'address_uzbek': clinic_uzbek.address,
        'address_russian': clinic_russian.address,
        'orientir_uzbek': clinic_uzbek.orientir,
        'orientir_russian': clinic_russian.orientir,
        'worktime_begin': dentist.worktime_begin,
        'worktime_end': dentist.worktime_end,
    })
    if 'incorrect_password' in request.session:
        passwordupdateform = PasswordUpdateForm(request.session['incorrect_password'])
        del request.session['incorrect_password']
    else:
        passwordupdateform = PasswordUpdateForm()
    return render(request, "dentist/settings.html", {
        'userform': userform,
        'languageform': languageform,
        'passwordupdateform': passwordupdateform,
        'clinicform': clinicform,
        'cabinet_images': cabinet_images,
        'cabinet_image': cabinet_image,
        'counter': counter,
        'dentist': dentist,
        'dentist_translation': dentist_translation,
        'active_tab': active_tab,
        'success_message': success_message,
    })


def update(request, form):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL_DENTX}?next={request.path}")
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        check_language(request, "dentist")
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        dentist = DentistUser.objects.get(user=user)
        if form == "profile":
            userform = UserForm(request.POST)
            languageform = LanguageForm(request.POST)
            if userform.is_valid() and languageform.is_valid():
                user.first_name = userform.cleaned_data['first_name']
                user.last_name = userform.cleaned_data['last_name']
                dentist.gender_id = userform.cleaned_data['gender']
                year = int(userform.cleaned_data['birth_year'])
                month = MONTHS.index(userform.cleaned_data['birth_month']) + 1
                day = int(userform.cleaned_data['birth_day'])
                dentist.birthday = datetime(year, month, day)
                dentist.phone_number = userform.cleaned_data['phone_number']
                user.email = userform.cleaned_data['email']
                dentist.language_id = languageform.cleaned_data['language']
                language = Language.objects.get(pk=dentist.language_id).name
                translation.activate(language)
                request.session[translation.LANGUAGE_SESSION_KEY] = language
                user.save()
                dentist.save()
                passwordupdateform = PasswordUpdateForm(request.POST)
                request.session['success_message'] = "Updated successfully"
                return redirect("patient:settings", active_tab="profile")
        elif form == "password":
            passwordupdateform = PasswordUpdateForm(request.POST)
            if passwordupdateform.is_valid():
                if user.check_password(passwordupdateform.cleaned_data['old_password']) and passwordupdateform.cleaned_data['password'] == passwordupdateform.cleaned_data['password_confirm']:
                    username = user.username
                    user.set_password(passwordupdateform.cleaned_data['password'])
                    user.save()
                    user = authenticate(
                        request,
                        username=username,
                        password=passwordupdateform.cleaned_data['password']
                    )
                    login(request, user)
                    language = Language.objects.get(pk=dentist.language_id).name
                    translation.activate(language)
                    request.session[translation.LANGUAGE_SESSION_KEY] = language
                    request.session[user.get_username()] = user.get_username()
                    userform = UserForm(request.POST)
                    request.session['success_message'] = "Updated successfully"
                    return redirect("dentx:settings", active_tab="password")
                else:
                    request.session['incorrect_password'] = {
                        'old_password': passwordupdateform.cleaned_data['old_password'],
                        'password': passwordupdateform.cleaned_data['password'],
                        'password_confirm': passwordupdateform.cleaned_data['password_confirm']
                    }
                    userform = UserForm(request.POST)
                    languageform = LanguageForm(request.POST)
                    request.session['success_message'] = "Passwords do not match"
                    return redirect("dentx:settings", active_tab="password")
        elif form == "clinic-photo":
            # new_cabinet_image = Cabinet_Image(
            #     image=request.FILES['file'],
            #     dentist=dentist
            # )
            cabinet_images = Cabinet_Image.objects.filter(dentist=dentist)
            if len(cabinet_images) > 1:
                cabinet_image = cabinet_images[0].image.url
                cabinet_images = [ image.image.url for image in cabinet_images[1:]]
                counter = len(cabinet_images)
            elif len(cabinet_images) == 1:
                cabinet_image = cabinet_images[0].image.url
                print(type(cabinet_image))
                cabinet_images = None
                counter = 1
            else:
                cabinet_image = None
                cabinet_images = None
                counter = 0
            return JsonResponse({
                'cabinet_images': cabinet_images,
                'cabinet_image': cabinet_image,
                'counter': counter,
            }, safe=False)
        # return redirect("dentx:settings", active_tab="profile")
