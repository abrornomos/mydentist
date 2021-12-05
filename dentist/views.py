from django.conf import settings as global_settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from django.utils.translation import get_language
from appointment.models import Appointment, Query
from baseapp.models import *
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
        counter = range(len(cabinet_images))
        cabinet_image = cabinet_images[0]
        cabinet_images = cabinet_images[1:]
    elif len(cabinet_images) == 1:
        counter = range(1)
        cabinet_image = cabinet_images[0]
        cabinet_images = None
    else:
        counter = 0
        cabinet_image = None
        cabinet_images = None
    return render(request, "dentist/dentist.html", {
        'clinic': clinic,
        'clinic_extra': clinic_extra,
        'dentist': dentist,
        'dentist_extra': dentist_extra,
        'services': services,
        'cabinet_image': cabinet_image,
        'cabinet_images': cabinet_images,
        'counter': counter,
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
        elif request.session['success_message'] == "Added successfully":
            success_message = "Added successfully"
        elif request.session['success_message'] == "Passwords do not match":
            success_message = "Passwords do not match"
        del request.session['success_message']
    else:
        success_message = None
    user = User.objects.get(username=request.user.username)
    dentist = DentistUser.objects.get(user=user)
    dentist_translation = DentistUserTranslation.objects.filter(
        dentist=dentist,
        language__pk=dentist.language_id
    )[0]
    clinic = Clinic.objects.get(pk=dentist.clinic_id)
    clinic_uz = Clinic_translation.objects.get(
        clinic=clinic,
        language__name="uz"
    )
    clinic_ru = Clinic_translation.objects.get(
        clinic=clinic,
        language__name="ru"
    )
    services_obj = Service.objects.filter(dentist=dentist)
    services = []
    for service in services_obj:
        service_uz = Service_translation.objects.get(service=service, language__name="uz")
        service_ru = Service_translation.objects.get(service=service, language__name="ru")
        services.append({
            'name_uz': service_uz.name,
            'name_ru': service_ru.name,
            'duration': service.duration,
            'price': service.price
        })
    cabinet_images = Cabinet_Image.objects.filter(dentist=dentist)
    if len(cabinet_images) > 1:
        counter = range(len(cabinet_images))
        cabinet_image = cabinet_images[0]
        cabinet_images = cabinet_images[1:]
    elif len(cabinet_images) == 1:
        counter = range(1)
        cabinet_image = cabinet_images[0]
        cabinet_images = None
    else:
        counter = 0
        cabinet_image = None
        cabinet_images = None
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
    clinics_obj = Clinic.objects.all()
    clinics = []
    for clinic_obj in clinics_obj:
        clinics.append(
            Clinic_translation.objects.get(
                clinic=clinic_obj,
                language__pk=dentist.language_id
            )
        )
        if clinic_obj.id == dentist.clinic_id:
            active_clinic = clinic_obj
    print(active_clinic)
    clinicform = ClinicForm({
        'clinic_name_uz': clinic_uz.name,
        'clinic_name_ru': clinic_ru.name,
        'address_uz': clinic_uz.address,
        'address_ru': clinic_ru.address,
        'orientir_uz': clinic_uz.orientir,
        'orientir_ru': clinic_ru.orientir,
        'region': clinic.region_id,
        'latitude': clinic.latitude,
        'longitude': clinic.longitude,
        'worktime_begin': dentist.worktime_begin,
        'worktime_end': dentist.worktime_end,
    })
    if 'incorrect_password' in request.session:
        passwordupdateform = PasswordUpdateForm(request.session['incorrect_password'])
        del request.session['incorrect_password']
    else:
        passwordupdateform = PasswordUpdateForm()
    serviceform = ServiceForm()
    return render(request, "dentist/settings.html", {
        'userform': userform,
        'languageform': languageform,
        'passwordupdateform': passwordupdateform,
        'clinicform': clinicform,
        'serviceform': serviceform,
        'clinics': clinics,
        'active_clinic': active_clinic,
        'cabinet_images': cabinet_images,
        'cabinet_image': cabinet_image,
        'counter': counter,
        'services': services,
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
                request.session['success_message'] = "Updated successfully"
                return redirect("dentx:settings", active_tab="profile")
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
        elif form == "clinic":
            clinicform = ClinicForm(request.POST)
            if clinicform.is_valid():
                if request.POST['clinic'] == 'other':
                    try:
                        latitude = float(clinicform.cleaned_data['latitude'])
                        longitude = float(clinicform.cleaned_data['longitude'])
                    except ValueError:
                        latitude = float(clinicform.cleaned_data['latitude'].replace(",", "."))
                        longitude = float(clinicform.cleaned_data['longitude'].replace(",", "."))
                    except Exception:
                        raise HttpResponseForbidden
                    clinic = Clinic.objects.create(
                        name=clinicform.cleaned_data['clinic_name_uz'],
                        region=Region.objects.get(pk=clinicform.cleaned_data['region']),
                        latitude=latitude,
                        longitude=longitude
                    )
                    clinic_uz = Clinic_translation.objects.create(
                        clinic=clinic,
                        name=clinicform.cleaned_data['clinic_name_uz'],
                        address=clinicform.cleaned_data['address_uz'],
                        orientir=clinicform.cleaned_data['orientir_uz'],
                        language=Language.objects.get(name="uz")
                    )
                    clinic_ru = Clinic_translation.objects.create(
                        clinic=clinic,
                        name=clinicform.cleaned_data['clinic_name_ru'],
                        address=clinicform.cleaned_data['address_ru'],
                        orientir=clinicform.cleaned_data['orientir_ru'],
                        language=Language.objects.get(name="ru")
                    )
                    dentist.clinic_id = clinic.id
                    dentist.save()
                    request.session['success_message'] = "Added successfully"
                    return redirect("dentx:settings", active_tab="clinic")
                if request.POST['clinic'] == "other":
                    clinic = Clinic.objects.create(
                        name=clinicform.cleaned_data['clinic_name_uz']
                    )
                else:
                    clinic_translation = Clinic_translation.objects.get(
                        name=request.POST['clinic'],
                        language__pk=dentist.language_id
                    )
                    print(clinic_translation)
                    clinic = Clinic.objects.get(
                        pk=clinic_translation.clinic_id
                    )
                    dentist.clinic_id = clinic.id
                    dentist.save()
                    request.session['success_message'] = "Updated successfully"
                    return redirect("dentx:settings", active_tab="clinic")
            else:
                print(clinicform.errors)
                print(float(request.POST['latitude'].replace(",", ".")))
                print(float(request.POST['longitude'].replace(",", ".")))
                request.session['success_message'] = "Updated successfully"
                return redirect("dentx:settings", active_tab="clinic")
        elif form == "clinic-photo":
            new_cabinet_image = Cabinet_Image.objects.create(
                image=request.FILES['file'],
                dentist=dentist
            )
            cabinet_images = Cabinet_Image.objects.filter(dentist=dentist)
            if len(cabinet_images) > 1:
                counter = len(cabinet_images)
                cabinet_image = cabinet_images[0].image.url
                cabinet_images = [ image.image.url for image in cabinet_images[1:]]
            elif len(cabinet_images) == 1:
                counter = 1
                cabinet_image = cabinet_images[0].image.url
                cabinet_images = None
            else:
                counter = 0
                cabinet_image = None
                cabinet_images = None
            return JsonResponse({
                'cabinet_images': cabinet_images,
                'cabinet_image': cabinet_image,
                'counter': counter,
            }, safe=False)
        elif form == "services":
            serviceform = ServiceForm(request.POST)
            if serviceform.is_valid():
                service = Service.objects.create(
                    name=serviceform.cleaned_data['name_uz'],
                    duration=serviceform.cleaned_data['duration'],
                    price=serviceform.cleaned_data['price'],
                    dentist=dentist
                )
                service_uz = Service_translation.objects.create(
                    service=service,
                    language=Language.objects.get(name="uz"),
                    name=serviceform.cleaned_data['name_uz'],
                )
                service_ru = Service_translation.objects.create(
                    service=service,
                    language=Language.objects.get(name="ru"),
                    name=serviceform.cleaned_data['name_ru'],
                )
                service.save()
                service_uz.save()
                service_ru.save()
                serviceform = ServiceForm()
                request.session['success_message'] = "Updated successfully"
                return redirect("dentx:settings", active_tab="services")
        return redirect("dentx:settings", active_tab="profile")


def get_clinic(request):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL_DENTX}?next={request.path}")
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        check_language(request, "dentist")
    dentist = DentistUser.objects.get(user__username=request.user.username)
    clinic_translation = Clinic_translation.objects.get(
        name=request.POST['clinic'],
        language__pk=dentist.language_id
    )
    if clinic_translation.language_id == 1:
        clinic_uz = clinic_translation
        clinic_ru = Clinic_translation.objects.get(
            clinic__pk=clinic_translation.clinic_id,
            language__pk=2
        )
    elif clinic_translation.language_id == 2:
        clinic_uz = Clinic_translation.objects.get(
            clinic__pk=clinic_translation.clinic_id,
            language__pk=1
        )
        clinic_ru = clinic_translation
    clinic = Clinic.objects.get(pk=clinic_translation.clinic_id)
    return JsonResponse({
        'name_uz': clinic_uz.name,
        'name_ru': clinic_ru.name,
        'address_uz': clinic_uz.address,
        'address_ru': clinic_ru.address,
        'orientir_uz': clinic_uz.orientir,
        'orientir_ru': clinic_ru.orientir,
        'region': clinic.region_id,
        'latitude': clinic.latitude,
        'longitude': clinic.longitude,
    }, safe=False)
