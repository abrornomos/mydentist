from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from pathlib import Path
from .models import *
from .forms import *
from baseapp.models import Language
from illness.models import *
from illness.forms import *
from patient.models import User as UserExtra, Illness, Other_Illness
from patient.forms import *
from patient.var import *

# Create your views here.


def register(request):
    if request.user.username in request.session:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    if request.method == "POST":
        userform = UserForm(request.POST)
        passwordform = PasswordForm(request.POST)
        illnessform = IllnessForm(request.POST)
        otherillnessform = OtherIllnessForm(request.POST)
        if userform.is_valid() and passwordform.is_valid() and illnessform.is_valid() and otherillnessform.is_valid():
            if passwordform.cleaned_data['password'] == passwordform.cleaned_data['password_confirm']:
                with open(Path(__file__).resolve().parent / "last_id.txt", "r") as file:
                    id = int(file.read()) + 1
                with open(Path(__file__).resolve().parent / "last_id.txt", "w") as file:
                    file.write(str(id))
                id = f"{id:07d}"
                user = User.objects.create_user(
                    f"user{id}",
                    email=userform.cleaned_data['email'],
                    password=passwordform.cleaned_data['password'],
                    first_name=userform.cleaned_data['name'],
                    last_name=userform.cleaned_data['last_name']
                )
                year = int(userform.cleaned_data['birth_year'])
                month = MONTHS.index(userform.cleaned_data['birth_month']) + 1
                day = int(userform.cleaned_data['birth_day'])
                user_extra = UserExtra.objects.create(
                    user=user,
                    phone_number=userform.cleaned_data['phone_number'],
                    address=userform.cleaned_data['address'],
                    birthday=datetime(year, month, day),
                    image="patients/photos/default.png",
                    language=Language.objects.get(name="ru")
                )
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
                illness = Illness.objects.create(
                    user=user_extra,
                    diabet=Diabet.objects.get(value=illnessform.cleaned_data['diabet']),
                    anesthesia=Anesthesia.objects.get(value=illnessform.cleaned_data['anesthesia']),
                    hepatitis=Hepatitis.objects.get(value=illnessform.cleaned_data['hepatitis']),
                    aids=AIDS.objects.get(value=illnessform.cleaned_data['aids']),
                    pressure=Pressure.objects.get(value=illnessform.cleaned_data['pressure']),
                    allergy=allergy,
                    asthma=Asthma.objects.get(value=illnessform.cleaned_data['asthma']),
                    dizziness=Dizziness.objects.get(value=illnessform.cleaned_data['dizziness']),
                )
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
                otherillness = Other_Illness.objects.create(
                    user=user_extra,
                    epilepsy=Epilepsy.objects.get(value=otherillnessform.cleaned_data['epilepsy']),
                    blood_disease=Blood_disease.objects.get(value=otherillnessform.cleaned_data['blood_disease']),
                    medications=medications,
                    stroke=Stroke.objects.get(value=otherillnessform.cleaned_data['stroke']),
                    heart_attack=Heart_attack.objects.get(value=otherillnessform.cleaned_data['heart_attack']),
                    oncologic=Oncologic.objects.get(value=otherillnessform.cleaned_data['oncologic']),
                    tuberculosis=Tuberculosis.objects.get(value=otherillnessform.cleaned_data['tuberculosis']),
                    alcohol=Alcohol.objects.get(value=otherillnessform.cleaned_data['alcohol']),
                    pregnancy=pregnancy,
                )
                return redirect("login:login")
            else:
                return render(request, "login/register.html", {
                    'userform': userform,
                    'passwordform': passwordform,
                    'illnessform': illnessform,
                    'otherillnessform': otherillnessform,
                    'error_message': _("Parollar to'g'ri kemayapti")
                })
        else:
            return render(request, "login/register.html", {
                'userform': userform,
                'passwordform': passwordform,
                'illnessform': illnessform,
                'otherillnessform': otherillnessform,
                'error_message': None
            })
    else:
        userform = UserForm()
        passwordform = PasswordForm()
        illnessform = IllnessForm()
        otherillnessform = OtherIllnessForm()
        return render(request, "login/register.html", {
            'userform': userform,
            'passwordform': passwordform,
            'illnessform': illnessform,
            'otherillnessform': otherillnessform,
            'error_message': None
        })


def sign_in(request):
    if request.user.username in request.session:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    if request.method == "POST":
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            try:
                user_check = User.objects.get(email=request.POST['email'])
                user = authenticate(
                    request,
                    username=user_check.username,
                    password=request.POST['password']
                )
                if user is not None:
                    login(request, user)
                    user_extra = UserExtra.objects.get(user=user)
                    language = Language.objects.get(pk=user_extra.language_id).name
                    translation.activate(language)
                    request.session[translation.LANGUAGE_SESSION_KEY] = language
                    request.session[user.get_username()] = user.get_username()
                    if 'next' in request.POST:
                        return redirect(request.POST['next'])
                    else:
                        return redirect("patient:profile")
                else:
                    return render(request, "login/login.html", {
                        'loginform': loginform,
                        'error_message': _("Xato parol")
                    })
            except:
                try:
                    user_check = UserExtra.objects.get(phone_number=loginform.cleaned_data['email'])
                    user_check = User.objects.get(pk=user_check.user_id)
                    user = authenticate(
                        request,
                        username=user_check.username,
                        password=request.POST['password']
                    )
                    if user is not None:
                        login(request, user)
                        user_extra = UserExtra.objects.get(user=user)
                        translation.activate(user_extra.language)
                        request.session[translation.LANGUAGE_SESSION_KEY] = user_extra.language
                        request.session[user.get_username()] = user.get_username()
                        if 'next' in request.POST:
                            return redirect(request.POST['next'])
                        else:
                            return redirect("patient:profile")
                    else:
                        return render(request, "login/login.html", {
                            'loginform': loginform,
                            'error_message': _("Xato parol")
                        })
                except:
                    return render(request, "login/login.html", {
                        'loginform': loginform,
                        'error_message': _("Xato telefon raqam yoki elektron manzil")
                    })
        else:
            return render(request, "login/login.html", {
                'loginform': loginform,
                'error_message': None
            })
    else:
        loginform = LoginForm()
        return render(request, "login/login.html", {
            'loginform': loginform,
            'error_message': None
        })


def sign_out(request):
    if request.user.username in request.session:
        del request.session[request.user.username]
    logout(request)
    return redirect("login:login")
