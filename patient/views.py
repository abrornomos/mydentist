from django.conf import settings as global_settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, date
from appointment.models import Query, Appointment
from baseapp.models import Language
from dentist.models import User as DentistUser, User_translation, Clinic, Clinic_translation, Service, Service_translation, Cabinet_Image
from illness.models import *
from illness.forms import *
from login.forms import PasswordUpdateForm
from mydentist.handler import *
from mydentist.var import *
from .forms import *
from .models import User as PatientUser, Illness, Other_Illness

# Create your views here.


def profile(request):
    if not is_authenticated(request, "patient"):
        if not is_authenticated(request, "dentist"):
            return redirect(f"{global_settings.LOGIN_URL}?next={request.path}")
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        check_language(request, "patient")
    user = User.objects.get(username=request.user.username)
    user_extra = PatientUser.objects.get(user=user)
    try:
        try:
            appointment = Appointment.objects.get(patient=user_extra)
            query = None
            dentist = DentistUser.objects.get(pk=appointment.dentist_id)
            dentist_extra = User_translation.objects.get(dentist=dentist, language__pk=user_extra.language_id)
            clinic = Clinic.objects.get(pk=dentist.clinic_id)
            clinic_extra = Clinic_translation.objects.get(clinic=clinic, language__pk=user_extra.language_id)
            cabinet_images = Cabinet_Image.objects.filter(dentist__pk=dentist.id)
            try:
                services_obj = Service_translation.objects.filter(language__pk=user_extra.language_id, service__dentist=dentist)
                services = []
                for service_extra in services_obj:
                    services.append({
                        'service': Service.objects.get(pk=service_extra.service_id),
                        'service_extra': service_extra
                    })
            except:
                services = []
        except:
            appointment = None
            query = Query.objects.get(patient=user_extra)
            dentist = DentistUser.objects.get(pk=query.dentist_id)
            dentist_extra = User_translation.objects.get(dentist=dentist, language__pk=user_extra.language_id)
            clinic = Clinic.objects.get(pk=dentist.clinic_id)
            clinic_extra = Clinic_translation.objects.get(clinic=clinic, language__pk=user_extra.language_id)
            cabinet_images = Cabinet_Image.objects.filter(dentist__pk=dentist.id)
            try:
                services_obj = Service_translation.objects.filter(language__pk=user_extra.language_id, service__dentist=dentist)
                services = []
                for service_extra in services_obj:
                    services.append({
                        'service': Service.objects.get(pk=service_extra.service_id),
                        'service_extra': service_extra
                    })
            except:
                services = []
    except:
        appointment = None
        query = None
        dentist = None
        dentist_extra = None
        clinic = None
        clinic_extra = None
        cabinet_images = []
        services = []
    authenticated = is_authenticated(request, "patient")
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
    if len(cabinet_images) > 1:
        return render(request, "patient/profile.html", {
            'user_extra': user_extra,
            'appointment': appointment,
            'dentist': dentist,
            'dentist_extra': dentist_extra,
            'clinic': clinic,
            'clinic_extra': clinic_extra,
            'services': services,
            'cabinet_image': cabinet_images[0],
            'cabinet_images': cabinet_images[1:],
            'counter': range(len(cabinet_images)),
            'authenticated': authenticated,
        })
    elif len(cabinet_images) == 1:
        return render(request, "patient/profile.html", {
            'user_extra': user_extra,
            'appointment': appointment,
            'dentist': dentist,
            'dentist_extra': dentist_extra,
            'clinic': clinic,
            'clinic_extra': clinic_extra,
            'services': services,
            'cabinet_image': cabinet_images[0],
            'cabinet_images': None,
            'counter': range(len(cabinet_images)),
            'authenticated': authenticated,
        })
    else:
        return render(request, "patient/profile.html", {
            'user_extra': user_extra,
            'appointment': appointment,
            'dentist': dentist,
            'dentist_extra': dentist_extra,
            'clinic': clinic,
            'clinic_extra': clinic_extra,
            'services': services,
            'cabinet_images': None,
            'counter': 0,
            'authenticated': authenticated,
        })


