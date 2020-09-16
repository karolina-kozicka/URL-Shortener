from django.test import TestCase
from django.urls import reverse

from .. import views
from ..factories import LinkFactory
from shortener.users.factories import UserFactory
from shortener.users.views import LoginView


class LinksListViewTests(TestCase):
    def test_redirects_to_login_if_user_is_not_authenticated(self):
        response = self.client.get(reverse("links:list"))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse("links:list"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.resolver_match.func.__name__, LoginView.as_view().__name__
        )

    def test_uses_list_view(self):
        response = self.client.get(reverse("links:list"))
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.LinksListView.as_view().__name__,
        )

    def test_renders_list_template(self):
        user = UserFactory.create()
        self.client.force_login(user)
        response = self.client.get(reverse("links:list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "links/list.html")

    def test_puts_links_to_context(self):
        user = UserFactory.create()
        links = LinkFactory.create_batch(5, user=user)
        self.client.force_login(user)
        response = self.client.get(reverse("links:list"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context.get("links"), links, transform=lambda x: x, ordered=False
        )


class LinksDetailViewTests(TestCase):
    def test_redirects_to_login_if_user_is_not_authenticated(self):
        url = reverse("links:detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.resolver_match.func.__name__, LoginView.as_view().__name__
        )

    def test_uses_detail_view(self):
        response = self.client.get(reverse("links:detail", args=(1,)))
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.LinksDetailView.as_view().__name__,
        )

    def test_renders_detail_template(self):
        user = UserFactory.create()
        self.client.force_login(user)
        link = LinkFactory.create(user=user)
        url = reverse("links:detail", args=(link.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "links/detail.html")

    def test_puts_link_to_context(self):
        user = UserFactory.create()
        self.client.force_login(user)
        link = LinkFactory.create(user=user)
        url = reverse("links:detail", args=(link.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["link"], link)
