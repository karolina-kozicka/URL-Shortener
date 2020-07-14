from django.urls import path, include
from django_registration.backends.activation.views import RegistrationView
from django.contrib.auth.views import TemplateView

from . import views

app_name = "users"
urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("password-reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-change/", views.PasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "activate/<str:activation_key>/",
        views.ActivationView.as_view(),
        name="registration_activate",
    ),
    path("register/", views.RegistrationView.as_view(), name="registration_register",),
    path(
        "register/closed/",
        TemplateView.as_view(template_name="registration/registration_closed.html"),
        name="registration_disallowed",
    ),
    path("account/edit/", views.EditView.as_view(), name="edit"),
]
