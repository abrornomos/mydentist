from django.template import Library
from patient.var import MONTHS

register = Library()


@register.simple_tag
def time_format(datetime):
    return f"{datetime.day} {MONTHS[datetime.month - 1]} {datetime.year}"
