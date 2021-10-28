from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class PasswordReset(models.Model):

    email = models.CharField(_("E-mail"), max_length=100)
    uidb64 = models.CharField(_("uidb64"), max_length=100)
    token = models.CharField(_("Token"), max_length=150)
    is_active = models.BooleanField(_("Faolligi"))

    class Meta:
        verbose_name = _("Parol tiklanishi")
        verbose_name_plural = _("Parol tiklanishlari")

    def __str__(self):
        return f"{self.email} - {self.is_active}"
