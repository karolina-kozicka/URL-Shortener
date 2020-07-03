from django.db import models


class Link(models.Model):
    url = models.CharField(max_length=1024)
    hash = models.CharField(max_length=24, unique=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="links"
    )
    valid_date = models.DateTimeField(null=True, blank=True)
