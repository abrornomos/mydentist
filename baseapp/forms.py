from django import forms
from django.utils.translation import ugettext_lazy as _
from .var import CHOICES


class SearchForm(forms.Form):
    region = forms.CharField(
        widget=forms.Select(
            attrs={
                'class': "btn-select"
            },
            choices=CHOICES['region']
        ),
        max_length=50
    )
    gender = forms.CharField(
        widget=forms.Select(
            attrs={
                'class': "btn-select"
            },
            choices=CHOICES['gender']
        ),
        max_length=20
    )
    time = forms.BooleanField(
        label=_("24 soat"),
        widget=forms.CheckboxInput(
            attrs={
                'class': "form-check-input"
            }
        ),
        localize=True,
        required=False
    )
    nearest = forms.BooleanField(
        label=_("Yaqinligi bo'yicha"),
        widget=forms.CheckboxInput(
            attrs={
                'class': "form-check-input"
            }
        ),
        localize=True,
        required=False
    )

class GeoForm(forms.Form):
    latitude = forms.FloatField(
        widget=forms.HiddenInput(
            attrs={
                'value': 40.767684
            }
        ),
        required=False
    )
    longitude = forms.FloatField(
        widget=forms.HiddenInput(
            attrs={
                'value': 72.336187
            }
        ),
        required=False
    )
