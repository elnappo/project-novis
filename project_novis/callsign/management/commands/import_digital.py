import csv

import requests

from ...models import DMRID
from . import ImportCommand


class Command(ImportCommand):
    help = 'Import digital user data (DMR and D-STAR)'

    def ham_digital(self):
        dmr_user_list_url = "https://ham-digital.org/status/dmrid.dat"
        dstar_user_list_url = "https://ham-digital.org/status/dstaruser.db"
        self._write("Import ham-digital.org data")

        # Import DMR IDs
        self._write("Import DMR ID list")
        r = requests.get(dmr_user_list_url, stream=False)

        if r.status_code == 200:
            reader = csv.reader(r.iter_lines(decode_unicode=True), delimiter=';')
            for row in reader:
                try:
                    callsign_instance, _ = self._handle_callsign(row[1], source="ham-digital.org")
                    DMRID.objects.get_or_create(name=row[0], defaults={"name": row[0], "callsign": callsign_instance})
                except ValueError:
                    self._warning(f"Invalid data: {row}")

        # Import D-STAR users
        self._write("Import D-STAR user list")
        r = requests.get(dstar_user_list_url, stream=False)

        if r.status_code == 200:
            for row in r.iter_lines(decode_unicode=True):
                callsign_instance, _ = self._handle_callsign(row, source="ham-digital.org")
                if not callsign_instance.dstar:
                    callsign_instance.dstar = True
                    callsign_instance.save()

    def amateurradio_digital(self):
        url = "http://www.amateurradio.digital/export_csv_RAW.php?format=default&key=ekk0N0JSVE12azYxRVBrc2xHZzRZZz09"
        self._write("Import amateurradio.digital data")

        r = requests.get(url, stream=False)

        if r.status_code == 200:
            reader = csv.reader(r.iter_lines(decode_unicode=True), delimiter=',')
            for row in reader:
                try:
                    callsign_instance, _ = self._handle_callsign(row[1], source="amateurradio.digital")
                    DMRID.objects.update_or_create(name=row[0],
                                                   callsign=callsign_instance,
                                                   defaults={"name": row[0],
                                                             "callsign": callsign_instance,
                                                             "owner": row[2],
                                                             "city": row[3],
                                                             "state": row[4],
                                                             "country": row[5],
                                                             "remarks": ""})
                except ValueError:
                    self._warning(f"Invalid data: {row}")

    def handle(self, *args, **options):
        self.ham_digital()
        self.amateurradio_digital()
        self._finish()
