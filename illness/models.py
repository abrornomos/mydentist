from django.db import models
from django.utils.translation import ugettext_lazy as _


class Diabet(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Qandli diabet")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Anesthesia(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Narkoz")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Hepatitis(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Gepatit B")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class AIDS(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("OITS")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Pressure(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Qon bosimi")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Allergy(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Allergiya")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Asthma(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Bronxial astma")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Dizziness(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Bosh aylanishi")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Epilepsy(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Epilepsiya")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Blood_disease(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Qon kasali")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Medications(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Doimiy dorilar")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Stroke(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Insultga uchraganmisiz?")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Heart_attack(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Yurak xurujiga uchraganmisiz?")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Oncologic(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Onkologik kasalliklar")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Tuberculosis(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Sil kasalligi")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Alcohol(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Spirtli ichimlik ichasizmi?")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Pregnancy(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Homiladorlik")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"
