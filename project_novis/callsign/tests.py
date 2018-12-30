from django.test import TestCase

from .utils import generate_aprs_passcode


class APRSPasscodeTestCase(TestCase):
    def setUp(self):
        self.known_valid_passcodes = (
            ("KI4SWY", 23457),
            ("DO2FMW", 18620)
        )

    def test_verify_validate(self):
        for i in self.known_valid_passcodes:
            self.assertEqual(generate_aprs_passcode(i[0]), i[1])
