from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import views
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django_registration.backends.activation import views as django_registration_views
from django.contrib import messages

from .forms import RegisterForm
from .models import User


class HomeView(views.TemplateView):
    template_name = "home.html"


class LoginView(views.LoginView):
    template_name = "users/login.html"


class LogoutView(views.LogoutView):
    template_name = "users/logout.html"


class PasswordResetView(views.PasswordResetView):
    template_name = "users/password_reset.html"
    success_url = reverse_lazy("users:password_reset")
    email_template_name = "users/reset_emial.html"
    subject_template_name = "users/password_reset_subject.txt"

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "The email with further instructions was sent to the submitted email address. If you don’t receive a message in 5 minutes, check the junk folder.",
        )
        return super().form_valid(form)


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, "Password has been reset successfully!"
        )
        return super().form_valid(form)


class PasswordChangeView(LoginRequiredMixin, views.PasswordChangeView):
    template_name = "users/password_change.html"
    success_url = reverse_lazy("users:password_change")

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, "Password has been changed successfully!"
        )
        return super().form_valid(form)


class RegistrationView(django_registration_views.RegistrationView):
    template_name = "registration/registration_form.html"
    form_class = RegisterForm
    success_url = reverse_lazy("users:registration_register")
    disallowed_url = reverse_lazy("users:registration_disallowed")
    email_body_template = "registration/activation_email_body.txt"
    email_subject_template = "registration/activation_email_subject.txt"

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "The email with further instructions was sent to the submitted email address. If you don’t receive a message in 5 minutes, check the spam folder.",
        )
        return super().form_valid(form)


class ActivationView(django_registration_views.ActivationView):
    template_name = "registration/activation_failed.html"
    success_url = reverse_lazy("users:login")

    def get_success_url(self, *args, **kwargs):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Your account has been activated successfully. Have fun using URL-Shortener!",
        )
        return super().get_success_url(*args, **kwargs)


class EditView(LoginRequiredMixin, generic.UpdateView):
    template_name = "users/edit.html"
    model = User
    fields = ("username",)
    success_url = reverse_lazy("users:edit")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Account details have been changed successfully!",
        )
        return super().form_valid(form)
