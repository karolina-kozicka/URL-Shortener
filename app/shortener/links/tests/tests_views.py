from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import datetime

from .. import views, forms, models
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


class LinksAddViewTests(TestCase):
    def test_redirects_to_login_if_user_is_not_authenticated(self):
        url = reverse("links:add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.resolver_match.func.__name__, LoginView.as_view().__name__
        )

    def test_uses_add_view(self):
        response = self.client.get(reverse("links:add"))
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.LinksAddView.as_view().__name__,
        )

    def test_renders_add_template(self):
        user = UserFactory.create()
        self.client.force_login(user)
        url = reverse("links:add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "links/add.html")

    def test_adds_link(self):
        user = UserFactory.create()
        self.client.force_login(user)
        test_hash = "test_hash"
        data = {
            "url": "https://url-test.com/",
            "hash": test_hash,
        }
        url = reverse("links:add")

        response = self.client.post(url, data, follow=True)
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.LinksListView.as_view().__name__,
        )
        self.assertTrue(
            models.Link.objects.filter(
                hash=test_hash, user=user, valid_date__isnull=True
            ).exists()
        )

    def test_adds_link_with_password(self):
        user = UserFactory.create()
        self.client.force_login(user)
        test_hash = "test_hash"
        link_password = "password"
        data = {
            "url": "https://url-test.com/",
            "hash": test_hash,
            "password": link_password,
        }
        url = reverse("links:add")

        response = self.client.post(url, data, follow=True)
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.LinksListView.as_view().__name__,
        )
        self.assertTrue(
            models.Link.objects.filter(
                hash=test_hash,
                user=user,
                password=link_password,
                valid_date__isnull=True,
            ).exists()
        )

    def test_adds_link_with_valid_date(self):
        user = UserFactory.create()
        self.client.force_login(user)
        test_hash = "test_hash"
        valid_date = timezone.now() + datetime.timedelta(days=15)
        data = {
            "url": "https://url-test.com/",
            "hash": test_hash,
            "valid_date": valid_date.strftime("%Y-%m-%d %H:%M"),
        }
        url = reverse("links:add")

        response = self.client.post(url, data, follow=True)
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.LinksListView.as_view().__name__,
        )
        self.assertTrue(
            models.Link.objects.filter(
                hash=test_hash, user=user, valid_date=valid_date.strftime("%Y-%m-%d %H:%M")
            ).exists()
        )


class LinksEditViewTests(TestCase):
    def test_redirects_to_login_if_user_is_not_authenticated(self):
        url = reverse("links:edit", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.resolver_match.func.__name__, LoginView.as_view().__name__
        )

    def test_uses_edit_view(self):
        url = reverse("links:edit", args=(1,))
        response = self.client.get(url)
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.LinksEditView.as_view().__name__,
        )

    def test_renders_edit_template(self):
        user = UserFactory.create()
        self.client.force_login(user)
        link = LinkFactory.create(user=user)
        url = reverse("links:edit", args=(link.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "links/edit.html")

    def test_edits_link(self):
        user = UserFactory.create()
        self.client.force_login(user)
        test_hash = "test_hash"
        new_test_hash = "new_test_hash"
        link = LinkFactory.create(hash=test_hash, user=user)
        url = reverse("links:edit", args=(link.id,))
        data = {
            "url": "https://url-test.com/",
            "hash": new_test_hash,
            "password": "link_password",
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.LinksListView.as_view().__name__,
        )
        self.assertTrue(
            models.Link.objects.filter(hash=new_test_hash, user=user,).exists()
        )
        self.assertFalse(
            models.Link.objects.filter(hash=test_hash, user=user,).exists()
        )


class LinksDeleteViewTests(TestCase):
    def test_redirects_to_login_if_user_is_not_authenticated(self):
        url = reverse("links:delete", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.resolver_match.func.__name__, LoginView.as_view().__name__
        )

    def test_uses_delete_view(self):
        url = reverse("links:delete", args=(1,))
        response = self.client.get(url)
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.LinksDeleteView.as_view().__name__,
        )

    def test_renders_delete_template(self):
        user = UserFactory.create()
        self.client.force_login(user)
        link = LinkFactory.create(user=user)
        url = reverse("links:delete", args=(link.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "links/delete.html")

    def test_deletes_link(self):
        user = UserFactory.create()
        self.client.force_login(user)
        test_hash = "test_hash"
        link = LinkFactory.create(hash=test_hash, user=user)
        url = reverse("links:delete", args=(link.id,))
        response = self.client.post(url, follow=True)
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.LinksListView.as_view().__name__,
        )
        self.assertFalse(
            models.Link.objects.filter(hash=test_hash, user=user,).exists()
        )



class OpenLinkViewTests(TestCase):
    def test_uses_open_link_view(self):
        link = LinkFactory.create()
        url = reverse("open", args=(link.hash,))
        response = self.client.get(url)
        self.assertEqual(
            response.resolver_match.func.__name__, views.OpenLinkView.as_view().__name__
        )

    def test_redirects_to_link_url_if_link_is_without_password(self):
        link = LinkFactory.create()
        url = reverse("open", args=(link.hash,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, link.url)

    def test_renders_password_template_if_link_is_with_password(self):
        link = LinkFactory.create(password="password")
        url = reverse("open", args=(link.hash,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "links/password.html")

    def test_puts_password_form_to_context(self):
        link = LinkFactory.create(password="password")
        url = reverse("open", args=(link.hash,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], forms.PasswordForm)

    def test_redirects_to_link_if_password_is_correct(self):
        link_password = "password"
        link = LinkFactory.create(password=link_password)
        url = reverse("open", args=(link.hash,))
        data = {"password": link_password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, link.url)

    def test_renders_password_template_if_password_is_incorrect(self):
        link_password = "password"
        link = LinkFactory.create(password=link_password)
        url = reverse("open", args=(link.hash,))
        data = {"password": "incorrect_password"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "links/password.html")

    def test_increments_views_properly(self):
        link_password = "password"
        start_views = 0
        link_with_password = LinkFactory.create(
            password=link_password, views=start_views
        )
        link_without_password = LinkFactory.create(password="", views=start_views)

        url = reverse("open", args=(link_with_password.hash,))

        data = {"password": "incorrect_password"}
        self.client.post(url, data)
        link_with_password.refresh_from_db()
        self.assertEqual(link_with_password.views, start_views)

        data = {"password": link_password}
        self.client.post(url, data)
        link_with_password.refresh_from_db()
        self.assertEqual(link_with_password.views, start_views + 1)

        url = reverse("open", args=(link_without_password.hash,))

        self.client.get(url)
        link_without_password.refresh_from_db()
        self.assertEqual(link_without_password.views, start_views + 1)
