from decimal import Decimal

from django.utils.translation import ugettext_lazy as _


CALLSIGN_TYPES = (
    ("beacon", _("Beacon")),
    ("club", _("Club")),
    ("educational", _("Educational")),
    ("experimental", _("Experimental")),
    ("personal", _("Personal")),
    ("repeater", _("Repeater")),
    ("shortwave_listener", _("Shortwave Listener")),
    ("special_event", _("Special Event")),
)

CONTINENTS = (
    ("AF", _("Asia")),
    ("AN", _("Antarctica")),
    ("AS", _("Africa")),
    ("EU", _("Europe")),
    ("NA", _("North America")),
    ("OC", _("Oceania")),
    ("SA", _("South America"))
)

CTCSS = (
    (Decimal("67.0"), "67.0 Hz"),
    (Decimal("69.3"), "69.3 Hz"),
    (Decimal("71.9"), "71.9 Hz"),
    (Decimal("74.4"), "74.4 Hz"),
    (Decimal("77.0"), "77.0 Hz"),
    (Decimal("79.7"), "79.7 Hz"),
    (Decimal("82.5"), "82.5 Hz"),
    (Decimal("85.4"), "85.4 Hz"),
    (Decimal("88.5"), "88.5 Hz"),
    (Decimal("91.5"), "91.5 Hz"),
    (Decimal("94.8"), "94.8 Hz"),
    (Decimal("97.4"), "97.4 Hz"),
    (Decimal("100.0"), "100.0 Hz"),
    (Decimal("103.5"), "103.5 Hz"),
    (Decimal("107.2"), "107.2 Hz"),
    (Decimal("110.9"), "110.9 Hz"),
    (Decimal("114.8"), "114.8 Hz"),
    (Decimal("118.8"), "118.8 Hz"),
    (Decimal("123.0"), "123.0 Hz"),
    (Decimal("127.3"), "127.3 Hz"),
    (Decimal("131.8"), "131.8 Hz"),
    (Decimal("136.5"), "136.5 Hz"),
    (Decimal("141.3"), "141.3 Hz"),
    (Decimal("146.2"), "146.2 Hz"),
    (Decimal("150.0"), "150.0 Hz"),
    (Decimal("151.4"), "151.4 Hz"),
    (Decimal("156.7"), "156.7 Hz"),
    (Decimal("159.8"), "159.8 Hz"),
    (Decimal("162.2"), "162.2 Hz"),
    (Decimal("165.5"), "165.5 Hz"),
    (Decimal("167.9"), "167.9 Hz"),
    (Decimal("171.3"), "171.3 Hz"),
    (Decimal("173.8"), "173.8 Hz"),
    (Decimal("177.3"), "177.3 Hz"),
    (Decimal("179.9"), "179.9 Hz"),
    (Decimal("183.5"), "183.5 Hz"),
    (Decimal("186.2"), "186.2 Hz"),
    (Decimal("189.9"), "189.9 Hz"),
    (Decimal("192.8"), "192.8 Hz"),
    (Decimal("196.6"), "196.6 Hz"),
    (Decimal("199.5"), "199.5 Hz"),
    (Decimal("203.5"), "203.5 Hz"),
    (Decimal("206.5"), "206.5 Hz"),
    (Decimal("210.7"), "210.7 Hz"),
    (Decimal("213.8"), "213.8 Hz"),
    (Decimal("218.1"), "218.1 Hz"),
    (Decimal("221.3"), "221.3 Hz"),
    (Decimal("225.7"), "225.7 Hz"),
    (Decimal("229.1"), "229.1 Hz"),
    (Decimal("233.6"), "233.6 Hz"),
    (Decimal("237.1"), "237.1 Hz"),
    (Decimal("241.8"), "241.8 Hz"),
    (Decimal("245.5"), "245.5 Hz"),
    (Decimal("250.3"), "250.3 Hz"),
    (Decimal("254.1"), "254.1 Hz"),
)

