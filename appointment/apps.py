from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppointmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "appointment"
    verbose_name = _("Qabullar va so'rovlar")
