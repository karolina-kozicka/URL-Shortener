from django.contrib import admin

from .models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("url", "hash", "user", "valid_date", "views")
    search_fields = ("user__email", "url", "hash")
    list_filter = ("valid_date",)
