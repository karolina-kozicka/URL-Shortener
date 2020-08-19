from django.forms import ModelForm
from django_registration.forms import RegistrationForm

from .models import User

class RegisterForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
        fields = [
            "email",
            "password1",
            "password2",
        ]
 