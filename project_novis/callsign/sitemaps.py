from django.contrib.sitemaps import Sitemap

from .models import CallSign


class CallsignSitemap(Sitemap):
    changefreq = "weekly"
    limit = 10000

    def items(self):
        return CallSign.objects.all()

    def lastmod(self, obj):
        return obj.modified
