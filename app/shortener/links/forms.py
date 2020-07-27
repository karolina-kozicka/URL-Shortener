from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Button
from crispy_forms.bootstrap import FormActions
from django.utils import timezone
from . import models


class LinkForm(forms.ModelForm):
    class Meta:
        model = models.Link
        fields = ("url", "hash", "valid_date")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div("url", "hash", css_class="url-fields col-sm-6"),
                Div("valid_date", css_class="date-field col-sm-6"),
                css_class="double-column",
            ),
            Div(
                FormActions(
                    Submit("save", "Save", css_class="btn btn-lg btn-block btn-dark ",),
                ),
                css_class="one-button",
            ),
        )
    
    def clean_valid_date(self):
        valid_date = self.cleaned_data['valid_date']
        if valid_date and valid_date <= timezone.now():
            raise forms.ValidationError("Valid date must be in the future.")
        return valid_date

    def save(self, *args, **kwargs):
        self.instance.user = self.user
        return super().save(*args, **kwargs)
