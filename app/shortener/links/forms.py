from django import forms

from . import models


class LinkForm(forms.ModelForm):
    class Meta:
        model = models.Link
        fields = ("url", "hash", "valid_date")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.user = self.user
        return super().save(*args, **kwargs)

