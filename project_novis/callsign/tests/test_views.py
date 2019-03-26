from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import CallSign


class ViewTest(TestCase):
    def setUp(self):
        self.email = "test@project-novis.org"
        self.password = "top_secret"

        self.user = get_user_model().objects.create_user(email=self.email, password=self.password)
        self.client = Client()

    def create_callsigns(self, callsigns):
        for callsign in callsigns:
            CallSign.objects.create_callsign(callsign, self.user.id)

    def test_callsign_workflow(self):
        callsign = "DF0HSA"

        with self.subTest('GET callsign detail'):
            response = self.client.get(reverse('callsign:callsign-html-detail', kwargs={"slug": callsign}))
            self.assertEqual(response.status_code, 404)

        with self.subTest('GET callsign create'):
            response = self.client.get(reverse('callsign:callsign-html-create'))
            self.assertEqual(response.status_code, 302)

        with self.subTest('User login'):
            logged_in = self.client.login(username=self.email, password=self.password)
            self.assertTrue(logged_in)

        with self.subTest('GET callsign create logged in'):
            response = self.client.get(reverse('callsign:callsign-html-create'))
            self.assertEqual(response.status_code, 200)

        with self.subTest('POST callsign create'):
            response = self.client.post(reverse('callsign:callsign-html-create'), data={"name": callsign})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response._headers["location"][1],
                             reverse('callsign:callsign-html-detail', kwargs={"slug": callsign}))
            self.assertTrue(CallSign.objects.filter(name=callsign).exists())

        with self.subTest('GET callsign detail'):
            response = self.client.get(reverse('callsign:callsign-html-detail', kwargs={"slug": callsign}))
            self.assertEqual(response.status_code, 200)

        with self.subTest('POST callsign claim'):
            response = self.client.post(reverse('callsign:callsign-html-claim', kwargs={"slug": callsign}))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response._headers["location"][1],
                             reverse('callsign:callsign-html-detail', kwargs={"slug": callsign}))
            self.assertEqual(CallSign.objects.get(name=callsign).owner, self.user)

        with self.subTest('GET callsign update'):
            response = self.client.get(reverse('callsign:callsign-html-update', kwargs={"slug": callsign}))
            self.assertEqual(response.status_code, 200)

        with self.subTest('POST callsign update'):
            response = self.client.post(reverse('callsign:callsign-html-update', kwargs={"slug": callsign}),
                                        data={"type": "personal",
                                              "location": "{ 'type': 'Point', 'coordinates': [ -12977626.236679835245013, 5053729.738310274668038 ] }",
                                              "cq_zone": 1,
                                              "itu_zone": 1})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response._headers["location"][1],
                             reverse('callsign:callsign-html-detail', kwargs={"slug": callsign}))
            self.assertEqual(CallSign.objects.get(name=callsign).type, "personal")
            self.assertEqual(CallSign.objects.get(name=callsign).cq_zone, 1)
            self.assertEqual(CallSign.objects.get(name=callsign).itu_zone, 1)

        with self.subTest('GET callsign detail after update'):
            response = self.client.get(reverse('callsign:callsign-html-detail', kwargs={"slug": callsign}))
            self.assertEqual(response.status_code, 200)

    def test_callsign_permissions(self):
        callsigns = ("DF0HSA", "DB1QP")
        self.create_callsigns(callsigns)

        with self.subTest('GET callsign update as anonymous'):
            response = self.client.get(reverse('callsign:callsign-html-update', kwargs={"slug": callsigns[0]}))
            self.assertEqual(response.status_code, 302)

        with self.subTest('User login'):
            logged_in = self.client.login(username=self.email, password=self.password)
            self.assertTrue(logged_in)

        with self.subTest('POST callsign claim'):
            response = self.client.post(reverse('callsign:callsign-html-claim', kwargs={"slug": callsigns[0]}))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response._headers["location"][1],
                             reverse('callsign:callsign-html-detail', kwargs={"slug": callsigns[0]}))
            self.assertEqual(CallSign.objects.get(name=callsigns[0]).owner, self.user)

        with self.subTest('GET callsign update as owner'):
            response = self.client.get(reverse('callsign:callsign-html-update', kwargs={"slug": callsigns[0]}))
            self.assertEqual(response.status_code, 200)

        with self.subTest('GET callsign update not claimed callsign'):
            response = self.client.get(reverse('callsign:callsign-html-update', kwargs={"slug": callsigns[1]}))
            self.assertEqual(response.status_code, 403)

    def test_views_anonymous(self):
        callsigns = ("DF0HSA",)
        views = (
            ('callsign:callsign-html-create', dict(), 302),
            ('callsign:callsign-html-detail', dict(slug="DF0HSA"), 200),
            ('callsign:callsign-html-update', dict(slug="DF0HSA"), 302),
            ('callsign:callsign-html-claim', dict(slug="DF0HSA"), 302),
        )

        self.create_callsigns(callsigns)

        for view, kwargs, status_code in views:
            with self.subTest(i=view):
                response = self.client.get(reverse(view, kwargs=kwargs))
                self.assertEqual(response.status_code, status_code)