def settings(request, active_tab="profile"):
    if not is_authenticated(request, "patient"):
        if not is_authenticated(request, "dentist"):
            return redirect(f"{global_settings.LOGIN_URL}?next={request.path}")
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        check_language(request, "patient")
    if 'success_message' in request.session:
        if request.session['success_message'] == "Updated successfully":
            success_message = "Updated successfully"
        elif request.session['success_message'] == "Passwords do not match":
            success_message = "Passwords do not match"
        del request.session['success_message']
    else:
        success_message = None
    user = User.objects.get(username=request.user.username)
    user_extra = PatientUser.objects.get(user=user)
    userform = UserForm({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'gender': user_extra.gender_id,
        'birth_year': user_extra.birthday.year,
        'birth_month': MONTHS[user_extra.birthday.month - 1],
        'birth_day': user_extra.birthday.day,
        'phone_number': user_extra.phone_number,
        'email': user.email,
        'address': user_extra.address,
    })
    languageform = LanguageForm({
        'language': user_extra.language_id
    })
    if 'incorrect_password' in request.session:
        passwordupdateform = PasswordUpdateForm(request.session['incorrect_password'])
        del request.session['incorrect_password']
    else:
        passwordupdateform = PasswordUpdateForm()
    illness = Illness.objects.get(patient=user_extra)
    illnessform = IllnessForm({
        'diabet': Diabet.objects.get(pk=illness.diabet_id).value,
        'anesthesia': Anesthesia.objects.get(pk=illness.anesthesia_id).value,
        'hepatitis': Hepatitis.objects.get(pk=illness.hepatitis_id).value,
        'aids': AIDS.objects.get(pk=illness.aids_id).value,
        'pressure': Pressure.objects.get(pk=illness.pressure_id).value,
        'allergy': Allergy.objects.get(pk=illness.allergy_id).value,
        'allergy_detail': Allergy.objects.get(pk=illness.allergy_id).desc,
        'asthma': Asthma.objects.get(pk=illness.asthma_id).value,
        'dizziness': Dizziness.objects.get(pk=illness.dizziness_id).value,
    })
    otherillness = Other_Illness.objects.get(patient=user_extra)
    otherillnessform = OtherIllnessForm({
        'epilepsy': Epilepsy.objects.get(pk=otherillness.epilepsy_id).value,
        'blood_disease': Blood_disease.objects.get(pk=otherillness.blood_disease_id).value,
        'medications': Medications.objects.get(pk=otherillness.medications_id).value,
        'medications_detail': Medications.objects.get(pk=otherillness.medications_id).desc,
        'stroke': Stroke.objects.get(pk=otherillness.stroke_id).value,
        'heart_attack': Heart_attack.objects.get(pk=otherillness.heart_attack_id).value,
        'oncologic': Oncologic.objects.get(pk=otherillness.oncologic_id).value,
        'tuberculosis': Tuberculosis.objects.get(pk=otherillness.tuberculosis_id).value,
        'alcohol': Alcohol.objects.get(pk=otherillness.alcohol_id).value,
        'pregnancy': Pregnancy.objects.get(pk=otherillness.pregnancy_id).value,
        'pregnancy_detail': Pregnancy.objects.get(pk=otherillness.pregnancy_id).desc,
    })
    authenticated = is_authenticated(request, "patient")
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
    return render(request, "patient/settings.html", {
        'userform': userform,
        'languageform': languageform,
        'passwordupdateform': passwordupdateform,
        'illnessform': illnessform,
        'otherillnessform': otherillnessform,
        'active_tab': active_tab,
        'success_message': success_message,
        'authenticated': authenticated,
    })


