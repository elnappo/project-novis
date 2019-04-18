from django.contrib import admin

from .models import *


class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_filter = ("created", "modified")


class ClublogUserInline(admin.TabularInline):
    model = ClublogUser
    verbose_name = "Clublog"
    verbose_name_plural = "Clublog"

    readonly_fields = ("clublog_first_qso", "clublog_last_qso", "clublog_last_upload", "clublog_oqrs")

    def has_add_permission(self, request, obj=None) -> bool:
        return False


class DMRIDInline(admin.TabularInline):
    model = DMRID
    verbose_name = "DMR ID"
    verbose_name_plural = "DMR IDs"

    show_change_link = True
    fields = ("name", "active", "issued")
    readonly_fields = ("name", "active", "issued")

    def has_add_permission(self, request, obj=None) -> bool:
        return False


class TransmitterInline(admin.TabularInline):
    model = Transmitter
    show_change_link = True
    fields = ("transmit_frequency", "offset", "mode")
    readonly_fields = ("transmit_frequency", "offset", "mode")


def set_call_sign_metadata(modeladmin, request, queryset):
    for callsign in queryset:
        callsign.set_default_meta_data()
        callsign.save()
set_call_sign_metadata.short_description = "Set default metadata"


@admin.register(Callsign)
class CallsignAdmin(BaseModelAdmin):
    list_display = ("name", "country", "owner", "type")
    list_display_links = ("name",)
    list_filter = ("type", "_official_validated", "country", "issued", "created", "modified")
    search_fields = ("name",)
    actions = [set_call_sign_metadata]

    fieldsets = (
        ('Identifier', {
            'fields': (('name', 'prefix'), 'country')
        }),
        ('Details', {
            'fields': ('_official_validated', 'official_validated', 'type', 'owner', 'active', "issued", "dstar",
                       "comment", "eqsl", "lotw_last_activity")
        }),
        ('Location', {
            'fields': ('cq_zone', 'itu_zone', 'itu_region', 'grid', 'location')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('internal_comment', 'source', 'created', 'modified', "created_by")
        }),
    )
    raw_id_fields = ("owner", "prefix", "created_by")
    readonly_fields = ('created', 'modified', 'grid', 'official_validated')
    inlines = [DMRIDInline, ClublogUserInline]


@admin.register(DMRID)
class DMRIDAdmin(BaseModelAdmin):
    list_display = ("name", "callsign")
    list_display_links = ("name",)
    list_filter = ("active", "issued", "created", "modified")
    search_fields = ("name", "callsign__name")
    raw_id_fields = ("callsign",)
    readonly_fields = ('brandmeister_profile_url', 'created', 'modified')


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


@admin.register(CallsignPrefix)
class CallsignPrefixAdmin(BaseModelAdmin):
    list_display = ("name", "dxcc", "country")
    list_display_links = ("name",)
    list_filter = ("country", "cq_zone", "itu_zone")
    ordering = ('name',)
    search_fields = ("name",)


@admin.register(Repeater)
class RepeaterAdmin(BaseModelAdmin):
    list_display = ("callsign", "active")
    list_display_links = ("callsign",)
    list_filter = ("active",)
    ordering = ('callsign',)
    search_fields = ("callsign",)

    raw_id_fields = ("callsign",)
    inlines = [TransmitterInline, ]


@admin.register(Transmitter)
class TransmitterAdmin(BaseModelAdmin):
    list_display = ("repeater", "transmit_frequency", "offset")
    list_display_links = ("repeater",)
    list_filter = ("mode",)
    ordering = ('repeater',)

    fieldsets = (
        ('General', {
            'fields': ('repeater', 'active', 'transmit_frequency', 'offset', 'receive_frequency',
                       'mode', 'pep', 'description')
        }),
        ('Analog', {
            'fields': ('ctcss', 'echolink')
        }),
        ('Digital', {
            'fields': ('dmr_id', 'brandmeister_repeater_url', 'colorcode')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('source', 'created', 'modified', "created_by")
        }),
    )

    readonly_fields = ('receive_frequency', 'brandmeister_repeater_url', 'created', 'modified')
    raw_id_fields = ("repeater",)


@admin.register(TelecommunicationAgency)
class TelecommunicationAgencyAdmin(BaseModelAdmin):
    list_display = ("name", "country")
    list_display_links = ("name",)
    list_filter = ("used_for_official_callsign_import", "created", "modified")


@admin.register(Person)
class PersonAdmin(BaseModelAdmin):
    list_display = ("name", "identifier", "source")
    list_display_links = ("name", "identifier")
    list_filter = ("source", "country", "telco_agency", "created", "modified")
    search_fields = ("identifier", "callsigns__name")

    raw_id_fields = ("callsigns",)


@admin.register(DataImport)
class DataImportAdmin(BaseModelAdmin):
    list_display = ("task", "start", "stop", "finished", "failed")
    list_display_links = ("task",)
    list_filter = ("task", "start", "stop", "finished", "failed", "created", "modified")
    ordering = ('-start',)

    readonly_fields = ("finished",)


@admin.register(CallsignBlacklist)
class CallsignBlacklistAdmin(BaseModelAdmin):
    list_display = ("callsign", "submitter", "reason", "approved")
    list_display_links = ("callsign",)
    list_filter = ("reason", "approved", "created", "modified")
