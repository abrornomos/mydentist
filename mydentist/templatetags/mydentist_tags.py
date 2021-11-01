from django.template import Library
from django.utils.translation import get_language
from mydentist.var import MONTHS

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


@register.simple_tag
def date_format(datetime):
    return f"{datetime.day} {MONTHS[datetime.month - 1]} {datetime.year}"


@register.simple_tag
def time_format(datetime):
    return f"{datetime.hour}:{datetime.minute:02d}"
