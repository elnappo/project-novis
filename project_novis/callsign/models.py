from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.geos import Point

from .utils import CallSignField, CQZoneField, ITUZoneField, ITURegionField, WikidataObjectField, generate_aprs_passcode

from .enums import CALLSIGN_TYPES, CONTINENTS, CTCSS, RF_MODES


class BaseModel(models.Model):
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified"), auto_now=True)

    class Meta:
        abstract = True


class LocationBaseModel(BaseModel):
    location = models.PointField(null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def grid(self):
        """
        Converts WGS84 coordinates into the corresponding Maidenhead Locator.
        Based on https://github.com/dh1tw/pyhamtools/blob/master/pyhamtools/locator.py
        """
        # TODO add parameter for grid accuracy
        longitude = self.location.x + 180
        latitude = self.location.y + 90

        locator = chr(ord('A') + int(longitude / 20))
        locator += chr(ord('A') + int(latitude / 10))
        locator += chr(ord('0') + int((longitude % 20) / 2))
        locator += chr(ord('0') + int(latitude % 10))
        locator += chr(ord('A') + int((longitude - int(longitude / 2) * 2) / (2 / 24))).lower()
        locator += chr(ord('A') + int((latitude - int(latitude / 1) * 1) / (1 / 24))).lower()

        return locator

    @grid.setter
    def grid(self, value):
        """
        Converts Maidenhead locator in the corresponding WGS84 coordinates
        Based on https://github.com/dh1tw/pyhamtools/blob/master/pyhamtools/locator.py
        """
        # TODO allow arbitrary grid accuracy
        locator = value.upper()

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
            if ord (locator[5]) > ord('X') or ord(locator[5]) < ord('A'):
                raise ValueError

        longitude = (ord(locator[0]) - ord('A')) * 20 - 180
        latitude = (ord(locator[1]) - ord('A')) * 10 - 90
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

        self.location = Point(longitude, latitude)

    @property
    def cq_zone(self) -> int:
        raise NotImplementedError

    @property
    def itu_zone(self) -> int:
        raise NotImplementedError

    @property
    def itu_region(self) -> int:
        raise NotImplementedError

    @property
    def continent(self) -> str:
        raise NotImplementedError

    @property
    def dxcc(self) -> int:
        raise NotImplementedError

    @property
    def country(self) -> str:
        raise NotImplementedError

    @property
    def utc_offset(self) -> int:
        raise NotImplementedError


class Country(BaseModel):
    name = models.CharField(max_length=64, unique=True, db_index=True)
    alpha_2 = models.CharField(max_length=2, unique=True, db_index=True)
    alpha_3 = models.CharField(max_length=3, unique=True, db_index=True)
    numeric_3 = models.CharField(max_length=3, unique=True, db_index=True)
    wikidata_object = WikidataObjectField(unique=True, db_index=True)

    # Additional Information
    adif_name = models.CharField(max_length=64, db_index=True, blank=True, null=True)
    geonames_id = models.PositiveIntegerField(null=True, blank=True)
    osm_relation_id = models.PositiveIntegerField(null=True, blank=True)
    itu_object_identifier = models.CharField(max_length=16, blank=True, null=True)
    itu_letter_code = models.CharField(max_length=3, blank=True, null=True)
    fips = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    @property
    def wikidata_url(self) -> str:
        return f"https://www.wikidata.org/wiki/{self.wikidata_object}"

    @property
    def geonames_url(self) -> str:
        if self.geonames_id:
            return f"https://www.geonames.org/{self.geonames_id}"
        else:
            return ""

    @property
    def osm_relation_url(self) -> str:
        if self.osm_relation_id:
            return f"https://www.openstreetmap.org/relation/{self.osm_relation_id}"
        else:
            return ""

    @property
    def world_fact_book_url(self) -> str:
        if self.fips:
            return f"https://www.cia.gov/library/publications/the-world-factbook/geos/{self.fips}.html"
        else:
            return ""


class DXCCEntry(BaseModel):
    name = models.CharField(max_length=64, db_index=True)
    deleted = models.BooleanField(default=False)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "DXCC Entry"
        verbose_name_plural = "DXCC Entries"
        unique_together = ("name", "deleted")


class CallSignPrefix(BaseModel):
    name = models.CharField(max_length=16, unique=True, db_index=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True)
    dxcc = models.ForeignKey(DXCCEntry, on_delete=models.PROTECT, null=True, blank=True)
    cq_zone = CQZoneField(null=True, blank=True)
    itu_zone = ITUZoneField(null=True, blank=True)
    itu_region = ITURegionField(null=True, blank=True)
    continent = models.CharField(choices=CONTINENTS, max_length=2, blank=True)
    location = models.PointField(null=True, blank=True)
    utc_offset = models.FloatField(null=True, blank=True)
    type = models.CharField(choices=CALLSIGN_TYPES, max_length=32, blank=True)

    def __str__(self) -> str:
        return self.name


class CallSignManager(models.Manager):
    def create_call_sign(self, call_sign: str):
        call_sign = self.create(name=call_sign)
        call_sign.set_default_meta_data()
        call_sign.save()
        return call_sign


class CallSign(LocationBaseModel):
    name = CallSignField(unique=True, db_index=True)
    prefix = models.ForeignKey(CallSignPrefix, on_delete=models.PROTECT, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True)
    cq_zone = CQZoneField("CQ zone", null=True, blank=True)
    itu_zone = ITUZoneField("ITU zone", null=True, blank=True)
    itu_region = ITURegionField("ITU region", null=True, blank=True)
    type = models.CharField(choices=CALLSIGN_TYPES, max_length=32, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)
    issued = models.DateField(null=True, blank=True)
    dstar = models.BooleanField("D-STAR", default=False)
    comment = models.TextField(blank=True)
    official_validated = models.BooleanField(default=False, help_text="Callsign is validated by a government agency")

    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="callsigns")
    internal_comment = models.TextField(blank=True)
    source = models.CharField(max_length=256, blank=True)
    objects = CallSignManager()

    # TODO(elnappo) make sure a user can not change his name after validation

    def set_default_meta_data(self):
        call_sign = self.name
        while call_sign:
            if CallSignPrefix.objects.filter(name=call_sign).exists():
                prefix = CallSignPrefix.objects.get(name=call_sign)
                self.prefix = prefix
                self.country = prefix.country
                self.cq_zone = prefix.cq_zone
                self.itu_zone = prefix.itu_zone
                self.location = prefix.location
                break
            else:
                call_sign = call_sign[:-1]

    def get_absolute_url(self):
        return reverse('callsign:callsign-html-detail', args=[self.name])

    @property
    def location_source(self) -> str:
        if self.location == self.prefix.location:
            return "prefix"
        else:
            return "manual"

    @property
    def eqsl_profile_url(self) -> str:
        return f"https://www.eqsl.cc/Member.cfm?{ self.name }"

    @property
    def clublog_profile_url(self) -> str:
        return f"https://secure.clublog.org/logsearch/{ self.name }"

    @property
    def dxheat_profile_url(self) -> str:
        return f"https://dxheat.com/db/{ self.name }"

    @property
    def aprsfi_profile_url(self) -> str:
        return f"https://aprs.fi/info/?call={ self.name }"

    @property
    def pskreporter_profile_url(self) -> str:
        return f"http://www.pskreporter.de/table?call={ self.name }"

    @property
    def qrz_profile_url(self) -> str:
        return f"https://www.qrz.com/db/{ self.name }"

    @property
    def hamqth_profile_url(self) -> str:
        return f"https://www.hamqth.com/{ self.name }"

    @property
    def hamcall_profile_url(self) -> str:
        return f"https://hamcall.net/call?callsign={ self.name }"

    @property
    def aprs_passcode(self) -> int:
        return generate_aprs_passcode(self.name)

    def __str__(self) -> str:
        return self.name


