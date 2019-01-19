import re

import requests
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ...models import CallSign, EQSLUser
from ...utils import extract_callsign


class Command(BaseCommand):
    help = 'Import EQSL user data'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='?', type=str, default="http://www.eqsl.cc/QSLCard/DownloadedFiles/AGMemberlist.txt")

    def handle(self, *args, **options):
        counter = 0
        new_counter = 0
        error = 0

        self.stdout.write("Import EQSL user data")
        with requests.get(options['url'], stream=False) as r:
            if r.status_code == 200:
                for row in r.iter_lines(decode_unicode=True):
                    callsign = extract_callsign(row)
                    if not callsign:
                        self.stdout.write(f"Invalid callsign { row }")
                        continue

                    counter += 1

                    call_sign_instance, new_call_sign = CallSign.objects.get_or_create(name=callsign,
                                                                                       defaults={"name": callsign,
                                                                                                 "created_by": get_user_model().objects.get(id=1)})
                    if new_call_sign:
                        call_sign_instance.set_default_meta_data()
                        call_sign_instance.save()
                        new_counter += 1

                    EQSLUser.objects.get_or_create(callsign=call_sign_instance)

        self.stdout.write(self.style.SUCCESS('call sings: %d new call sings: %d errors: %d source: %s' % (
            counter, new_counter, error, options['url'])))
