from django import forms
from django.utils.translation import ugettext_lazy as _


class QueryForm(forms.Form):
    reason = forms.CharField(
        label=_("Borish sababi"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Sababini kiriting")
            }
        ),
        max_length=255,
        localize=True
    )
    comment = forms.CharField(
        label=_("Tish shifokoriga izohlar"),
        widget=forms.Textarea(
            attrs={
                'class': "form-control",
                'placeholder': _("Izohlaringizni kiriting")
            }
        ),
        localize=True
    )
