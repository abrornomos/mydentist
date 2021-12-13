from django.template import Library
from django.utils.translation import get_language, ugettext_lazy as _
from illness.models import Allergy, Medications, Pregnancy
from mydentist.var import *

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


@register.simple_tag
def get_gender(gender_id):
    return GENDERS[gender_id - 1]


@register.simple_tag
def get_option(select, index):
    options = CHOICES[select]
    if select == "allergy" and index != 1:
        return Allergy.objects.get(pk=index).desc
    elif select == "medications" and index != 1:
        return Medications.objects.get(pk=index).desc
    elif select == "pregnancy" and index != 1:
        return f"{Pregnancy.objects.get(pk=index).desc}-{_('oy')}"
    else:
        for option in options:
            if int(option[0]) == index:
                if select == "anesthesia" and index in [1, 2]:
                    return f"{option[1]} {_('marta')}"
                else:
                    return option[1]
        return None


@register.simple_tag
def get_message(notification):
    if notification.type == "query":
        messages = notification.message.split(NEW_LINE)
        message = f"{_('Sabab')}: {messages[0]}{NEW_LINE}{_('Izohlar')}: {messages[1]}"
    else:
        message = notification.message
    return message
