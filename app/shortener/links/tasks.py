from celery import Celery
from . import models
from django.utils import timezone
from config import celery_app

from config.shortener import EXPIRED_LINKS_KEEP_TIME


@celery_app.task()
def delete_expired_links():
    models.Link.delete_expired_links()
