from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Clinic)
admin.site.register(Clinic_translation)
admin.site.register(User)
admin.site.register(User_translation)
admin.site.register(Service)
admin.site.register(Service_translation)
admin.site.register(Cabinet_Image)
