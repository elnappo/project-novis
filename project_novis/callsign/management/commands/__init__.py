import sys

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
import requests

from ...models import Country, Callsign, DataImport, CallsignBlacklist
from ...utils import extract_callsign


class ImportCommand(BaseCommand):
    """
    Abstract class which includes common functionality for imports commands
    """
    # TODO Use bulk_create and bulk_update

    source = ""
    task = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.task:
            raise LookupError("task class variable is empty")

        self._start_time = timezone.now()
        self._import_user_email = "bot@project-novis.org"
        self._import_user = get_user_model().objects.get(email=self._import_user_email)
        self._callsign_counter = 0
        self._new_callsign_counter = 0
        self._update_callsign_counter = 0
        self._delete_callsign_counter = 0
        self._invalid_callsign_counter = 0
        self._blacklist_callsign_counter = 0
        self._error_counter = 0
        self._existing_callsigns = list(Callsign.objects.order_by("name").values_list('name', flat=True))
        self._callsign_blacklist = set(CallsignBlacklist.objects.order_by("callsign").values_list('callsign', flat=True))
        self._callsign_data_import_instance = DataImport.objects.create(start=self._start_time,
                                                                        task=self.task,
                                                                        description=self.help)
        self.countries = dict(Country.objects.values_list("name", "id"))
        self.session = requests.Session()
        self._write(self.help)
        self._write(f"Size of callsign list is {sys.getsizeof(self._existing_callsigns)} bytes")

    def _warning(self, message: str):
        self.stderr.write(self.style.WARNING(message))

    def _error(self, message: str):
        self.stderr.write(self.style.ERROR(message))

    def _success(self, message: str):
        self.stdout.write(self.style.SUCCESS(message))

    def _write(self, message: str):
        self.stdout.write(message)

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        raise NotImplementedError('subclasses of ImportCommand must provide a handle() method')

    def _handle_callsign(self, callsign: str, source: str = "", official: bool = False, return_instance: bool = True):
        self._callsign_counter += 1
        raw_callsign = extract_callsign(callsign)

        if not raw_callsign:
            self._invalid_callsign_counter += 1
            raise ValueError(f"Invalid callsign {callsign}")

        elif raw_callsign in self._callsign_blacklist:
            self._blacklist_callsign_counter += 1
            raise ValueError(f"Blacklisted callsign {callsign}")

        elif raw_callsign not in self._existing_callsigns:
            call_sign_instance, new_call_sign = Callsign.objects.get_or_create(
                name=raw_callsign,
                defaults={"name": raw_callsign,
                          "created_by_id": self._import_user.id,
                          "source": source if source else self.source,
                          "_official_validated": official})
            if new_call_sign:
                self._new_callsign_counter += 1
                call_sign_instance.set_default_meta_data()
                call_sign_instance.save()

            return call_sign_instance, new_call_sign

        else:
            if return_instance:
                call_sign_instance = Callsign.objects.get(name=raw_callsign)
                return call_sign_instance, False
            else:
                return None, False

    def _finish(self, extra_message: str = None):
        self._callsign_data_import_instance.callsigns = self._callsign_counter
        self._callsign_data_import_instance.new_callsigns = self._new_callsign_counter
        self._callsign_data_import_instance.updated_callsigns = self._update_callsign_counter
        self._callsign_data_import_instance.deleted_callsigns = self._delete_callsign_counter
        self._callsign_data_import_instance.invalid_callsigns = self._invalid_callsign_counter
        self._callsign_data_import_instance.blacklisted_callsigns = self._blacklist_callsign_counter
        self._callsign_data_import_instance.errors = self._error_counter
        self._callsign_data_import_instance.stop = timezone.now()
        self._callsign_data_import_instance.save()

        self._success(f"duration: {timezone.now() - self._start_time} "
                      f"callsings: {self._callsign_counter} "
                      f"new callsings: {self._new_callsign_counter} "
                      f"update callsings: {self._update_callsign_counter} "
                      f"delete callsings: {self._delete_callsign_counter} "
                      f"invalid callsigns: {self._invalid_callsign_counter} "
                      f"blacklisted callsigns: {self._blacklist_callsign_counter} "
                      f"error callsings: {self._error_counter}")
        if extra_message:
            self._success(extra_message)
