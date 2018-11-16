from django.contrib import admin
from django import forms

from .models import *


class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_filter = ("created", "modified")


class LOTWUserInline(admin.TabularInline):
    model = LOTWUser
    verbose_name = "LOTW"
    verbose_name_plural = "LOTW"


class ClublogUserInline(admin.TabularInline):
    model = ClublogUser
    verbose_name = "Clublog"
    verbose_name_plural = "Clublog"


class ESQLUserInline(admin.TabularInline):
    model = EQSLUser
    verbose_name = "ESQL"
    verbose_name_plural = "ESQL"


def set_call_sign_metadata(modeladmin, request, queryset):
    for callsign in queryset:
        callsign.set_default_meta_data()
        callsign.save()
set_call_sign_metadata.short_description = "Set default metadata"


@admin.register(CallSign)
class CallSignAdmin(BaseModelAdmin):
    list_display = ("name", "country", "owner", "type")
    list_display_links = ("name",)
    list_filter = ("type", "issued", "created", "modified")
    search_fields = ("name",)
    actions = [set_call_sign_metadata]

    fieldsets = (
        ('Identifier', {
            'fields': (('name', 'prefix'), 'country')
        }),
        ('Details', {
            'fields': ('type', 'owner', 'active', "issued", "comment")
        }),
        ('Location', {
            'fields': ('cq_zone', 'itu_zone', 'itu_region', 'grid', 'latitude', 'longitude')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('created', 'modified', "created_by")
        }),
    )
    raw_id_fields = ("owner", "prefix", "created_by")
    inlines = [LOTWUserInline, ClublogUserInline, ESQLUserInline]


@admin.register(DMRID)
class DMRIDAdmin(BaseModelAdmin):
    list_display = ("name", "callsign")
    list_display_links = ("name",)
    list_filter = ("active", "issued", "created", "modified")


@admin.register(Club)
class ClubAdmin(BaseModelAdmin):
    list_display = ("callsign", "owner")
    list_display_links = ("callsign",)

    raw_id_fields = ("callsign", "owner", "members")


@admin.register(Country)
class CountryAdmin(BaseModelAdmin):
    list_display = ("name", "alpha_2", "alpha_3", "numeric_3")
    list_display_links = ("name",)
    ordering = ('name',)


@admin.register(DXCCEntry)
class DXCCEntryAdmin(BaseModelAdmin):
    list_display = ("id", "name", "country")
    list_display_links = ("id", "name")
    list_filter = ("deleted",)
    ordering = ('id',)


@admin.register(CallSignPrefix)
class CallsignPrefixAdmin(BaseModelAdmin):
    list_display = ("name", "dxcc", "country")
    list_display_links = ("name",)
    list_filter = ("country", "cq_zone", "itu_zone")
    ordering = ('name',)
    search_fields = ("name",)
