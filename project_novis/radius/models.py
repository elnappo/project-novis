from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class Client(models.Model):
    TYPE_CHOICES = (
        ("wifi", _("WiFi")),
        ("switch", _("Switch")),
        ("vpn", _("VPN")),
        ("other", _("Other")),
    )

    name = models.CharField(max_length=128)
    ip_address = models.GenericIPAddressField(_("IP address"), null=True, blank=True)
    secret = models.CharField(max_length=256)
    description = models.TextField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=32)
    approved = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    last_request = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

    created = models.DateTimeField(_("Created"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified"), auto_now=True)
