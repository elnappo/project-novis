import csv
import re
from dateutil.parser import parse

from django.core.management.base import BaseCommand
import requests

from ...models import Callsign


class Command(BaseCommand):
    help = 'Import LOTW user data'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='?', type=str, default="https://lotw.arrl.org/lotw-user-activity.csv")

    def handle(self, *args, **options):
        counter = 0
        new_callsign_counter = 0
        r = requests.get(options['url'], stream=True)

        if r.status_code == 200:
            reader = csv.reader(r.iter_lines(decode_unicode=True), delimiter=',')
            for row in reader:
                valid = re.match('^[\w]+$', row[0]) is not None
                if valid:
                    counter += 1
                    callsign, new_callsign = Callsign.objects.get_or_create(name=row[0])
                    callsign.last_activity = parse(row[1]+"T"+row[2]+"Z")
                    if new_callsign:
                        new_callsign_counter += 1

            self.stdout.write(self.style.SUCCESS('Successfully imported %d users from which %d are new from %s' % (
                counter, new_callsign_counter, options['url'])))
