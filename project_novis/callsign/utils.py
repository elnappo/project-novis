import re
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

CALLSIGN_REGEX = r"^([a-zA-Z]+[0-9][a-zA-Z]+)$"
CALLSIGN_REGEX_COMPILE = re.compile(CALLSIGN_REGEX)
CALLSIGN_EXTRACT_REGEX_COMPILE = re.compile(r"([A-Z0-9]+[/_-]{1})?([a-zA-Z]+[0-9][a-zA-Z]+)([/-_]{1}[A-Z0-9]+)?")


class CallSignField(models.CharField):
    # TODO(elnappo) enhance regex validation
    default_validators = [RegexValidator(regex=CALLSIGN_REGEX)]
    description = _("Ham radio call sign field")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 16
        super().__init__(*args, **kwargs)

    def get_db_prep_value(self, value, connection, prepared=False):
        value = super().get_db_prep_value(value, connection, prepared)
        if value is not None:
            return value.upper()
        return value


class CQZoneField(models.PositiveSmallIntegerField):
    description = _("CQ zone field")

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': 1,
            'max_value': 40,
            **kwargs,
        })


class ITUZoneField(models.PositiveSmallIntegerField):
    description = _("ITU zone field")

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': 1,
            'max_value': 90,
            **kwargs,
        })


class ITURegionField(models.PositiveSmallIntegerField):
    description = _("ITU region field")

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': 1,
            'max_value': 3,
            **kwargs,
        })


class QTHLocatorField(models.CharField):
    default_validators = [RegexValidator(regex=r"^([A-R]{2})(\d{2})?([a-x]{2})?(\d{2})?$")]
    description = _("QTH locator field")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 8
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs


def extract_callsign(value: str) -> str:
    value = value.replace(" ", "").upper()

    if CALLSIGN_REGEX_COMPILE.search(value):
        return value

    callsign_groups = CALLSIGN_EXTRACT_REGEX_COMPILE.search(value)

    if callsign_groups:
        return callsign_groups.group(2)

    return ""


def generate_aprs_passcode(callsign: str) -> int:
    """
    Generate APRS passcode from callsing based on https://github.com/magicbug/PHP-APRS-Passcode/blob/master/aprs_func.php
    """

    hash_value = 0x73e2
    i = 0
    length = len(callsign)

    while i < length:
        hash_value ^= ord(callsign[i:i+1]) << 8
        hash_value ^= ord(callsign[i+1:i+1+1])
        i += 2

    return hash_value & 0x7fff
