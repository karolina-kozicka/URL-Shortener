from django import forms

from . import models


class LinkForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields = Author.objects.filter(name__startswith='O')

    class Meta:
        model = models.Link
        fields = ("url", "hash", "valid_date")

