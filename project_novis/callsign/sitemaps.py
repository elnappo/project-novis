from django.contrib.sitemaps import Sitemap

from project_novis.callsign.models import Callsign


class CallsignSitemap(Sitemap):
    changefreq = "weekly"
    limit = 10000

    def items(self):
        return Callsign.objects.all().order_by('id')

    def lastmod(self, obj):
        return obj.modified
