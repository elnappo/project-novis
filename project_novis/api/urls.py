from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers
from rest_framework.authtoken import views
from rest_framework.permissions import AllowAny

from project_novis.accounts.views import CurrentUserAPIView
from project_novis.api.apps import ApiConfig
from project_novis.callsign.views import CountryViewSet, DXCCEntryViewSet, CallsignViewSet, UserCallsignViewSet, \
    CallsignCreateAPIView, DMRIDViewSet, CallsignPrefixViewSet, RepeaterViewSet, APRSPasscodeView

app_name = ApiConfig.name
schema_view = get_schema_view(
    openapi.Info(
        title="project novis API",
        default_version='v1',
        description="Ham radio API provided by project novis. API is in beta stage and not stable.",
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
router.register(r'callsign', CallsignViewSet)
router.register(r'dmr', DMRIDViewSet)
router.register(r'prefix', CallsignPrefixViewSet)
router.register(r'repeater', RepeaterViewSet)
router.register(r'user/callsign', UserCallsignViewSet)

urlpatterns = [
    path('callsign', CallsignCreateAPIView.as_view(), name="callsign-create"),
    path('user', CurrentUserAPIView.as_view(), name="userinfo-retrieve"),
    path('user/callsign/<str:name>/aprs_passcode', APRSPasscodeView.as_view(), name="aprs-passcode"),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
    path('api-token-auth/', views.obtain_auth_token)
]

urlpatterns += router.urls
