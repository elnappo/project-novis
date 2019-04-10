from django.contrib.sitemaps import Sitemap

from project_novis.callsign.models import Callsign


class CallsignSitemap(Sitemap):
    changefreq = "weekly"
    limit = 10000

    def items(self):
        return Callsign.objects.all()

    def lastmod(self, obj):
        return obj.modified
