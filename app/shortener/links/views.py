from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models

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
    context_object_name = "link"
    success_url = reverse_lazy("links:detail")


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
