import time

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from ...models import CallSign
from ...utils import extract_callsign


class ImportCommand(BaseCommand):
    """
    Abstract class which includes common functionality for imports commands
    """

    source = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._start_time = time.time()
        self._import_user_id = 1
        self._import_user = get_user_model().objects.get(id=self._import_user_id)
        self._callsign_counter = 0
        self._new_callsign_counter = 0
        self._update_callsign_counter = 0
        self._delete_callsign_counter = 0
        self._error_counter = 0
        self._existing_callsigns = CallSign.objects.values_list('name', flat=True)

        self.stdout.write(self.help)

    def _warning(self, message: str):
        self.stderr.write(self.style.WARNING(message))

    def _error(self, message: str):
        self.stderr.write(self.style.ERROR(message))

    def _success(self, message: str):
        self.stderr.write(self.style.SUCCESS(message))

    def _handle_callsign(self, callsign: str):
        self._callsign_counter += 1
        raw_callsign = extract_callsign(callsign)

        if not raw_callsign:
            self._error_counter += 1
            self._warning(f"Invalid callsign {callsign}")
            return None, None

        elif raw_callsign not in self._existing_callsigns:
            call_sign_instance, new_call_sign = CallSign.objects.get_or_create(
                name=raw_callsign,
                defaults={"name": raw_callsign,
                          "created_by_id": self._import_user_id,
                          "source": self.source})
            if new_call_sign:
                self._new_callsign_counter += 1
                call_sign_instance.set_default_meta_data()
                call_sign_instance.save()

            return call_sign_instance, new_call_sign

        else:
            call_sign_instance = CallSign.objects.get(name=raw_callsign)
            return call_sign_instance, False

    def _finish(self, extra_message: str = None):
        self._success(f"duration: {time.time() - self._start_time} "
                      f"callsings: {self._callsign_counter} "
                      f"new callsings: {self._new_callsign_counter} "
                      f"update callsings: {self._update_callsign_counter} "
                      f"delete callsings: {self._delete_callsign_counter} "
                      f"error callsings: {self._error_counter}")
        if extra_message:
            self._success(extra_message)

