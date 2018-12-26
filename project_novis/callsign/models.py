from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse

from project_novis.callsign.utils import CallSignField, CQZoneField, ITUZoneField, ITURegionField, QTHLocatorField

CALL_SIGN_TYPE_CHOICES = (
    ("personal", _("Personal")),
    ("club", _("Club")),
    ("repeater", _("Repeater")),
    ("beacon", _("Beacon")),
    ("educational", _("Educational")),
    ("experimental", _("Experimental")),
    ("special_event", _("Special Event")),
    ("shortwave_listener", _("Shortwave Listener"))
)

CONTINENT_CHOICES = (
    ("AF", _("Asia")),
    ("AN", _("Antarctica")),
    ("AS", _("Africa")),
    ("EU", _("Europe")),
    ("NA", _("North America")),
    ("OC", _("Oceania")),
    ("SA", _("South America"))
)


class BaseModel(models.Model):
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified"), auto_now=True)

    class Meta:
        abstract = True


class Country(BaseModel):
    name = models.CharField(max_length=64, unique=True, db_index=True)
    adif_name = models.CharField(max_length=64, db_index=True, blank=True)
    alpha_2 = models.CharField(max_length=2, unique=True, db_index=True)
    alpha_3 = models.CharField(max_length=3, unique=True, db_index=True)
    numeric_3 = models.CharField(max_length=3, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.name


class DXCCEntry(BaseModel):
    name = models.CharField(max_length=64, db_index=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    deleted = models.BooleanField(default=False)

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
    continent = models.CharField(choices=CONTINENT_CHOICES, max_length=2, blank=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    utc_offset = models.FloatField(null=True, blank=True)
    type = models.CharField(choices=CALL_SIGN_TYPE_CHOICES, max_length=32, blank=True)

    def __str__(self) -> str:
        return self.name


class CallSignManager(models.Manager):
    def create_call_sign(self, call_sign: str):
        call_sign = self.create(name=call_sign)
        call_sign.set_default_meta_data()
        call_sign.save()
        return call_sign


class CallSign(BaseModel):
    name = CallSignField(unique=True, db_index=True)
    prefix = models.ForeignKey(CallSignPrefix, on_delete=models.PROTECT, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True)
    cq_zone = CQZoneField("CQ zone", null=True, blank=True)
    itu_zone = ITUZoneField("ITU zone", null=True, blank=True)
    itu_region = ITURegionField("ITU region", null=True, blank=True)
    grid = QTHLocatorField(blank=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    type = models.CharField(choices=CALL_SIGN_TYPE_CHOICES, max_length=32, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)
    issued = models.DateField(null=True, blank=True)
    dstar = models.BooleanField("D-STAR", default=False)

    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="created_by")
    comment = models.TextField(blank=True)

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
                self.latitude = prefix.latitude
                self.longitude = prefix.longitude
                break
            else:
                call_sign = call_sign[:-1]

    def get_absolute_url(self):
        return reverse('callsign:callsign-html-detail', args=[self.name])

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

    def __str__(self) -> str:
        return self.name


class DMRID(BaseModel):
    name = models.PositiveSmallIntegerField()
    callsign = models.ForeignKey(CallSign, related_name='dmr_ids', on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)
    issued = models.DateTimeField(null=True, blank=True)

    @property
    def brandmeister_profile_url(self) -> str:
        return f"https://brandmeister.network/index.php?page=profile&call={ self.callsign.name }"

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

    def __str__(self) -> str:
        return self.callsign.name


class LOTWUser(BaseModel):
    callsign = models.OneToOneField(CallSign, on_delete=models.CASCADE)
    lotw_last_activity = models.DateTimeField()

    def __str__(self) -> str:
        return self.callsign.name


class ClublogUser(BaseModel):
    callsign = models.OneToOneField(CallSign, on_delete=models.CASCADE)
    clublog_first_qso = models.DateTimeField()
    clublog_last_qso = models.DateTimeField()
    clublog_last_upload = models.DateTimeField()
    clublog_oqrs = models.BooleanField()

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
