from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Illness)
admin.site.register(Other_Illness)
admin.site.register(Tooth)
admin.site.register(Tooth_status)
admin.site.register(Plan)
admin.site.register(Process_photo)
