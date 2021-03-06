from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.sitemaps import views as sitemaps_views
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.views.decorators.cache import cache_page

from project_novis.main.sitemaps import StaticViewSitemap
from project_novis.callsign.sitemaps import CallsignSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'flatpages': FlatPageSitemap,
    'callsigns': CallsignSitemap
}

urlpatterns = [
    path('', include('project_novis.main.urls')),
    path('accounts/', include('project_novis.accounts.urls')),
    path('.well-known/change-password', RedirectView.as_view(pattern_name='account_change_password', permanent=False)),
    path('sitemap.xml', cache_page(3600)(sitemaps_views.index), {'sitemaps': sitemaps}, name="sitemap"),
    path('sitemap-<section>.xml', cache_page(3600)(sitemaps_views.sitemap), {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('c/', include('project_novis.callsign.urls')),
    path("api/v1/", include("project_novis.api.urls", namespace='v1')),
    path('', include('project_novis.radius.urls')),
    path('admin/', admin.site.urls),
    path('docs/', RedirectView.as_view(url=settings.DOCS_URL, permanent=False), name='docs'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    from django.views import defaults as default_views
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path('400/', default_views.bad_request, kwargs={'exception': Exception('Bad Request')}),
        path('403/', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        path('404/', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        path('500/', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
