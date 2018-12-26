from decimal import Decimal

import requests
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ...models import CallSign


class Command(BaseCommand):
    help = 'Import DMR repeater from Brandmeister'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='?', type=str, default="https://api.brandmeister.network/v1.0/repeater/?action=LIST")

    def handle(self, *args, **options):
        counter = 0
        new_callsign_counter = 0
        update_callsign_counter = 0
        error = 0

        self.stdout.write("Import DMR repeater from Brandmeister")
        r = requests.get(options['url'], stream=False)
        if r.ok:
            repeaters = r.json()
            for repeater in repeaters:
                counter += 1
                call_sign_instance, new_call_sign = CallSign.objects.get_or_create(name=repeater["callsign"],
                                                                                   defaults={"name": repeater["callsign"],
                                                                                             "created_by": get_user_model().objects.get(id=1),
                                                                                             "type": "repeater"})
                if new_call_sign:
                    call_sign_instance.set_default_meta_data()
                    # TODO handle 0.0 0.0 and 10000.0 0.0
                    # if repeater["lat"] and repeater["lng"]:
                    #     try:
                    #         call_sign_instance.latitude = Decimal(repeater["lat"])
                    #         call_sign_instance.longitude = Decimal(repeater["lng"])
                    #     except Exception:
                    #         print(repeater)
                    call_sign_instance.save()
                    new_callsign_counter += 1

                # if (repeater["lat"] and repeater["lng"]) and (call_sign_instance.latitude != Decimal(repeater["lat"]) or call_sign_instance.longitude != Decimal(repeater["lng"])):
                #     try:
                #         call_sign_instance.latitude = Decimal(repeater["lat"])
                #         call_sign_instance.longitude = Decimal(repeater["lng"])
                #         call_sign_instance.save()
                #         update_callsign_counter += 1
                #     except Exception:
                #         print(repeater)

        self.stdout.write(self.style.SUCCESS('call sings: %d new call sings: %d updated call sings: %d errors: %d source: %s' % (
            counter, new_callsign_counter, update_callsign_counter, error, options['url'])))
