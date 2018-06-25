from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model


class BaseModel(models.Model):
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified"), auto_now=True)

    class Meta:
        abstract = True


class Country(BaseModel):
    CONTINENT_CHOICES = (
        ("AF", _("Asia")),
        ("AN", _("Antarctica")),
        ("AS", _("Africa")),
        ("EU", _("Europe")),
        ("NA", _("North America")),
        ("OC", _("Oceania")),
        ("SA", _("South America"))
    )

    name = models.CharField(max_length=64, db_index=True)
    adif = models.PositiveSmallIntegerField(db_index=True)
    cq_zone = models.PositiveSmallIntegerField(_("CQ zone"),
                                               validators=[MinValueValidator(1), MaxValueValidator(40)])
    itu_zone = models.PositiveSmallIntegerField(_("ITU zone"),
                                                validators=[MinValueValidator(1), MaxValueValidator(75)])
    latitude = models.FloatField()
    longitude = models.FloatField()
    continent = models.CharField(choices=CONTINENT_CHOICES, max_length=2)
    utc_offset = models.SmallIntegerField(_("UTC offset"), validators=[MinValueValidator(-12), MaxValueValidator(15)])

    def __str__(self) -> str:
        return self.name


class Callsign(BaseModel):
    TYPE_CHOICES = (
        ("personal", _("Personal")),
        ("club", _("Club")),
        ("repeater", _("Repeater")),
        ("beacon", _("Beacon")),
        ("educational", _("Educational")),
        ("experimental", _("Experimental")),
        ("special_event", _("Special Event")),
        ("shortwave_listener", _("Shortwave Listener"))
    )

    name = models.CharField(max_length=8)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    type = models.CharField(choices=TYPE_CHOICES, max_length=32, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)
    issued = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class DMRID(BaseModel):
    name = models.PositiveSmallIntegerField()
    callsign = models.ForeignKey(Callsign, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)
    issued = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = _("DMR ID")


class Club(BaseModel):
    callsign = models.ForeignKey(Callsign, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    members = models.ManyToManyField(get_user_model(), related_name="members")
    website = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.callsign.name


class LOTWUser(BaseModel):
    callsign = models.OneToOneField(Callsign, on_delete=models.CASCADE)
    last_activity = models.DateTimeField()


class ClublogUser(BaseModel):
    callsign = models.OneToOneField(Callsign, on_delete=models.CASCADE)
    first_qso = models.DateTimeField()
    last_qso = models.DateTimeField()
    last_upload = models.DateTimeField()
    oqrs = models.BooleanField()


class ESQLUser(BaseModel):
    callsign = models.OneToOneField(Callsign, on_delete=models.CASCADE)
