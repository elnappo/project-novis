import sys
from itertools import islice
from typing import List, Iterator, Tuple, Iterable, Dict

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
import requests

from ...models import Country, Callsign, DataImport, CallsignBlacklist
from ...utils import extract_callsign


class ImportCommand(BaseCommand):
    """
    Abstract class which includes common functionality for import commands
    """

    source: str = ""
    task: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.task:
            raise LookupError("task class variable is empty")

        self._batch_size: int = 500
        self._start_time = timezone.now()
        self._import_user_email: str = "bot@project-novis.org"
        self._import_user = get_user_model().objects.get(email=self._import_user_email)
        self._callsign_counter: int = 0
        self._new_callsign_counter: int = 0
        self._update_callsign_counter: int = 0
        self._delete_callsign_counter: int = 0
        self._invalid_callsign_counter: int = 0
        self._blacklist_callsign_counter: int = 0
        self._error_counter: int = 0
        self._existing_callsigns = list(Callsign.objects.order_by("name").values_list('name', flat=True))
        self._callsign_blacklist = set(CallsignBlacklist.objects.order_by("callsign").values_list('callsign', flat=True))
        self._callsign_data_import_instance = DataImport.objects.create(start=self._start_time,
                                                                        task=self.task,
                                                                        description=self.help)
        self.countries: Dict[str, int] = dict(Country.objects.values_list("name", "id"))
        self.session: requests.Session = requests.Session()
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

    def _extract_callsign(self, callsign: str) -> str:
        raw_callsign = extract_callsign(callsign)
        if not raw_callsign:
            self._warning(f"Invalid callsign {callsign}")
            return ""
        elif raw_callsign in self._callsign_blacklist:
            self._warning(f"Blacklisted callsign {callsign}")
            return ""
        elif raw_callsign not in self._existing_callsigns:
            return raw_callsign

    def _filter_callsigns_bulk_create(self, callsigns: Iterable[str], extra_fields=None, source: str = "", official: bool = False) -> Iterator[Callsign]:
        """Create a list of Callsign instances from dirty callsigns.

        Filter out already existing, blacklisted and invalid callsigns.

        :param callsigns: List of dirty callsigns (could be with origin country prefix or postfix e.g. /P)
        :param source: Callsign data source e.g. website or agency
        :param official: callsign is official and validated
        :return: Filtered list of Callsign instances
        """
        if extra_fields is None:
            extra_fields = {}

        # Callsign must be checked before bulk_create as bulk_create does not validate callsign name field
        for callsign in callsigns:
            self._callsign_counter += 1
            raw_callsign = extract_callsign(callsign)
            if not raw_callsign:
                self._invalid_callsign_counter += 1
                self._warning(f"Invalid callsign {callsign}")
            elif raw_callsign in self._callsign_blacklist:
                self._blacklist_callsign_counter += 1
                self._warning(f"Blacklisted callsign {callsign}")
            elif raw_callsign not in self._existing_callsigns:
                self._new_callsign_counter += 1
                yield Callsign(name=callsign,
                               created_by_id=self._import_user.id,
                               source=source if source else self.source,
                               _official_validated=official,
                               **extra_fields)

    def _callsign_bulk_create(self, callsigns: Iterable[str], extra_fields=None, source: str = "", official: bool = False) -> List[Callsign]:
        """Create callsigns and set default meta data

        Takes a list of dirty callsigns and adds the ones missing from database. Also set the default meta data, e.g.
        prefix, location,...

        :param callsigns: List of dirty callsigns (could be with origin country prefix or postfix e.g. /P)
        :param source: Callsign data source e.g. website or agency
        :param official: callsign is official and validated
        :return: List of Callsign instances created
        """
        if extra_fields is None:
            extra_fields = {}
        filtered_callsigns = self._filter_callsigns_bulk_create(callsigns, source=source, official=official)
        callsign_instances: List[Callsign] = list()

        # Create all missing callsigns
        self._write("Start bulk create")
        create_counter = 0
        while True:
            batch = list(islice(filtered_callsigns, self._batch_size))
            if not batch:
                break
            callsign_instances += Callsign.objects.bulk_create(batch, self._batch_size)
            create_counter += len(batch)
            self._write(f"created callsigns: {create_counter} ")

        # Add fields from Callsign.set_default_meta_data()
        fields = ["prefix", "country", "cq_zone", "itu_zone", "location", "_location_source"]
        self._write("Start bulk update default callsign data")
        default_data_counter = 0
        while True:
            batch = list(islice(callsign_instances, self._batch_size))
            if not batch:
                break

            # Set default data to new callsign instances
            for callsign_instance in batch:
                callsign_instance.set_default_meta_data()
            default_data_counter += len(batch)
            self._write(f"set default data on callsigns: {default_data_counter} ")
            Callsign.objects.bulk_update(callsign_instances, fields, self._batch_size)

        # Update DataImport record
        self._callsign_data_import_instance.callsigns = self._callsign_counter
        self._callsign_data_import_instance.new_callsigns = self._new_callsign_counter
        self._callsign_data_import_instance.invalid_callsigns = self._invalid_callsign_counter
        self._callsign_data_import_instance.blacklisted_callsigns = self._blacklist_callsign_counter
        self._callsign_data_import_instance.save()

        return callsign_instances

    def _callsign_bulk_update(self, callsign_instances: List[Callsign], fields: List[str]):
        self._write("Start bulk update")
        update_counter = 0
        while True:
            batch = list(islice(callsign_instances, self._batch_size))
            if not batch:
                break
            update_counter += len(batch)
            self._write(f"updated callsigns: {update_counter} ")
            Callsign.objects.bulk_update(callsign_instances, fields, self._batch_size)

    def _handle_callsign(self, callsign: str, source: str = "", official: bool = False, return_instance: bool = True) -> Tuple[Callsign, bool]:
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

    def _finish(self, extra_message: str = "", failed: bool = False, error_message: str = ""):
        self._callsign_data_import_instance.callsigns = self._callsign_counter
        self._callsign_data_import_instance.new_callsigns = self._new_callsign_counter
        self._callsign_data_import_instance.updated_callsigns = self._update_callsign_counter
        self._callsign_data_import_instance.deleted_callsigns = self._delete_callsign_counter
        self._callsign_data_import_instance.invalid_callsigns = self._invalid_callsign_counter
        self._callsign_data_import_instance.blacklisted_callsigns = self._blacklist_callsign_counter
        self._callsign_data_import_instance.errors = self._error_counter
        self._callsign_data_import_instance.stop = timezone.now()
        self._callsign_data_import_instance.duration = self._callsign_data_import_instance.stop - self._callsign_data_import_instance.start
        self._callsign_data_import_instance.finished = True
        self._callsign_data_import_instance.failed = failed
        self._callsign_data_import_instance.error_message = error_message
        self._callsign_data_import_instance.save()

        if not failed:
            self._success(f"duration: {timezone.now() - self._start_time} "
                          f"callsings: {self._callsign_counter} "
                          f"new callsings: {self._new_callsign_counter} "
                          f"update callsings: {self._update_callsign_counter} "
                          f"delete callsings: {self._delete_callsign_counter} "
                          f"invalid callsigns: {self._invalid_callsign_counter} "
                          f"blacklisted callsigns: {self._blacklist_callsign_counter} "
                          f"error callsings: {self._error_counter}")
        else:
            self._error("Command failed")
            self._error(error_message)
            self._error(f"duration: {timezone.now() - self._start_time} "
                        f"callsings: {self._callsign_counter} "
                        f"new callsings: {self._new_callsign_counter} "
                        f"update callsings: {self._update_callsign_counter} "
                        f"delete callsings: {self._delete_callsign_counter} "
                        f"invalid callsigns: {self._invalid_callsign_counter} "
                        f"blacklisted callsigns: {self._blacklist_callsign_counter} "
                        f"error callsings: {self._error_counter}")
        if extra_message:
            self._write(extra_message)
