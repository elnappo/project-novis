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
            ('account_login', dict(), 200),
            ('account_logout', dict(), 302),
            ('account_signup', dict(), 200),
            ('account_reset_password', dict(), 200),
            ('profile_change', dict(), 302),
            ('profile_social_change', dict(), 302),
            ('profile_validation', dict(), 302),
        )

        for view, kwargs, status_code in views:
            with self.subTest(i=view):
                response = self.client.get(reverse(view, kwargs=kwargs))
                self.assertEqual(response.status_code, status_code)

    def test_views_logged_in(self):
        views = (
            ('account_login', dict(), 302),
            ('account_logout', dict(), 200),
            ('account_signup', dict(), 302),
            ('account_reset_password', dict(), 200),
            ('profile_change', dict(), 200),
            ('profile_social_change', dict(), 200),
            ('profile_validation', dict(), 200),
        )

        with self.subTest('User login'):
            logged_in = self.client.login(username=self.email, password=self.password)
            self.assertTrue(logged_in)

        for view, kwargs, status_code in views:
            with self.subTest(i=view):
                response = self.client.get(reverse(view, kwargs=kwargs))
                self.assertEqual(response.status_code, status_code)
