from celery import Celery
from . import models
from django.utils import timezone
from config import celery_app


@celery_app.task()
def delete_expired_links():
    old_links = models.Link.objects.filter(
        valid_date__lte=(timezone.now() + timezone.timedelta(days=20))
    )
    for link in old_links:
        link.delete()

