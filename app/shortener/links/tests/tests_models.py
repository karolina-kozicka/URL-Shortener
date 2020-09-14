from django.test import TestCase
import datetime
from django.utils import timezone

from ..factories import LinkFactory


class LinksTestCase(TestCase):
    def test_increment_views_returns_views_plus_one(self):
        link = LinkFactory.create(views=0)
        link.increment_views()
        link.refresh_from_db()
        self.assertEqual(link.views, 1)
    
    def test_active_returns_true_if_link_is_active(self):
        tomorrow = timezone.now() + datetime.timedelta(days=1)
        link = LinkFactory.create(valid_date=tomorrow)
        self.assertTrue(link.active)

    def test_active_returns_true_if_link_is_unlimited(self):
        link = LinkFactory.create(valid_date=None)
        self.assertTrue(link.active)
        
    def test_active_returns_false_if_link_is_not_active(self):
        yesterday = timezone.now() - datetime.timedelta(days=1)
        link = LinkFactory.create(valid_date=yesterday)
        self.assertFalse(link.active)