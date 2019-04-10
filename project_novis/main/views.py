from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer


class EmptyView(View):
    @staticmethod
    def get(request: HttpRequest) -> HttpResponse:
        return HttpResponse("")


class VersionView(APIView):
    swagger_schema = None
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)

    @staticmethod
    def get(request: HttpRequest) -> Response:
        return Response({
            "hostname": settings.HOSTNAME,
            "version": settings.VERSION
        }, content_type="application/json")


class HomePageView(TemplateView):
    template_name = "marketing.html"


@method_decorator(cache_page(60 * 60), name='dispatch')
class RobotsView(View):
    @staticmethod
    def get(request: HttpRequest) -> HttpResponse:
        if settings.PRODUCTION:
            return HttpResponse(
                f"User-agent: *\nDisallow: /accounts/\nDisallow: /admin/\nSitemap: { request.build_absolute_uri('/sitemap.xml') }",
                content_type="text/plain")
        else:
            return HttpResponse(
                f"User-agent: *\nDisallow: /\nSitemap: {request.build_absolute_uri('/sitemap.xml')}",
                content_type="text/plain")
