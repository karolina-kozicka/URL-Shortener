from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.crypto import get_random_string

from . import models
from . import forms
from . import utils


class LinksListView(LoginRequiredMixin, generic.ListView):
    template_name = "links/list.html"
    model = models.Link
    context_object_name = "links"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class LinksDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "links/detail.html"
    model = models.Link
    context_object_name = "link"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class LinksAddView(LoginRequiredMixin, generic.CreateView):
    template_name = "links/add.html"
    model = models.Link
    form_class = forms.LinkForm
    context_object_name = "link"
    success_url = reverse_lazy("links:list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_initial(self):
        data = super().get_initial()
        data["hash"] = utils.create_hash()
        return data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class LinksEditView(LoginRequiredMixin, generic.UpdateView):
    template_name = "links/edit.html"
    model = models.Link
    form_class = forms.LinkForm
    success_url = reverse_lazy("links:detail:pk")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class LinksDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "links/delete.html"
    model = models.Link
    context_object_name = "link"
    success_url = reverse_lazy("links:list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class RedirectionView(LoginRequiredMixin, generic.base.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        hash = kwargs.get("hash")
        link = get_object_or_404(models.Link, hash=hash)
        link.increment_views()
        return link.url

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
