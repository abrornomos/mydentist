from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DentistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dentist'
    verbose_name = _("Tish shifokori ma'lumotlari")
