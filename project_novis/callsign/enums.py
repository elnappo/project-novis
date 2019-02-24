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
    (67.0, "67.0 Hz"),
    (69.3, "69.3 Hz"),
    (71.9, "71.9 Hz"),
    (74.4, "74.4 Hz"),
    (77.0, "77.0 Hz"),
    (79.7, "79.7 Hz"),
    (82.5, "82.5 Hz"),
    (85.4, "85.4 Hz"),
    (88.5, "88.5 Hz"),
    (91.5, "91.5 Hz"),
    (94.8, "94.8 Hz"),
    (97.4, "97.4 Hz"),
    (100.0, "100.0 Hz"),
    (103.5, "103.5 Hz"),
    (107.2, "107.2 Hz"),
    (110.9, "110.9 Hz"),
    (114.8, "114.8 Hz"),
    (118.8, "118.8 Hz"),
    (123.0, "123.0 Hz"),
    (127.3, "127.3 Hz"),
    (131.8, "131.8 Hz"),
    (136.5, "136.5 Hz"),
    (141.3, "141.3 Hz"),
    (146.2, "146.2 Hz"),
    (150.0, "150.0 Hz"),
    (151.4, "151.4 Hz"),
    (156.7, "156.7 Hz"),
    (159.8, "159.8 Hz"),
    (162.2, "162.2 Hz"),
    (165.5, "165.5 Hz"),
    (167.9, "167.9 Hz"),
    (171.3, "171.3 Hz"),
    (173.8, "173.8 Hz"),
    (177.3, "177.3 Hz"),
    (179.9, "179.9 Hz"),
    (183.5, "183.5 Hz"),
    (186.2, "186.2 Hz"),
    (189.9, "189.9 Hz"),
    (192.8, "192.8 Hz"),
    (196.6, "196.6 Hz"),
    (199.5, "199.5 Hz"),
    (203.5, "203.5 Hz"),
    (206.5, "206.5 Hz"),
    (210.7, "210.7 Hz"),
    (213.8, "213.8 Hz"),
    (218.1, "218.1 Hz"),
    (221.3, "221.3 Hz"),
    (225.7, "225.7 Hz"),
    (229.1, "229.1 Hz"),
    (233.6, "233.6 Hz"),
    (237.1, "237.1 Hz"),
    (241.8, "241.8 Hz"),
    (245.5, "245.5 Hz"),
    (250.3, "250.3 Hz"),
    (254.1, "254.1 Hz"),
)

RF_MODES = (
    ("am", _("AM")),
    ("fm", _("FM")),
    ("dstar", _("D-STAR")),
    ("dmr", _("DMR")),
    ("ssb", _("SSB")),
)

BLACKLIST_REASONS = (
    ("invalid", _("Invalid Callsign")),
    ("abuse", _("Abuse")),
    ("other", _("Other")),
)

LICENSE_TYPE = {
    # Add CEPT equivalent?
    # https://en.wikipedia.org/wiki/Amateur_radio_licensing_in_the_United_States
    "USA": ("Technician Class", "General Class", "Amateur Extra Class", "Novice Class", "Advanced Class", "Technician Plus Class"),
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
