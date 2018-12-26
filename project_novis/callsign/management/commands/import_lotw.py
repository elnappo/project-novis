import csv
import re

import requests
from dateutil.parser import parse
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ...models import CallSign, LOTWUser


class Command(BaseCommand):
    help = 'Import LOTW user data'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='?', type=str, default="https://lotw.arrl.org/lotw-user-activity.csv")

    def handle(self, *args, **options):
        counter = 0
        new_counter = 0
        error = 0

        self.stdout.write("Import LOTW user data")
        r = requests.get(options['url'], stream=False)

        if r.status_code == 200:
            reader = csv.reader(r.iter_lines(decode_unicode=True), delimiter=',')
            for row in reader:
                valid = re.match('^[\w]+$', row[0]) is not None
                if valid:
                    counter += 1

                    call_sign_instance, new_call_sign = CallSign.objects.get_or_create(name=row[0],
                                                                                       defaults={"name": row[0],
                                                                                                 "created_by": get_user_model().objects.get(id=1)})
                    if new_call_sign:
                        call_sign_instance.set_default_meta_data()
                        call_sign_instance.save()
                        new_counter += 1

                    last_activity = parse(row[1] + "T" + row[2] + "Z")
                    lotw_instance, lotw_instance_created = LOTWUser.objects.get_or_create(callsign=call_sign_instance,
                                                                                          defaults={"callsign": call_sign_instance,
                                                                                                    "lotw_last_activity": last_activity})
                    if not lotw_instance_created and lotw_instance.lotw_last_activity < last_activity:
                        lotw_instance.lotw_last_activity = last_activity
                        lotw_instance.save()

            self.stdout.write(self.style.SUCCESS('call sings: %d new call sings: %d errors: %d source: %s' % (
                counter, new_counter, error, options['url'])))
