from django.contrib import admin

from .models import *


class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_filter = ("created", "modified")


@admin.register(Callsign)
class CallsignAdmin(BaseModelAdmin):
    list_display = ("name", "owner", "type")
    list_display_links = ("name",)
    list_filter = ("type", "issued", "created", "modified")


@admin.register(DMRID)
class DMRIDAdmin(BaseModelAdmin):
    list_display = ("name", "callsign")
    list_display_links = ("name",)
    list_filter = ("active", "issued", "created", "modified")


@admin.register(Club)
class ClubAdmin(BaseModelAdmin):
    list_display = ("callsign", "owner")
    list_display_links = ("callsign",)


@admin.register(Country)
class CountryAdmin(BaseModelAdmin):
    list_display = ("name", "cq_zone", "itu_zone")
    list_display_links = ("name",)
