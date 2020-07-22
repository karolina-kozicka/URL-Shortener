from django import template
from django.contrib.sites.shortcuts import get_current_site

register = template.Library()


@register.simple_tag(takes_context=True)
def get_domain(context):
    request = context["request"]
    current_site = get_current_site(request)
    return current_site.domain
