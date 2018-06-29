from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers
from rest_framework.permissions import AllowAny

from .views import CallSignDetailView, CallSignCreate, CallSignUpdate, CountryViewSet, DXCCEntryViewSet, CallSignViewSet

app_name = "callsign"
schema_view = get_schema_view(
    openapi.Info(
        title="project novis API",
        default_version='v1',
        description="Ham radio API",
        terms_of_service="https://www.project-novis.org/terms/",
        contact=openapi.Contact(email="help@project-novis.org"),
        license=openapi.License(name="MIT License"),
    ),
    validators=['flex', 'ssv'],
    public=True,
    permission_classes=(AllowAny,),
)


router = routers.SimpleRouter()
router.register(r'api/country', CountryViewSet)
router.register(r'api/dxcc', DXCCEntryViewSet)
router.register(r'api/callsign', CallSignViewSet)


urlpatterns = [
    path('c/add/', CallSignCreate.as_view(), name='callsign-html-create'),
    path('c/<slug>/', CallSignDetailView.as_view(), name='callsign-html-detail'),
    path('c/<slug>/change', CallSignUpdate.as_view(), name='callsign-html-update'),

    re_path(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
]

urlpatterns += router.urls
