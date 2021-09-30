from django.contrib.auth.models import User
from django.utils import translation
from .models import User as UserExtra
from baseapp.models import Language


def check_language(request):
    language = translation.get_language()
    user = UserExtra.objects.get(user=User.objects.get(username=request.user.username))
    user_language = Language.objects.get(pk=user.language_id).name
    if user_language != language:
        translation.activate(user_language)
        request.session[translation.LANGUAGE_SESSION_KEY] = user_language
