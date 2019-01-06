from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class EmptyView(View):
    def get(self, request) -> HttpResponse:
        return HttpResponse("")


class VersionView(APIView):
    swagger_schema = None
    permission_classes = (AllowAny,)

    def get(self, request) -> Response:
        return Response({
            "hostname": settings.HOSTNAME,
            "version": settings.VERSION
        }, content_type="application/json")


class HomePageView(TemplateView):
    template_name = "marketing.html"


@method_decorator(cache_page(60 * 60), name='dispatch')
class RobotsView(View):
    def get(self, request) -> HttpResponse:
        return HttpResponse(
            "User-agent: *\nDisallow: /admin/\nSitemap: https://www.project-novis.org/sitemap.xml",
            content_type="text/plain")
