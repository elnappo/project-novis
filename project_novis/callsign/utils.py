from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


def extract_callsign(callsign: str) -> str:
    parts = callsign.split("/")
    return callsign


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

    def __init__(self, **kwargs):
        kwargs['max_length'] = 8
        super().__init__(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs
