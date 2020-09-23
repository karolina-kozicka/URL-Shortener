"""shortener URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from shortener.links import views
from shortener.users.views import HomeView, trigger_error

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path("links/", include("shortener.links.urls")),
    path("user/", include("shortener.users.urls")),
    path('sentry-debug/', trigger_error),
    path("<str:hash>/", views.OpenLinkView.as_view(), name="open")
]
