import csv
import sys

from dateutil.parser import parse

from . import ImportCommand


class Command(ImportCommand):
    help = 'Import LOTW user data'
    source = 'lotw.arrl.org'
    task = "callsign_import_lotw"

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='?', type=str, default="https://lotw.arrl.org/lotw-user-activity.csv")

    def run(self, url):
        r = self.session.get(url, stream=False)

        if r.status_code != 200:
            raise Exception(f"Failed to download {url} status code {r.status_code}")

        reader = csv.reader(r.iter_lines(decode_unicode=True), delimiter=',')
        callsigns = dict()

        for row in reader:
            if row[0]:
                raw_callsign = self._extract_callsign(row[0])
                if not raw_callsign:
                    continue
                if row[1] and row[2]:
                    callsigns[raw_callsign] = {"last_activity": parse(row[1] + "T" + row[2] + "Z")}
                else:
                    callsigns[raw_callsign] = {"last_activity": None}

        callsign_instances = self._callsign_bulk_create(callsigns.keys())
        for callsign_instance in callsign_instances:
            callsign_instance.lotw_last_activity = callsigns[callsign_instance.name]["last_activity"]
            callsign_instance.save()

        # TODO update existing callsigns

    def handle(self, *args, **options):
        self._write(f"Download callsign data from { options['url'] }")

        try:
            self.run(options['url'])
            self._finish()
        except:
            self._finish(failed=True, error_message=sys.exc_info())
            raise
