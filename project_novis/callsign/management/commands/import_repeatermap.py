import requests
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from ...models import CallSign, Repeater, Transmitter
from ...utils import extract_callsign


class Command(BaseCommand):
    help = 'Import repeater from repeatermap.de'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='?', type=str, default="https://repeatermap.de/api.php")

    def handle(self, *args, **options):
        counter = 0
        new_callsign_counter = 0
        update_callsign_counter = 0
        error = 0

        self.stdout.write("Import repeater from repeatermap.de")
        r = requests.get(options['url'], stream=False)
        if r.ok:
            repeaters = r.json()
            for repeater in repeaters["relais"]:
                callsign = extract_callsign(repeater["call"].split("-")[0])
                if not callsign:
                    self.stdout.write(f"Invalid callsign { repeater['call'].split('-')[0] }")
                    continue

                counter += 1
                call_sign_instance, new_call_sign = CallSign.objects.get_or_create(name=callsign,
                                                                                   defaults={"name": callsign,
                                                                                             "created_by": get_user_model().objects.get(id=1),
                                                                                             "type": "repeater"})
                if new_call_sign:
                    call_sign_instance.set_default_meta_data()
                    if "lat" in repeater and "lon" in repeater:
                        try:
                            call_sign_instance.location = Point(repeater["lon"], repeater["lat"])
                        except Exception:
                            print(repeater)
                    call_sign_instance.save()
                    new_callsign_counter += 1

                if "lat" in repeater and "lon" in repeater:
                    try:
                        repeater_instance, new_repeater = Repeater.objects.get_or_create(callsign=call_sign_instance,
                                                                                 defaults={"callsign": call_sign_instance,
                                                                                           "website": repeater["url"],
                                                                                           "location": Point(repeater["lon"], repeater["lat"]),
                                                                                           "created_by": get_user_model().objects.get(id=1),})
                        transmitter_instance, new_transmitter = Transmitter.objects.get_or_create(
                            repeater=repeater_instance, transmit_frequency=repeater["tx"],
                            defaults={"repeater": repeater_instance,
                                      "transmit_frequency": repeater["tx"],
                                      "offset": repeater["rx"] - repeater["tx"],
                                      "mode": repeater["mode"],
                                      "description": repeater["remarks"],
                                      "created_by": get_user_model().objects.get(id=1),})

                    except:
                        self.stderr.write(repeater)


        self.stdout.write(self.style.SUCCESS('call sings: %d new call sings: %d updated call sings: %d errors: %d source: %s' % (
            counter, new_callsign_counter, update_callsign_counter, error, options['url'])))
