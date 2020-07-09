from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.crypto import get_random_string

from . import models
from . import forms
from . import utils

# TODO Add: LoginRequiredMixin(get_queryset-filter), forms
class LinksListView(generic.ListView):
    template_name = "links/list.html"
    model = models.Link
    context_object_name = "links"


class LinksDetailView(generic.DetailView):
    template_name = "links/detail.html"
    model = models.Link
    context_object_name = "link"


class LinksAddView(generic.CreateView):
    template_name = "links/add.html"
    model = models.Link
    form_class = forms.LinkForm
    context_object_name = "link"
    success_url = reverse_lazy("links:detail")

    def get_initial(self):
        data = super().get_initial()
        data["hash"] = utils.create_hash()
        return data


class LinksEditView(generic.UpdateView):
    template_name = "links/edit.html"
    model = models.Link
    context_object_name = "link"
    success_url = reverse_lazy("links:detail")


class LinksDeleteView(generic.DeleteView):
    template_name = "delete.html"
    model = models.Link
    context_object_name = "link"
    success_url = reverse_lazy("links:list")


class RedirectionView(generic.base.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        hash = kwargs.get("hash")
        link = get_object_or_404(models.Link, hash=hash)
        return link.url
