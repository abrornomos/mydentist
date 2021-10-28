from datetime import datetime
from django.conf import settings as global_settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import translation
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import get_language, ugettext_lazy as _
from dotenv import load_dotenv
from os import getenv
from pathlib import Path
from smtplib import SMTP_SSL
from .models import *
from .forms import *
from .tokens import reset_password_token
from baseapp.models import Language, Gender
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
                    language=Language.objects.get(name=get_language()),
                    gender=Gender.objects.get(pk=userform.cleaned_data['gender'])
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
                    password=loginform.cleaned_data['password']
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
                # try:
                #     user_check = UserExtra.objects.get(phone_number=loginform.cleaned_data['email'])
                #     user_check = User.objects.get(pk=user_check.user_id)
                #     user = authenticate(
                #         request,
                #         username=user_check.username,
                #         password=request.POST['password']
                #     )
                #     if user is not None:
                #         login(request, user)
                #         user_extra = UserExtra.objects.get(user=user)
                #         translation.activate(user_extra.language)
                #         request.session[translation.LANGUAGE_SESSION_KEY] = user_extra.language
                #         request.session[user.get_username()] = user.get_username()
                #         if 'next' in request.POST:
                #             return redirect(request.POST['next'])
                #         else:
                #             return redirect("patient:profile")
                #     else:
                #         return render(request, "login/login.html", {
                #             'loginform': loginform,
                #             'error_message': _("Xato parol")
                #         })
                # except:
                return render(request, "login/login.html", {
                    'loginform': loginform,
                    'error_message': _("Xato e-mail")
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


def password_reset(request):
    if request.user.username in request.session:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    if request.method == "POST":
        emailform = EmailForm(request.POST)
        if emailform.is_valid():
            # load_dotenv(global_settings.BASE_DIR / ".env")
            # print(getenv("EMAIL_HOST"))
            # print(getenv("EMAIL_HOST_USER"))
            # print(getenv("EMAIL_HOST_PASSWORD"))
            # smtp = SMTP_SSL(getenv("EMAIL_HOST"))
            # smtp.login(getenv("EMAIL_HOST_USER"), getenv("EMAIL_HOST_PASSWORD"))
            # smtp.sendmail(getenv("EMAIL_HOST_USER"), emailform.cleaned_data['email'], "Parolni tiklash uchun quyidagi havolaga kiring")
            # smtp.quit()
            # return redirect("login:password_reset_done")
            email = emailform.cleaned_data['email']
            user = User.objects.get(email=email)
            link = f"{urlsafe_base64_encode(force_bytes(user.username))}/{reset_password_token.make_token(user)}"
            text = f"You're receiving this email because you requested a password reset for your user account at {request.META.get('HTTP_HOST')}.\n\nPlease go to the following page and choose a new password: {request.META.get('HTTP_ORIGIN')}/auth/reset/{link}\n\nYour username, in case you’ve forgotten: {user.username}\n\nThanks for using our site!"
            print(global_settings.EMAIL_HOST_USER)
            result_email = send_mail(_("Parolni tiklash"), text, global_settings.EMAIL_HOST_USER, [email])
            return redirect("login:password_reset_done")
            if result_email:
                return redirect("login:password_reset_done")
    else:
        emailform = EmailForm()
        return render(request, "login/password_reset.html", {
            'emailform': emailform
        })


def password_reset_done(request):
    if request.user.username in request.session:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, "login/password_reset_sent.html")


def reset(request, uidb64, token):
    try:
        username = force_text(urlsafe_base64_decode(uidb64))
        is_token_correct = reset_password_token.check_token(User.objects.get(username=username), token)
        if is_token_correct:
            return redirect("login:password_reset_complete")
    except:
        return Http404(_("Havolani muddati yakunlandi"))


def reset_done(request):
    if request.user.username in request.session:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, "login/password_reset_done.html")