def update(request, form):
    if not is_authenticated(request, "patient"):
        if not is_authenticated(request, "dentist"):
            return redirect(f"{global_settings.LOGIN_URL}?next={request.path}")
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        check_language(request, "patient")
    if request.method == "POST":
        if form == "profile":
            userform = UserForm(request.POST)
            languageform = LanguageForm(request.POST)
            if userform.is_valid() and languageform.is_valid():
                user = User.objects.get(username=request.user.username)
                user_extra = PatientUser.objects.get(user=user)
                user.first_name = userform.cleaned_data['first_name']
                user.last_name = userform.cleaned_data['last_name']
                user_extra.gender_id = userform.cleaned_data['gender']
                year = int(userform.cleaned_data['birth_year'])
                month = MONTHS.index(userform.cleaned_data['birth_month']) + 1
                day = int(userform.cleaned_data['birth_day'])
                user_extra.birthday = datetime(year, month, day)
                user_extra.phone_number = userform.cleaned_data['phone_number']
                user.email = userform.cleaned_data['email']
                user_extra.address = userform.cleaned_data['address']
                user_extra.language_id = languageform.cleaned_data['language']
                language = Language.objects.get(pk=user_extra.language_id).name
                translation.activate(language)
                request.session[translation.LANGUAGE_SESSION_KEY] = language
                user.save()
                user_extra.save()
                passwordupdateform = PasswordUpdateForm(request.POST)
                illnessform = IllnessForm(request.POST)
                otherillnessform = OtherIllnessForm(request.POST)
                request.session['success_message'] = "Updated successfully"
                return redirect("patient:settings", active_tab="profile")
        elif form == "password":
            passwordupdateform = PasswordUpdateForm(request.POST)
            if passwordupdateform.is_valid():
                user = User.objects.get(username=request.user.username)
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
                    userform = UserForm(request.POST)
                    illnessform = IllnessForm(request.POST)
                    otherillnessform = OtherIllnessForm(request.POST)
                    request.session['success_message'] = "Updated successfully"
                    return redirect("patient:settings", active_tab="password")
                else:
                    request.session['incorrect_password'] = {
                        'old_password': passwordupdateform.cleaned_data['old_password'],
                        'password': passwordupdateform.cleaned_data['password'],
                        'password_confirm': passwordupdateform.cleaned_data['password_confirm']
                    }
                    userform = UserForm(request.POST)
                    illnessform = IllnessForm(request.POST)
                    otherillnessform = OtherIllnessForm(request.POST)
                    request.session['success_message'] = "Passwords do not match"
                    return redirect("patient:settings", active_tab="password")
        elif form == "illness":
            illnessform = IllnessForm(request.POST)
            if illnessform.is_valid():
                user = User.objects.get(username=request.user.username)
                user_extra = PatientUser.objects.get(user=user)
                illness = Illness.objects.get(user=user_extra)
                if illnessform.cleaned_data['allergy'] == 2:
                    try:
                        allergy = Allergy.objects.get(
                            value=illnessform.cleaned_data['allergy'],
                            desc=illnessform.cleaned_data['allergy_detail'],
                        )
                    except:
                        allergy = Allergy.objects.create(
                            value=illnessform.cleaned_data['allergy'],
                            desc=illnessform.cleaned_data['allergy_detail'],
                        )
                else:
                    allergy = Allergy.objects.get(
                        value=illnessform.cleaned_data['allergy'],
                    )
                illness.diabet_id = Diabet.objects.get(value=illnessform.cleaned_data['diabet']).id
                illness.anesthesia_id = Anesthesia.objects.get(value=illnessform.cleaned_data['anesthesia']).id
                illness.hepatitis_id = Hepatitis.objects.get(value=illnessform.cleaned_data['hepatitis']).id
                illness.aids_id = AIDS.objects.get(value=illnessform.cleaned_data['aids']).id
                illness.pressure_id = Pressure.objects.get(value=illnessform.cleaned_data['pressure']).id
                illness.allergy_id = allergy.id
                illness.asthma_id = Asthma.objects.get(value=illnessform.cleaned_data['asthma']).id
                illness.dizziness_id = Dizziness.objects.get(value=illnessform.cleaned_data['dizziness']).id
                illness.save()
                userform = UserForm(request.POST)
                passwordupdateform = PasswordUpdateForm(request.POST)
                otherillnessform = OtherIllnessForm(request.POST)
                request.session['success_message'] = "Updated successfully"
                return redirect("patient:settings", active_tab="illness")
        elif form == "other-illness":
            otherillnessform = OtherIllnessForm(request.POST)
            if otherillnessform.is_valid():
                user = User.objects.get(username=request.user.username)
                user_extra = PatientUser.objects.get(user=user)
                otherillness = Other_Illness.objects.get(user=user_extra)
                if otherillnessform.cleaned_data['medications'] == 2:
                    try:
                        medications = Medications.objects.get(
                            value=otherillnessform.cleaned_data['medications'],
                            desc=otherillnessform.cleaned_data['medications_detail'],
                        )
                    except:
                        medications = Medications.objects.create(
                            value=otherillnessform.cleaned_data['medications'],
                            desc=otherillnessform.cleaned_data['medications_detail'],
                        )
                else:
                    medications = Medications.objects.get(
                        value=otherillnessform.cleaned_data['medications'],
                    )
                if otherillnessform.cleaned_data['pregnancy'] == 2:
                    try:
                        pregnancy = Pregnancy.objects.get(
                            value=otherillnessform.cleaned_data['pregnancy'],
                            desc=otherillnessform.cleaned_data['pregnancy_detail'],
                        )
                    except:
                        pregnancy = Pregnancy.objects.create(
                            value=otherillnessform.cleaned_data['pregnancy'],
                            desc=otherillnessform.cleaned_data['pregnancy_detail'],
                        )
                else:
                    pregnancy = Pregnancy.objects.get(
                        value=otherillnessform.cleaned_data['pregnancy'],
                    )
                otherillness.epilepsy_id = Epilepsy.objects.get(value=otherillnessform.cleaned_data['epilepsy']).id
                otherillness.blood_disease_id = Blood_disease.objects.get(value=otherillnessform.cleaned_data['blood_disease']).id
                otherillness.medications_id = medications.id
                otherillness.stroke_id = Stroke.objects.get(value=otherillnessform.cleaned_data['stroke']).id
                otherillness.heart_attack_id = Heart_attack.objects.get(value=otherillnessform.cleaned_data['heart_attack']).id
                otherillness.oncologic_id = Oncologic.objects.get(value=otherillnessform.cleaned_data['oncologic']).id
                otherillness.tuberculosis_id = Tuberculosis.objects.get(value=otherillnessform.cleaned_data['tuberculosis']).id
                otherillness.alcohol_id = Alcohol.objects.get(value=otherillnessform.cleaned_data['alcohol']).id
                otherillness.pregnancy_id = pregnancy.id
                otherillness.save()
                userform = UserForm(request.POST)
                passwordupdateform = PasswordUpdateForm(request.POST)
                illnessform = IllnessForm(request.POST)
                request.session['success_message'] = "Updated successfully"
                return redirect("patient:settings", active_tab="other-illness")
        return redirect("patient:settings", active_tab="profile")


