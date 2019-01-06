import zipfile
import json
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import requests

from ...models import CallSign, ClublogUser
from ...utils import extract_callsign


class Command(BaseCommand):
    help = 'Import ClubLog user data'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='?', type=str, default="https://secure.clublog.org/clublog-users.json.zip")

    def handle(self, *args, **options):
        counter = 0
        new_counter = 0
        r = requests.get(options['url'], stream=False)

        if r.ok:
            data = BytesIO(r.content)
            z = zipfile.ZipFile(data)
            with z.open("clublog_users.json") as clublog_data:
                data = json.load(clublog_data)
                for key, value in data.items():
                    counter += 1
                    callsign = extract_callsign(key)
                    if not callsign:
                        self.stdout.write(f"Invalid callsign { key }")
                        continue

                    call_sign_instance, new_call_sign = CallSign.objects.get_or_create(name=callsign,
                                                                                       defaults={"name": callsign,
                                                                                                 "created_by": get_user_model().objects.get(id=1)})

                    if new_call_sign:
                        call_sign_instance.set_default_meta_data()
                        call_sign_instance.save()
                        new_counter += 1

                    # TODO add UTC timezone
                    clublog_user_data = {"callsign": call_sign_instance,
                                         "clublog_first_qso": value.get("firstqso", None),
                                         "clublog_last_qso": value.get("lastqso", None),
                                         "clublog_last_upload": value.get("lastupload", None),
                                         "clublog_oqrs": value.get("oqrs", None)}

                    clublog_instance, clublog_instance_created = ClublogUser.objects.get_or_create(callsign=call_sign_instance,
                                                                                                   defaults=clublog_user_data)
                    if not clublog_instance_created:
                        for attr, a_value in clublog_user_data.items():
                            setattr(clublog_instance, attr, a_value)
                        clublog_instance.save()


            self.stdout.write(self.style.SUCCESS('Successfully imported %d users from which %d are new from %s' % (
                counter, new_counter, options['url'])))
