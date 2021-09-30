from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Clinic(models.Model):

    name = models.CharField(_("Nomi"), max_length=100)
    region = models.ForeignKey("baseapp.Region", verbose_name=_("Hudud"), on_delete=models.CASCADE)
    address = models.CharField(_("Manzil"), max_length=255)
    orientir = models.CharField(_("Mo'ljal"), max_length=255, blank=True, null=True)
    latitude = models.FloatField(_("Kenglik"), blank=True, null=True)
    longitude = models.FloatField(_("Uzunlik"), blank=True, null=True)
    language = models.ForeignKey("baseapp.Language", verbose_name=_("Til"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Shifoxona")
        verbose_name_plural = _("Shifoxonalar")

    def __str__(self):
        return self.name


class Dentist(models.Model):

    fullname = models.CharField(_("FISh"), max_length=100)
    gender = models.ForeignKey("baseapp.Gender", verbose_name=_("Jins"), on_delete=models.CASCADE)
    worktime_begin = models.TimeField(_("Ish vaqti boshlanishi"), auto_now=False, auto_now_add=False)
    worktime_end = models.TimeField(_("Ish vaqti tugashi"), auto_now=False, auto_now_add=False)
    is_fullday = models.BooleanField(_("24 soat rejimi"))
    phone_number = models.CharField(_("Telefon raqami"), max_length=100)
    image = models.ImageField(_("Rasmi"), upload_to="dentists/photos/", default="dentists/photos/default.png")
    speciality = models.CharField(_("Soha"), max_length=500)
    experience = models.IntegerField(_("Tajriba"))
    slug = models.CharField(_("Slug"), max_length=255)
    clinic = models.ForeignKey("dentist.Clinic", verbose_name=_("Shifoxona"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Tish shifokori")
        verbose_name_plural = _("Tish shifokorlari")

    def __str__(self):
        return self.fullname


class Cabinet_Image(models.Model):

    image = models.ImageField(_("Rasm"), upload_to="dentists/cabinet_photos/")
    dentist = models.ForeignKey("dentist.Dentist", verbose_name=_("Tish shifokori"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Kabinet rasmi")
        verbose_name_plural = _("Kabinet rasmlari")

    def __str__(self):
        return self.image


class Service(models.Model):

    name = models.CharField(_("FISh"), max_length=100)
    duration = models.TimeField(_("Xizmat davomiyligi"), auto_now=False, auto_now_add=False)
    price = models.IntegerField(_("Xizmat narxi"))
    dentist = models.ForeignKey("dentist.Dentist", verbose_name=_("Tish shifokori"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Xizmat")
        verbose_name_plural = _("Xizmatlar")

    def __str__(self):
        return self.name


class Appointment(models.Model):

    user = models.ForeignKey("patient.User", verbose_name=_("Foydalanuvchi"), on_delete=models.CASCADE)
    reason = models.CharField(_("Sabab"), max_length=255)
    comment = models.TextField(_("Izohlar"))
    dentist = models.ForeignKey("dentist.Dentist", verbose_name=_("Tish shifokori"), on_delete=models.CASCADE)
    time = models.DateTimeField(_("Qabul vaqti"), default=None, auto_now=False, auto_now_add=False)
    attend = models.CharField(_("Qabul holati"), max_length=50)

    class Meta:
        verbose_name = _("So'rov")
        verbose_name_plural = _("So'rovlar")

    def __str__(self):
        return self.user.__str__()

