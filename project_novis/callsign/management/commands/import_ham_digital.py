import csv

import requests
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ...models import CallSign, DMRID


class Command(BaseCommand):
    help = 'Import Ham Digital user data (DMR and D-STAR)'

    def handle(self, *args, **options):
        dmr_user_list_url = "https://ham-digital.org/status/dmrid.dat"
        dstar_user_list_url = "https://ham-digital.org/status/dstaruser.db"

        counter = 0
        new_counter = 0
        error = 0

        # Import DMR IDs
        self.stdout.write("Import DMR ID list")
        r = requests.get(dmr_user_list_url, stream=False)

        if r.status_code == 200:
            reader = csv.reader(r.iter_lines(decode_unicode=True), delimiter=';')
            for row in reader:
                try:
                    counter += 1
                    call_sign_instance, new_call_sign = CallSign.objects.get_or_create(name=row[1],
                                                                                       defaults={"name": row[1],
                                                                                                 "created_by": get_user_model().objects.get(id=1)})
                    if new_call_sign:
                        call_sign_instance.set_default_meta_data()
                        call_sign_instance.save()
                        new_counter += 1

                    DMRID.objects.get_or_create(name=row[0], defaults={"name": row[0], "callsign": call_sign_instance})
                except IndexError:
                    error += 1
                    self.stderr.write(self.style.ERROR('Error in line: %s' % row))

        # Import D-STAR users
        self.stdout.write("Import D-STAR user list")
        r = requests.get(dstar_user_list_url, stream=False)

        if r.status_code == 200:
            for row in r.iter_lines(decode_unicode=True):
                counter += 1

                call_sign_instance, new_call_sign = CallSign.objects.get_or_create(name=row,
                                                                                   defaults={"name": row,
                                                                                             "dstar": True,
                                                                                             "created_by": get_user_model().objects.get(id=1)})
                if new_call_sign:
                    call_sign_instance.set_default_meta_data()
                    new_counter += 1
                else:
                    call_sign_instance.dstar = True
                call_sign_instance.save()

        self.stdout.write(self.style.SUCCESS('call sings: %d new call sings: %d errors: %d source: %s' % (
            counter, new_counter, error, options['url'])))
