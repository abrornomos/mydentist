from django.db import models
from django.utils.translation import ugettext_lazy as _


class Clinic(models.Model):

    name = models.CharField(_("Nomi"), max_length=100)
    region = models.ForeignKey("baseapp.Region", verbose_name=_("Hudud"), on_delete=models.CASCADE, related_name="clinic_region")
    latitude = models.FloatField(_("Kenglik"), blank=True, null=True)
    longitude = models.FloatField(_("Uzunlik"), blank=True, null=True)

    class Meta:
        verbose_name = _("Shifoxona")
        verbose_name_plural = _("Shifoxonalar")

    def __str__(self):
        return self.name


class Clinic_translation(models.Model):

    clinic = models.ForeignKey("dentist.Clinic", verbose_name=_("Shifoxona"), on_delete=models.CASCADE, related_name="dentist_clinic_translation")
    name = models.CharField(_("Nomi"), max_length=100)
    address = models.CharField(_("Manzil"), max_length=255)
    orientir = models.CharField(_("Mo'ljal"), max_length=255, blank=True, null=True)
    language = models.ForeignKey("baseapp.Language", verbose_name=_("Til"), on_delete=models.CASCADE, related_name="clinic_language")

    class Meta:
        verbose_name = _("Shifoxonaning ma'lumoti")
        verbose_name_plural = _("Shifoxonaning ma'lumotlari")

    def __str__(self):
        return f"{self.name} - {self.language.name}"


class User(models.Model):

    user = models.OneToOneField("auth.User", verbose_name=_("Tish shifokori"), on_delete=models.CASCADE, related_name="dentist_user")
    phone_number = models.CharField(_("Telefon raqami"), max_length=100)
    gender = models.ForeignKey("baseapp.Gender", verbose_name=_("Jins"), on_delete=models.CASCADE, related_name="dentist_gender")
    birthday = models.DateField(_("Tug'ilgan sanasi"), auto_now=False, auto_now_add=False)
    image = models.ImageField(_("Rasmi"), upload_to="dentists/photos/", default="dentists/photos/default.png")
    language = models.ForeignKey("baseapp.Language", verbose_name=_("Tili"), on_delete=models.CASCADE, related_name="dentist_language")
    experience = models.IntegerField(_("Tajriba"))
    worktime_begin = models.TimeField(_("Ish vaqti boshlanishi"), auto_now=False, auto_now_add=False)
    worktime_end = models.TimeField(_("Ish vaqti tugashi"), auto_now=False, auto_now_add=False)
    is_fullday = models.BooleanField(_("24 soat rejimi"))
    slug = models.CharField(_("Slug"), max_length=255)
    clinic = models.ForeignKey("dentist.Clinic", verbose_name=_("Shifoxona"), on_delete=models.CASCADE, related_name="dentist_clinic")

    class Meta:
        verbose_name = _("Tish shifokori")
        verbose_name_plural = _("Tish shifokorlari")

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


class User_translation(models.Model):

    dentist = models.ForeignKey("dentist.User", verbose_name=_("Tish shifokori"), on_delete=models.CASCADE, related_name="dentist_user_translation")
    language = models.ForeignKey("baseapp.Language", verbose_name=_("Tili"), on_delete=models.CASCADE, related_name="dentist_language_translation")
    fullname = models.CharField(_("MyDentist dagi FIShi"), max_length=100)
    speciality = models.CharField(_("Soha"), max_length=500)

    class Meta:
        verbose_name = _("Tish shifokorining ma'lumoti")
        verbose_name_plural = _("Tish shifokorining ma'lumotlari")

    def __str__(self):
        return f"{self.dentist.__str__()} - {self.language.name}"


class Service(models.Model):

    name = models.CharField(_("Xizmat nomi"), max_length=100)
    duration = models.IntegerField(_("Xizmat davomiyligi"))
    price = models.IntegerField(_("Xizmat narxi"))
    dentist = models.ForeignKey("dentist.User", verbose_name=_("Tish shifokori"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Xizmat")
        verbose_name_plural = _("Xizmatlar")

    def __str__(self):
        return f"{self.name} - {self.dentist.__str__()}"


class Service_translation(models.Model):

    service = models.ForeignKey("dentist.Service", verbose_name=_("Xizmat"), on_delete=models.CASCADE, related_name="dentist_service_translation")
    language = models.ForeignKey("baseapp.Language", verbose_name=_("Tili"), on_delete=models.CASCADE, related_name="service_language_translation")
    name = models.CharField(_("Xizmat nomi"), max_length=100)

    class Meta:
        verbose_name = _("Xizmatning ma'lumoti")
        verbose_name_plural = _("Xizmatning ma'lumotlari")

    def __str__(self):
        return f"{self.service.__str__()} - {self.language.name}"


class Cabinet_Image(models.Model):

    image = models.ImageField(_("Rasm"), upload_to="dentists/cabinet_photos/")
    dentist = models.ForeignKey("dentist.User", verbose_name=_("Tish shifokori"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Kabinet rasmi")
        verbose_name_plural = _("Kabinet rasmlari")

    def __str__(self):
        return f"{self.image.name} - {self.dentist.__str__()}"
