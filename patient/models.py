from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(models.Model):
    user = models.OneToOneField("auth.User", verbose_name=_("Bemor"), on_delete=models.CASCADE, related_name="patient_user")
    phone_number = models.CharField(_("Telefon raqami"), max_length=50)
    gender = models.ForeignKey("baseapp.Gender", verbose_name=_("Jins"), on_delete=models.CASCADE, related_name="patient_gender")
    address = models.CharField(_("Manzil"), max_length=255)
    birthday = models.DateField(_("Tug'ilgan sanasi"), auto_now=False, auto_now_add=False)
    image = models.ImageField(_("Rasmi"), upload_to="patients/photos/")
    language = models.ForeignKey("baseapp.Language", verbose_name=_("Tili"), on_delete=models.CASCADE, related_name="patient_language")

    class Meta:
        verbose_name = _("Bemor")
        verbose_name_plural = _("Bemorlar")

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


class Illness(models.Model):

    patient = models.OneToOneField("patient.User", verbose_name=_("Bemor"), on_delete=models.CASCADE)
    diabet = models.ForeignKey("illness.Diabet", verbose_name=_("Qandli diabet"), on_delete=models.CASCADE)
    anesthesia = models.ForeignKey("illness.Anesthesia", verbose_name=_("Narkoz"), on_delete=models.CASCADE)
    hepatitis = models.ForeignKey("illness.Hepatitis", verbose_name=_("Gepatit B"), on_delete=models.CASCADE)
    aids = models.ForeignKey("illness.AIDS", verbose_name=_("OITS"), on_delete=models.CASCADE)
    pressure = models.ForeignKey("illness.Pressure", verbose_name=_("Qon bosimi"), on_delete=models.CASCADE)
    allergy = models.ForeignKey("illness.Allergy", verbose_name=_("Allergiya"), on_delete=models.CASCADE)
    asthma = models.ForeignKey("illness.Asthma", verbose_name=_("Bronxial astma"), on_delete=models.CASCADE)
    dizziness = models.ForeignKey("illness.Dizziness", verbose_name=_("Bosh aylanishi"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Bemor kasalligi")
        verbose_name_plural = _("Bemor kasalliklari")

    def __str__(self):
        return self.patient.__str__()


class Other_Illness(models.Model):

    patient = models.OneToOneField("patient.User", verbose_name=_("Bemor"), on_delete=models.CASCADE)
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
        verbose_name = _("Bemor kasalligi")
        verbose_name_plural = _("Bemor kasalliklari")

    def __str__(self):
        return self.patient.__str__()


class Tooth(models.Model):
    code = models.IntegerField(_("Tish raqami"))
    status = models.ForeignKey("patient.Tooth_status", verbose_name=_("Tish holati"), on_delete=models.CASCADE, related_name="patient_tooth_status")
    patient = models.ForeignKey("patient.User", verbose_name=_("Bemor"), on_delete=models.CASCADE, related_name="patient_tooth")

    class Meta:
        verbose_name = _("Tish")
        verbose_name_plural = _("Tishlar")

    def __str__(self):
        return f"{self.code}-{_('tish')} - {self.status} ({self.patient.__str__()})"


class Tooth_status(models.Model):
    name = models.CharField(_("Holat nomi"), max_length=100)
    prefix = models.CharField(_("Holat qo'shimchasi"), max_length=50)

    class Meta:
        verbose_name = _("Tish holati")
        verbose_name_plural = _("Tish holatlari")

    def __str__(self):
        return self.name


class Plan(models.Model):
    name = models.CharField(_("Ish nomi"), max_length=100)
    is_done = models.BooleanField(_("Qilinganligi"))
    patient = models.ForeignKey("patient.User", verbose_name=_("Bemor"), on_delete=models.CASCADE, related_name="patient_plan")

    class Meta:
        verbose_name = _("Qilingan ish")
        verbose_name_plural = _("Qilingan ishlar")

    def __str__(self):
        return f"{self.name} - {self.patient.__str__()}"


class Process_photo(models.Model):
    image = models.ImageField(_("Ish jarayonidagi rasm"), upload_to="patients/process_photos/")
    patient = models.ForeignKey("patient.User", verbose_name=_("Bemor"), on_delete=models.CASCADE, related_name="patient_process_photo")

    class Meta:
        verbose_name = _("Tish holati")
        verbose_name_plural = _("Tish holatlari")

    def __str__(self):
        return f"{self.image.name} - {self.patient.__str__()}"
