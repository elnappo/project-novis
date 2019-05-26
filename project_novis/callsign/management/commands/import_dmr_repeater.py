import requests
from django.contrib.gis.geos import Point

from . import ImportCommand
from ...models import Repeater, Transmitter, DMRID


class Command(ImportCommand):
    help = 'Import DMR repeater from Brandmeister'
    source = 'brandmeister.network'
    task = "repeater_import_brandmeister"

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='?', type=str, default="https://api.brandmeister.network/v1.0/repeater/?action=LIST")

    def handle(self, *args, **options):
        r = requests.get(options['url'], stream=False)
        if r.ok:
            repeaters = r.json()
            for repeater in repeaters:
                try:
                    call_sign_instance, new_call_sign = self._handle_callsign(repeater["callsign"])
                except ValueError:
                    continue

                if not call_sign_instance.type:
                    call_sign_instance.type = "repeater"
                    call_sign_instance.save()

                if new_call_sign and repeater["lat"] and repeater["lng"]:
                    try:
                        latitude = float(repeater["lat"])
                        longitude = float(repeater["lng"])
                        if (-180 <= latitude <= 180) and (0 <= longitude <= 360):
                            call_sign_instance.location = Point(longitude, latitude)
                        call_sign_instance.save()

                    except Exception as e:
                        self._error(f"Invalid data: {repeater} - {str(e)}")

                dmr_id_instance, _ = DMRID.objects.get_or_create(name=repeater["repeaterid"],
                                                                 defaults={"name": repeater["repeaterid"],
                                                                           "callsign": call_sign_instance})

                try:
                    # TODO handle updates
                    repeater_instance, new_repeater = Repeater.objects.get_or_create(
                        callsign=call_sign_instance,
                        defaults={"callsign": call_sign_instance,
                                  "website": repeater.get("website", None),
                                  "altitude": repeater.get("agl", None),
                                  "created_by_id": self._import_user.id,
                                  "source": self.source})
                    transmitter_instance, new_transmitter = Transmitter.objects.update_or_create(
                        repeater=repeater_instance, transmit_frequency=float(repeater["tx"]),
                        defaults={"repeater": repeater_instance,
                                  "transmit_frequency": float(repeater["tx"]),
                                  "offset": float(repeater["rx"]) - float(repeater["tx"]),
                                  "mode": "dmr",
                                  "pep": repeater.get("pep", None),
                                  "description": repeater.get("description", ""),
                                  "hardware": repeater.get("hardware", ""),
                                  "colorcode": repeater.get("colorcode", None),
                                  "dmr_id": dmr_id_instance,
                                  "created_by_id": self._import_user.id,
                                  "source": self.source})

                except Exception as e:
                    self._error(f"Invalid data: {repeater} - {str(e)}")
            self._finish()
        else:
            self._error(f"Failed to get DMR repeater list. Status code {r.status_code}")
