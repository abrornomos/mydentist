from django.conf import settings
from django.shortcuts import redirect
from django.utils import translation


def set_language(request, user_language):
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    # old_full_url = request.META.get('HTTP_REFERER', '/')
    # old_url = f"/{'/'.join(old_full_url.split('/')[3:])}"
    # prefix_exists = False
    # for language in settings.EXTRA_LANGUAGES:
    #     if f"/{language[0]}/" in old_url:
    #         prefix_exists = True
    # if not prefix_exists and user_language != settings.LANGUAGE_CODE:
    #     new_url = F"/{user_language}{old_url}"
    # elif user_language == settings.LANGUAGE_CODE:
    #     new_url = old_url.replace(f"/{old_url.split('/')[1]}/", "/")
    # else:
    #     new_url = old_url.replace(f"/{old_url.split('/')[1]}/", f"/{user_language}/")
    # return redirect(new_url)
    return redirect(request.META.get('HTTP_REFERER', '/'))


# def get_ip(request):
#     address = request.META.get("HTTP_X_FORWARDED_FOR")
#     return address.split(",")[-1].strip() if address else request.META.get("REMOTE_ADDR")
