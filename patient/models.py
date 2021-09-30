from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class User(models.Model):

    user = models.ForeignKey("auth.User", verbose_name=_("Foydalanuvchi"), on_delete=models.CASCADE)
    phone_number = models.CharField(_("Telefon raqami"), max_length=25)
    address = models.CharField(_("Manzili"), max_length=255)
    birthday = models.DateField(_("Tug'ilgan sanasi"), auto_now=False, auto_now_add=False)
    image = models.ImageField(_("Rasmi"), upload_to="patients/photos/")
    language = models.ForeignKey("baseapp.Language", verbose_name=_("Tili"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Foydalanuvchi")
        verbose_name_plural = _("Foydalanuvchilar")

    def __str__(self):
        return self.user.__str__()


class Illness(models.Model):

    user = models.ForeignKey("patient.User", verbose_name=_("Foydalanuvchi"), on_delete=models.CASCADE)
    diabet = models.ForeignKey("illness.Diabet", verbose_name=_("Qandli diabet"), on_delete=models.CASCADE)
    anesthesia = models.ForeignKey("illness.Anesthesia", verbose_name=_("Narkoz"), on_delete=models.CASCADE)
    hepatitis = models.ForeignKey("illness.Hepatitis", verbose_name=_("Gepatit B"), on_delete=models.CASCADE)
    aids = models.ForeignKey("illness.AIDS", verbose_name=_("OITS"), on_delete=models.CASCADE)
    pressure = models.ForeignKey("illness.Pressure", verbose_name=_("Qon bosimi"), on_delete=models.CASCADE)
    allergy = models.ForeignKey("illness.Allergy", verbose_name=_("Allergiya"), on_delete=models.CASCADE)
    asthma = models.ForeignKey("illness.Asthma", verbose_name=_("Bronxial astma"), on_delete=models.CASCADE)
    dizziness = models.ForeignKey("illness.Dizziness", verbose_name=_("Bosh aylanishi"), on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = _("Foydalanuvchi kasalliklari")

    def __str__(self):
        return self.name


class Other_Illness(models.Model):

    user = models.ForeignKey("patient.User", verbose_name=_("Foydalanuvchi"), on_delete=models.CASCADE)
    epilepsy = models.ForeignKey("illness.Epilepsy", verbose_name=_("Epilepsiya"), on_delete=models.CASCADE)
    blood_disease = models.ForeignKey("illness.Blood_disease", verbose_name=_("Qon kasali"), on_delete=models.CASCADE)
    medications = models.ForeignKey("illness.Medications", verbose_name=_("Doimiy dorilar"), on_delete=models.CASCADE)
    stroke = models.ForeignKey("illness.Stroke", verbose_name=_("Insultga uchraganmisiz?"), on_delete=models.CASCADE)
    heart_attack = models.ForeignKey("illness.Heart_attack", verbose_name=_("Yurak xurujiga uchraganmisiz?"), on_delete=models.CASCADE)
    oncologic = models.ForeignKey("illness.Oncologic", verbose_name=_("Onkologik kasalliklar"), on_delete=models.CASCADE)
    tuberculosis = models.ForeignKey("illness.Tuberculosis", verbose_name=_("Sil kasalligi"), on_delete=models.CASCADE)
    alcohol = models.ForeignKey("illness.Alcohol", verbose_name=_("Spirtli ichimlik ichasizmi?"), on_delete=models.CASCADE)
    pregnancy = models.ForeignKey("illness.Pregnancy", verbose_name=_("Homiladorlik"), on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = _("Foydalanuvchi kasalliklari")

    def __str__(self):
        return self.name
