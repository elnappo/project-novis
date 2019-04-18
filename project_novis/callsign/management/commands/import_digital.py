import csv

import requests

from . import ImportCommand
from ...models import DMRID
from ...utils import address_to_grid_based_point


class Command(ImportCommand):
    help = 'Import digital user data (DMR and D-STAR)'
    task = "callsign_import_digital"

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='?', type=str, default="http://www.amateurradio.digital/export_csv_RAW.php?format=default")

    def ham_digital(self):
        dmr_user_list_url: str = "https://ham-digital.org/status/dmrid.dat"
        dstar_user_list_url: str = "https://ham-digital.org/status/dstaruser.db"
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
                except (ValueError, IndexError) as e:
                    self._warning(f"Invalid data: {row} - {e}")

        # Import D-STAR users
        self._write("Import D-STAR user list")
        r = requests.get(dstar_user_list_url, stream=False)

        if r.status_code == 200:
            for row in r.iter_lines(decode_unicode=True):
                callsign_instance, _ = self._handle_callsign(row, source="ham-digital.org")
                if not callsign_instance.dstar:
                    callsign_instance.dstar = True
                    callsign_instance.save()

    def amateurradio_digital(self, options):
        self._write("Import amateurradio.digital data")

        r = requests.get(options['url'], stream=False)

        if r.status_code == 200:
            reader = csv.reader(r.iter_lines(decode_unicode=True), delimiter=',')
            for row in reader:
                try:
                    callsign_instance, _ = self._handle_callsign(row[1], source="amateurradio.digital")
                    DMRID.objects.update_or_create(name=row[0],
                                                   callsign=callsign_instance,
                                                   defaults={"name": row[0],
                                                             "callsign": callsign_instance})
                    # TODO(elnappo) use Callsign.update_location()
                    if callsign_instance._location_source == "prefix":
                        address = f"{row[3]}, {row[4]}, {row[5]}"
                        location = address_to_grid_based_point(address)
                        callsign_instance.location = location
                        callsign_instance._location_source = "unofficial"
                        callsign_instance.save()

                except (ValueError, IndexError) as e:
                    self._warning(f"Invalid data: {row} - {e}")

    def handle(self, *args, **options):
        # self.ham_digital()
        self.amateurradio_digital(options)
        self._finish()
