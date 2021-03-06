from django.db import models
from django.db.models import F
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from config.shortener import EXPIRED_LINKS_KEEP_TIME


class Link(models.Model):
    url = models.URLField(verbose_name=_("URL"), max_length=1024)
    hash = models.CharField(verbose_name=_("Hash"), max_length=24, unique=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="links"
    )
    valid_date = models.DateTimeField(
        verbose_name=_("Valid date"), null=True, blank=True
    )
    views = models.BigIntegerField(default=0)
    password = models.CharField(verbose_name=_("Password"), max_length=16, default="", blank=True)

    def increment_views(self):
        self.views = F("views") + 1
        self.save(update_fields=["views"])

    @property
    def active(self):
        return self.valid_date == None or self.valid_date >= timezone.now()

    @classmethod
    def delete_expired_links(cls):
        cls.objects.filter(
            valid_date__lte=timezone.now() - EXPIRED_LINKS_KEEP_TIME
        ).delete()