class DMRID(BaseModel):
    name = models.PositiveIntegerField(unique=True, db_index=True)
    callsign = models.ForeignKey(CallSign, related_name='dmr_ids', on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)
    issued = models.DateTimeField(null=True, blank=True)

    # Optional information used for DMR ID list
    owner = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=128, blank=True)
    remarks = models.CharField(max_length=128, blank=True)

    @property
    def brandmeister_profile_url(self) -> str:
        if self.callsign:
            return f"https://brandmeister.network/index.php?page=profile&call={ self.callsign.name }"
        else:
            return ""

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = _("DMR ID")


class Club(BaseModel):
    callsign = models.ForeignKey(CallSign, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    members = models.ManyToManyField(get_user_model(), related_name="members")
    website = models.URLField(blank=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="clubs")

    def __str__(self) -> str:
        return self.callsign.name


class LOTWUser(BaseModel):
    callsign = models.OneToOneField(CallSign, on_delete=models.CASCADE)
    lotw_last_activity = models.DateTimeField()

    def __str__(self) -> str:
        return self.callsign.name


class ClublogUser(BaseModel):
    callsign = models.OneToOneField(CallSign, on_delete=models.CASCADE)
    clublog_first_qso = models.DateTimeField(blank=True, null=True)
    clublog_last_qso = models.DateTimeField(blank=True, null=True)
    clublog_last_upload = models.DateTimeField(blank=True, null=True)
    clublog_oqrs = models.NullBooleanField(blank=True, null=True)

    @property
    def profile_url(self) -> str:
        return self.callsign.clublog_profile_url

    def __str__(self) -> str:
        return self.callsign.name


class EQSLUser(BaseModel):
    callsign = models.OneToOneField(CallSign, on_delete=models.CASCADE)

    @property
    def profile_url(self) -> str:
        return self.callsign.eqsl_profile_url

    def __str__(self) -> str:
        return self.callsign.name


class Repeater(BaseModel):
    callsign = models.ForeignKey(CallSign, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    website = models.URLField(max_length=400, blank=True, null=True)
    altitude = models.FloatField(blank=True, null=True)
    location = models.PointField(blank=True, null=True)
    description = models.TextField(blank=True)

    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="repeaters")
    source = models.CharField(max_length=256, blank=True)

    def __str__(self) -> str:
        return self.callsign.name


class Transmitter(BaseModel):
    repeater = models.ForeignKey(Repeater, on_delete=models.CASCADE, related_name='transmitters')
    active = models.BooleanField(default=True)
    transmit_frequency = models.DecimalField(max_digits=18, decimal_places=6)
    offset = models.DecimalField(max_digits=18, decimal_places=6)
    mode = models.CharField(max_length=16, choices=RF_MODES)
    pep = models.FloatField("PEP", null=True, blank=True, help_text="Peak Envelope Power")
    description = models.TextField(blank=True, null=True)
    hardware = models.CharField(max_length=256, blank=True)

    # Analog
    ctcss = models.FloatField("CTCSS", choices=CTCSS, blank=True, null=True, help_text="Continuous Tone Coded Squelch System")
    echolink = models.IntegerField(blank=True, null=True)

    # Digital
    dmr_id = models.ForeignKey(DMRID, on_delete=models.PROTECT, related_name="transmitters", verbose_name="DMR ID", blank=True, null=True)
    colorcode = models.SmallIntegerField(blank=True, null=True)

    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="transmitters")
    source = models.CharField(max_length=256, blank=True)

    @property
    def receive_frequency(self) -> Decimal:
        return self.transmit_frequency + self.offset

    @property
    def brandmeister_repeater_url(self) -> str:
        if self.dmr_id:
            return f"https://brandmeister.network/index.php?page=repeater&id={ self.dmr_id.name }"
        else:
            return "#"

    def __str__(self) -> str:
        return f"{ self.repeater.callsign.name } at { self.transmit_frequency } MHz"
