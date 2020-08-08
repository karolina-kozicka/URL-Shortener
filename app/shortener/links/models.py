from django.db import models
from django.db.models import F
from django.utils import timezone


class Link(models.Model):
    url = models.CharField(max_length=1024)
    hash = models.CharField(max_length=24, unique=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="links"
    )
    valid_date = models.DateTimeField(null=True, blank=True)
    views = models.BigIntegerField(default=0)

    def increment_views(self):
        self.views = F("views") + 1
        self.save()

    @property
    def active(self):
        return self.valid_date == None or self.valid_date >= timezone.now()
