from django.utils.translation import ugettext_lazy as _

CHOICES = {
    'diabet': [
        ('1', _("Yo'q")),
        ('2', _("Bor")),
        ('3', _("Bilmadim"))
    ],
    'anesthesia': [
        ('1', "1"),
        ('2', "2"),
        ('3', _("3 va undan ko'proq")),
        ('4', _("Qo'llanilmagan")),
    ],
    'hepatitis': [
        ('1', _("Yo'q")),
        ('2', _("Bor")),
        ('3', _("Bilmadim"))
    ],
    'aids': [
        ('1', _("Yo'q")),
        ('2', _("Bor")),
        ('3', _("Bilmadim"))
    ],
    'pressure': [
        ('1', _("Normal")),
        ('2', _("Past")),
        ('3', _("Baland"))
    ],
    'allergy': [
        ('1', _("Yo'q")),
        ('2', _("Bor (nimagaligini yozing)"))
    ],
    'asthma': [
        ('1', _("Yo'q")),
        ('2', _("Bor")),
        ('3', _("Bilmadim"))
    ],
    'dizziness': [
        ('1', _("Yo'q")),
        ('2', _("Ko'pincha")),
        ('3', _("Ba'zida"))
    ],
    'epilepsy': [
        ('1', _("Yo'q")),
        ('2', _("Bor"))
    ],
    'blood_disease': [
        ('1', _("Yo'q")),
        ('2', _("Bor"))
    ],
    'medications': [
        ('1', _("Yo'q")),
        ('2', _("Bor (qaysilar)"))
    ],
    'stroke': [
        ('1', _("Yo'q")),
        ('2', _("Ha"))
    ],
    'heart_attack': [
        ('1', _("Yo'q")),
        ('2', _("Ha"))
    ],
    'oncologic': [
        ('1', _("Yo'q")),
        ('2', _("Bor"))
    ],
    'tuberculosis': [
        ('1', _("Yo'q")),
        ('2', _("Bor"))
    ],
    'alcohol': [
        ('1', _("Yo'q")),
        ('2', _("Ha"))
    ],
    'pregnancy': [
        ('1', _("Yo'q")),
        ('2', _("Bor (nechinchi oy)"))
    ],
}
