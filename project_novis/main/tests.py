from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class ViewTest(TestCase):
    def setUp(self):
        self.email = "test@project-novis.org"
        self.password = "top_secret"

        self.user = get_user_model().objects.create_user(email=self.email, password=self.password)
        self.client = Client()

    def test_views_anonymous(self):
        views = (
            ('index', dict(), 200),
            ('version', dict(), 200),
            ('healthz', dict(), 200),
            ('readiness', dict(), 200),
            ('robots', dict(), 200),
            ("sitemap", dict(), 200),
            ("docs", dict(), 302),
        )

        for view, kwargs, status_code in views:
            with self.subTest(i=view):
                response = self.client.get(reverse(view, kwargs=kwargs))
                self.assertEqual(response.status_code, status_code)

    def test_views_logged_in(self):
        views = (
            ('index', dict(), 200),
            ('version', dict(), 200),
            ('healthz', dict(), 200),
            ('readiness', dict(), 200),
            ('robots', dict(), 200),
            ("sitemap", dict(), 200),
            ("docs", dict(), 302),
        )

        with self.subTest('User login'):
            logged_in = self.client.login(username=self.email, password=self.password)
            self.assertTrue(logged_in)

        for view, kwargs, status_code in views:
            with self.subTest(i=view):
                response = self.client.get(reverse(view, kwargs=kwargs))
                self.assertEqual(response.status_code, status_code)
