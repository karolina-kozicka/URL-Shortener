from django import forms

from . import models


class LinkForm(forms.ModelForm):
    class Meta:
        model = models.Link
        fields = ("url", "hash", "valid_date")

