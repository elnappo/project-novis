from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers
from rest_framework.permissions import AllowAny

from callsign.views import CountryViewSet, DXCCEntryViewSet, CallSignViewSet, UserCallSignViewSet, CallSignCreateAPIView, DMRIDViewSet, CallSignPrefixViewSet, RepeaterViewSet, APRSPasscodeView
from api.apps import ApiConfig
from accounts.views import CurrentUserAPIView

app_name = ApiConfig.name
schema_view = get_schema_view(
    openapi.Info(
        title="project novis API",
        default_version='v1',
        description="Ham radio API",
        terms_of_service="https://www.project-novis.org/terms/",
        contact=openapi.Contact(email="help@project-novis.org", url="https://www.project-novis.org"),
        license=openapi.License(name="MIT License", url="https://choosealicense.com/licenses/mit/"),
    ),
    validators=['flex', 'ssv'],
    public=True,
    permission_classes=(AllowAny,),
)


router = routers.SimpleRouter()
router.register(r'country', CountryViewSet)
router.register(r'dxcc', DXCCEntryViewSet)
router.register(r'callsign', CallSignViewSet)
router.register(r'dmr', DMRIDViewSet)
router.register(r'prefix', CallSignPrefixViewSet)
router.register(r'repeater', RepeaterViewSet)
router.register(r'user/callsign', UserCallSignViewSet)

urlpatterns = [
    path('callsign', CallSignCreateAPIView.as_view(), name="callsign-create"),
    path('user', CurrentUserAPIView.as_view(), name="userinfo-retrieve"),
    path('user/callsign/<str:name>/aprs_passcode', APRSPasscodeView.as_view(), name="aprs-passcode"),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
]

urlpatterns += router.urls
