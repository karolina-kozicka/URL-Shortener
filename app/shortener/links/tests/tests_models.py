from django.test import TestCase
import datetime
from django.utils import timezone

from config.shortener import EXPIRED_LINKS_KEEP_TIME
from ..factories import LinkFactory
from ..models import Link




class LinksTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.yesterday = timezone.now() - datetime.timedelta(days=1)
        self.tomorrow = timezone.now() + datetime.timedelta(days=1)
        self.before_expired = timezone.now() - EXPIRED_LINKS_KEEP_TIME + datetime.timedelta(days=1)
        self.after_expired = timezone.now() - EXPIRED_LINKS_KEEP_TIME - datetime.timedelta(days=1)

    def test_increment_views_returns_views_plus_one(self):
        link = LinkFactory.create(views=0)
        link.increment_views()
        link.refresh_from_db()
        self.assertEqual(link.views, 1)
    
    def test_active_returns_true_if_link_is_active(self):
        link = LinkFactory.create(valid_date=self.tomorrow)
        self.assertTrue(link.active)

    def test_active_returns_true_if_link_is_unlimited(self):
        link = LinkFactory.create(valid_date=None)
        self.assertTrue(link.active)
        
    def test_active_returns_false_if_link_is_not_active(self):
        link = LinkFactory.create(valid_date=self.yesterday)
        self.assertFalse(link.active)

    def test_delete_expired_links_return_only_active_links(self):
        active_link =  LinkFactory.create(valid_date=self.tomorrow)
        before_expired_link =  LinkFactory.create(valid_date=self.before_expired)
        after_expired_link =  LinkFactory.create(valid_date=self.after_expired)
        Link.delete_expired_links()
        self.assertIn(active_link, Link.objects.all())
        self.assertIn(before_expired_link, Link.objects.all())
        self.assertNotIn(after_expired_link, Link.objects.all())
