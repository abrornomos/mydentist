from django.template import Library
from django.utils.translation import get_language

register = Library()


@register.simple_tag
def convert_time(minutes):
    time = ""
    language = get_language()
    if language == "uz":
        if minutes // 60 != 0:
            time += f"{str(minutes // 60)} soat"
        if minutes % 60 != 0:
            time += f"{str(minutes % 60)} daqiqa"
    elif language == "ru":
        if minutes // 60 != 0:
            time += f"{str(minutes // 60)} час"
        if minutes % 60 != 0:
            time += f"{str(minutes % 60)} минут"
    return time