def patients(request):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL}?next={request.path}")
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        check_language(request, "dentist")
    user = User.objects.get(username=request.user.username)
    dentist = DentistUser.objects.get(user=user)
    patients_obj = PatientUser.objects.all()
    results = []
    for patient_obj in patients_obj:
        results.append({
            'patient': User.objects.get(pk=patient_obj.user_id),
            'patient_extra': patient_obj,
            'gender': GENDERS[patient_obj.gender_id - 1]
        })
    patientform = PatientForm()
    return render(request, "patient/patients.html", {
        'dentist': dentist,
        'results': results,
        'patientform': patientform
    })


def patient(request, id):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL}?next={request.path}")
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        check_language(request, "dentist")
    user = User.objects.get(username=request.user.username)
    dentist = DentistUser.objects.get(user=user)
    patient_extra = PatientUser.objects.get(pk=id)
    patient = User.objects.get(pk=patient_extra.user_id)
    patient_illness = Illness.objects.get(patient=patient_extra)
    patient_other_illness = Other_Illness.objects.get(patient=patient_extra)
    year = (date.today() - patient_extra.birthday).days // 365
    return render(request, "patient/patient.html", {
        'dentist': dentist,
        'patient': patient,
        'patient_extra': patient_extra,
        'patient_illness': patient_illness,
        'patient_other_illness': patient_other_illness,
        'year': year
    })

