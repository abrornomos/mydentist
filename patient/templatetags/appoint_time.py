from django.template import Library

register = Library()


@register.simple_tag
def appoint_time(datetime):
    return f"{datetime.hour}:{datetime.minute}"
