import re

import geocoder
from django.apps import apps
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

CALLSIGN_REGEX = r"^(?=.*[a-zA-Z])([a-zA-Z0-9]+[0-9][a-zA-Z0-9]+)$"
CALLSIGN_REGEX_COMPILE = re.compile(CALLSIGN_REGEX)
CALLSIGN_EXTRACT_REGEX_COMPILE = re.compile(
    r"(?=.*[a-zA-Z])([A-Z0-9]+[/_-])?([a-zA-Z]+[0-9][a-zA-Z]+)([/-_][A-Z0-9]+)?")
ALPHANUM_ONLY = re.compile(r'[\W_]+')
CALLSIGN_MAX_LENGTH = 16


class CallsignField(models.CharField):
    # TODO(elnappo) enhance regex validation
    default_validators = [RegexValidator(regex=CALLSIGN_REGEX)]
    description = _("Ham radio callsign field")

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


class WikidataObjectField(models.CharField):
    # TODO WikidataObject class, save as int
    description = _("Wikidata object field")
    default_validators = [RegexValidator(regex=r"^Q\d+$")]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 16
        super().__init__(*args, **kwargs)
    
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs


def extract_callsign(value: str) -> str:
    value: str = value.replace(" ", "").upper()
    callsign: str = ""

    if CALLSIGN_REGEX_COMPILE.search(value):
        if len(value) <= CALLSIGN_MAX_LENGTH:
            callsign = value

    callsign_groups = CALLSIGN_EXTRACT_REGEX_COMPILE.search(value)

    if callsign_groups:
        if len(value) <= CALLSIGN_MAX_LENGTH:
            callsign = callsign_groups.group(2)

    # Remove all non alphanumeric characters
    return ALPHANUM_ONLY.sub('', callsign).upper()


def generate_aprs_passcode(callsign: str) -> int:
    """
    Generate APRS passcode from callsign based on
    https://github.com/magicbug/PHP-APRS-Passcode/blob/master/aprs_func.php
    """

    hash_value = 0x73e2
    i = 0
    length = len(callsign)

    while i < length:
        hash_value ^= ord(callsign[i:i+1]) << 8
        hash_value ^= ord(callsign[i+1:i+1+1])
        i += 2

    return hash_value & 0x7fff


def point_to_grid(point: Point, high_accuracy: bool = True) -> str:
    """
    Converts WGS84 coordinates into the corresponding Maidenhead Locator.
    Based on https://github.com/dh1tw/pyhamtools/blob/master/pyhamtools/locator.py
    """
    # TODO add parameter for various grid accuracy
    longitude: float = point.x + 180
    latitude: float = point.y + 90

    locator: str = chr(ord('A') + int(longitude / 20))
    locator += chr(ord('A') + int(latitude / 10))
    locator += chr(ord('0') + int((longitude % 20) / 2))
    locator += chr(ord('0') + int(latitude % 10))
    if high_accuracy:
        locator += chr(ord('A') + int((longitude - int(longitude / 2) * 2) / (2 / 24))).lower()
        locator += chr(ord('A') + int((latitude - int(latitude / 1) * 1) / (1 / 24))).lower()

    return locator


def grid_to_point(grid: str) -> Point:
    """
    Converts Maidenhead locator in the corresponding WGS84 coordinates
    Based on https://github.com/dh1tw/pyhamtools/blob/master/pyhamtools/locator.py
    """
    # TODO allow arbitrary grid accuracy
    locator: str = grid.upper()

    if len(locator) == 5 or len(locator) < 4:
        raise ValueError

    if ord(locator[0]) > ord('R') or ord(locator[0]) < ord('A'):
        raise ValueError

    if ord(locator[1]) > ord('R') or ord(locator[1]) < ord('A'):
        raise ValueError

    if ord(locator[2]) > ord('9') or ord(locator[2]) < ord('0'):
        raise ValueError

    if ord(locator[3]) > ord('9') or ord(locator[3]) < ord('0'):
        raise ValueError

    if len(locator) == 6:
        if ord(locator[4]) > ord('X') or ord(locator[4]) < ord('A'):
            raise ValueError
        if ord(locator[5]) > ord('X') or ord(locator[5]) < ord('A'):
            raise ValueError

    longitude: float = (ord(locator[0]) - ord('A')) * 20 - 180
    latitude: float = (ord(locator[1]) - ord('A')) * 10 - 90
    longitude += (ord(locator[2]) - ord('0')) * 2
    latitude += (ord(locator[3]) - ord('0'))

    if len(locator) == 6:
        longitude += ((ord(locator[4])) - ord('A')) * (2 / 24)
        latitude += ((ord(locator[5])) - ord('A')) * (1 / 24)

        # move to center of subsquare
        longitude += 1 / 24
        latitude += 0.5 / 24

    else:
        # move to center of square
        longitude += 1
        latitude += 0.5

    return Point(longitude, latitude)


def address_to_point(address: str, provider: str = "arcgis", session=None, use_cache: bool = True) -> Point:
    # use provider string as function name
    _geocoder = getattr(geocoder, provider)
    AddressLocationCache = apps.get_model('callsign', 'AddressLocationCache')

    if use_cache:
        try:
            return AddressLocationCache.objects.get(address=address, provider=provider).location
        except AddressLocationCache.DoesNotExist:
            if session:
                g = _geocoder(address, session=session)
            else:
                g = _geocoder(address)
            location = Point(g.lng, g.lat)
            AddressLocationCache.objects.create(address=address, provider=provider, location=location)
            return location
    else:
        if session:
            g = _geocoder(address, session=session)
        else:
            g = _geocoder(address)
        return Point(g.lng, g.lat)


def address_to_grid_based_point(address: str,
                                provider: str = "arcgis",
                                session=None,
                                use_cache: bool = True,
                                high_accuracy: bool = True) -> Point:
    """ Return location of address but limit accuracy to center of grid square"""
    grid = point_to_grid(address_to_point(address=address,
                                          provider=provider,
                                          session=session,
                                          use_cache=use_cache), high_accuracy=high_accuracy)
    return grid_to_point(grid)


def get_sentinel_user():
    return get_user_model().objects.get_or_create(email='deleted@project-novis.org')[0]
