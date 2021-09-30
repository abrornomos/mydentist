from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import *


admin.site.site_header = _("MyDentist sayti boshqaruvi")
admin.site.site_title = _("MyDentist sayti boshqaruvi")

# Register your models here.
admin.site.register(Language)
