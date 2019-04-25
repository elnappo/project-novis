import json
import zipfile
from io import BytesIO
from datetime import timezone
from dateutil.parser import parse

import requests

from . import ImportCommand
from ...models import ClublogUser


class Command(ImportCommand):
    help = 'Import ClubLog user data'
    source = 'clublog.org'
    task = "callsign_import_clublog"

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='?', type=str, default="https://secure.clublog.org/clublog-users.json.zip")

    def handle(self, *args, **options):
        r = requests.get(options['url'], stream=False)

        if r.ok:
            data = BytesIO(r.content)
            z = zipfile.ZipFile(data)
            with z.open("clublog_users.json") as clublog_data:
                data = json.load(clublog_data)
                for key, value in data.items():
                    try:
                        call_sign_instance, _ = self._handle_callsign(key)
                    except (ValueError,):
                        self._warning(f"Invalid callsign {key} {value}")
                        continue

                    clublog_user_data = {"callsign": call_sign_instance,
                                         "clublog_first_qso": parse(value["firstqso"]).replace(tzinfo=timezone.utc) if value.pop("firstqso", None) in value else None,
                                         "clublog_last_qso": parse(value["lastqso"]).replace(tzinfo=timezone.utc) if value.pop("lastqso", None) in value else None,
                                         "clublog_last_upload": parse(value["lastupload"]).replace(tzinfo=timezone.utc) if value.pop("lastupload", None) in value else None,
                                         "clublog_oqrs": value.get("oqrs", None)}

                    clublog_instance, clublog_created = ClublogUser.objects.get_or_create(callsign=call_sign_instance,
                                                                                          defaults=clublog_user_data)
                    if not clublog_created:
                        for attr, a_value in clublog_user_data.items():
                            setattr(clublog_instance, attr, a_value)
                        clublog_instance.save()

            self._finish()