RF_MODES = (
    ("am", _("AM")),
    ("fm", _("FM")),
    ("dstar", _("D-STAR")),
    ("dmr", _("DMR")),
    ("ssb", _("SSB")),
    ("cw", _("CW")),
    ("psk125", _("PSK125")),
    ("PSK31", _("PSK31")),
    ("psk63", _("PSK63")),
    ("rtty", _("RTTY")),
)

BLACKLIST_REASONS = (
    ("invalid", _("Invalid Callsign")),
    ("abuse", _("Abuse")),
    ("other", _("Other")),
)

LICENSE_TYPE = {
    # Add CEPT equivalent?
    # https://en.wikipedia.org/wiki/Amateur_radio_licensing_in_the_United_States
    "USA": ("Technician Class", "General Class", "Amateur Extra Class", "Novice Class",
            "Advanced Class", "Technician Plus Class"),
    # https://de.wikipedia.org/wiki/Amateurfunkzeugnis
    "DEU": ("Class A", "Class E"),
    # https://de.wikipedia.org/wiki/Amateurfunkzeugnis
    "CHE": ("Amateurfunkkonzession 1", "Amateurfunkkonzession 2", "Amateurfunkkonzession 3"),
    # https://de.wikipedia.org/wiki/Amateurfunkzeugnis
    "AUT": ("Bewilligungsklasse 1", "Bewilligungsklasse 3", "Bewilligungsklasse 4"),
    # https://de.wikipedia.org/wiki/Amateurfunkzeugnis
    "POL": (),
    "GENERIC": ("CEPT", "CEPT-Novice", "IARP")
}

LOCATION_SOURCE_CHOICES = (
    ("user", _("User")),
    ("official", _("Official")),
    ("unofficial", _("Unofficial")),
    ("prefix", _("Prefix"))
)

LOCATION_SOURCE_PRIORITY = (
    "prefix",
    "unofficial",
    "official",
    "user",
)

# TODO add missing values
COUNTRY_ALTERNATIVE_NAME_MAPPING = {
    "Argentina Republic": "",
    "Aruba": "",
    "Belarus/Belorussia": "",
    "Belarus/belorussia": "",
    "Bosnia And Hercegovi": "Bosnia and Herzegovina",
    "Bosnia And Hercegovina": "Bosnia and Herzegovina",
    "Bosnia And Herzegovin": "Bosnia and Herzegovina",
    "Bosnia And Herzegovina": "Bosnia and Herzegovina",
    "Bosnia and Hercegovina": "Bosnia and Herzegovina",
    "Brunei Darussalam": "",
    "Central African Repu": "",
    "China": "People's Republic of China",
    "Columbia": "",
    "Corsica": "",
    "Domenican Republic": "",
    "England": "United Kingdom",
    "Faroe": "",
    "Gibraltar": "",
    "Greenland": "",
    "Guadeloupe": "",
    "Guam": "",
    "Hong Kong": "",
    "Korea": "",
    "Korea S": "",
    "Korsika": "",
    "Lithunia": "",
    "Luxemburg": "",
    "Macao": "",
    "Macedonia": "",
    "Marocco": "",
    "Martinique": "",
    "Mauretania": "",
    "Montserrat": "",
    "Netherlands": "Kingdom of the Netherlands",
    "Netherlands Antilles": "Kingdom of the Netherlands",
    "New Caledonia": "",
    "Oesterreich/Austria": "",
    "Oesterreich/austria": "",
    "Puerto Rico": "United States of America",
    "Reunion": "",
    "Saint Kitts And Nevis": "",
    "Scotland": "United Kingdom",
    "St. Vincent and Gren.": "",
    "St.Lucia": "",
    "Swaziland": "",
    "Trinidad And Tobago": "",
    "United States": "United States of America",
    "Viet Nam": "Vietnam",
    "Virgin Islands": "",
    "Wales": "United Kingdom",
}
