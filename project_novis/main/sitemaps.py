from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    def items(self):
        return ['index', 'api:schema-swagger-ui', 'api:schema-redoc']

    def location(self, item):
        return reverse(item)
