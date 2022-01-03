from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BaseappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "baseapp"
    verbose_name = _("Asosiy ma'lumotlar")
