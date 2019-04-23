import requests
from django.contrib.gis.geos import Point

from . import ImportCommand
from ...models import Repeater, Transmitter


class Command(ImportCommand):
    help = 'Import repeater from repeatermap.de'
    source = "repeatermap.de"
    task = "repeater_import_repeatermap"

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='?', type=str, default="https://repeatermap.de/api.php")

    def handle(self, *args, **options):

        self.stdout.write("Import repeater from repeatermap.de")
        r = requests.get(options['url'], stream=False)
        if r.ok:
            repeaters = r.json()
            for repeater in repeaters["relais"]:
                try:
                    call_sign_instance, new_call_sign = self._handle_callsign(repeater["call"].split("-")[0])
                except (ValueError,) as e:
                    self._warning(f"Invalid callsign {repeater} - {e}")
                    continue

                if not call_sign_instance.type:
                    call_sign_instance.type = "repeater"
                    call_sign_instance.save()

                # TODO handle updates
                if new_call_sign:
                    if "lat" in repeater and "lon" in repeater:
                        try:
                            call_sign_instance.location = Point(repeater["lon"], repeater["lat"])
                            call_sign_instance.save()
                        except:
                            self._warning(f"Invalid location {repeater}")

                # TODO handle updates
                if "lat" in repeater and "lon" in repeater:
                    try:
                        repeater_instance, new_repeater = Repeater.objects.get_or_create(callsign=call_sign_instance,
                                                                                         defaults={"callsign": call_sign_instance,
                                                                                                   "website": repeater["url"],
                                                                                                   "location": Point(repeater["lon"], repeater["lat"]),
                                                                                                   "created_by": self._import_user,
                                                                                                   "source": self.source})
                        transmitter_instance, new_transmitter = Transmitter.objects.get_or_create(
                            repeater=repeater_instance, transmit_frequency=repeater["tx"],
                            defaults={"repeater": repeater_instance,
                                      "transmit_frequency": repeater["tx"],
                                      "offset": repeater["rx"] - repeater["tx"],
                                      "mode": repeater["mode"],
                                      "description": repeater["remarks"],
                                      "created_by": self._import_user,
                                      "source": self.source})
                    except:
                        self._warning(f"Invalid repeater or transmitter data in {repeater}")
        self._finish()
