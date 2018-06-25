from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "ip_address", "type", "owner", "approved", "active")
    list_display_links = ("name",)
    list_filter = ("type", ("owner", admin.RelatedOnlyFieldListFilter), "approved", "active")

    readonly_fields = ("created", "modified")
    raw_id_fields = ("owner",)
