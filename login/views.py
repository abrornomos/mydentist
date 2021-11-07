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
from pathlib import Path
from baseapp.models import Language, Gender
from illness.models import *
from illness.forms import *
from patient.models import User as UserExtra, Illness, Other_Illness
from patient.forms import *
from mydentist.var import *
from .models import *
from .forms import *
from .tokens import reset_password_token

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
                    patient=user_extra,
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
                    patient=user_extra,
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
            email = emailform.cleaned_data['email']
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.username))
            token = reset_password_token.make_token(user)
            password_reset = PasswordReset.objects.create(
                email=email,
                uidb64=uidb64,
                token=token,
                is_active=True
            )
            text = f"You're receiving this email because you requested a password reset for your user account at {request.META.get('HTTP_HOST')}.\n\nPlease go to the following page and choose a new password: {request.META.get('HTTP_ORIGIN')}/auth/reset/{uidb64}/{token}\n\nThanks for using our site!"
            result_email = send_mail(_("Parolni tiklash"), text, global_settings.EMAIL_HOST_USER, [email])
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
        user = User.objects.get(username=force_text(urlsafe_base64_decode(uidb64)))
        is_token_correct = reset_password_token.check_token(user, token)
        if is_token_correct:
            try:
                password_reset = PasswordReset.objects.get(
                    email=user.email,
                    uidb64=uidb64,
                    token=token
                )
                if password_reset.is_active:
                    if request.method == "POST":
                        passwordform = PasswordForm(request.POST)
                        if passwordform.is_valid():
                            if passwordform.cleaned_data['password'] == passwordform.cleaned_data['password_confirm']:
                                user.set_password(passwordform.cleaned_data['password'])
                                user.save()
                                password_reset.is_active = False
                                password_reset.save()
                                return redirect("login:password_reset_complete")
                            else:
                                passwordform = PasswordForm(request.POST)
                                return render(request, "login/password_reset_form.html", {
                                    'passwordform': passwordform,
                                    'error_message': _("Parollar mos kelmayapti")
                                })
                        else:
                            passwordform = PasswordForm(request.POST)
                            return render(request, "login/password_reset_form.html", {
                                'passwordform': passwordform,
                                'error_message': None
                            })
                    else:
                        passwordform = PasswordForm()
                        return render(request, "login/password_reset_form.html", {
                            'passwordform': passwordform,
                            'error_message': None
                        })
                else:
                    raise Http404(_("Havolani muddati yakunlandi"))
            except:
                raise Http404(_("Havolani muddati yakunlandi"))
        else:
            raise Http404(_("Havolani muddati yakunlandi"))
    except:
        raise Http404(_("Havolani muddati yakunlandi"))


def reset_done(request):
    if request.user.username in request.session:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, "login/password_reset_done.html")


def dentx_login(request):
    if request.method == "POST":
        loginform = DentXLoginForm(request.POST)
        if loginform.is_valid():
            user = authenticate(
                request,
                username=loginform.cleaned_data['username'],
                password=loginform.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                request.session[user.get_username()] = user.get_username()
                return redirect("dentx:appointments")
            else:
                return render(request, "login/dentx_login.html", {
                    'loginform': loginform,
                    'error_message': _("Noto'g'ri login yoki parol")
                })
        else:
            loginform = DentXLoginForm()
            return render(request, "login/dentx_login.html", {
                'loginform': loginform,
                'error_message': None
            })
    else:
        loginform = DentXLoginForm()
        return render(request, "login/dentx_login.html", {
            'loginform': loginform,
            'error_message': None
        })


def dentx_logout(request):
    if request.user.username in request.session:
        del request.session[request.user.username]
    logout(request)
    return redirect("dentx:login")
