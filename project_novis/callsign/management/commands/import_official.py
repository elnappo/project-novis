import collections
import re
from io import BytesIO

import PyPDF2
import requests

from . import ImportCommand


class Command(ImportCommand):
    help = 'Import user data from Federal Network Agencies'
    task = 'callsign_import_official'

    def germany(self):
        # update v parameter?
        url: str = "https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Telekommunikation/Unternehmen_Institutionen/Frequenzen/Amateurfunk/Rufzeichenliste/Rufzeichenliste_AFU.pdf?__blob=publicationFile&v=51"
        regex = re.compile(r"D[A-Z][0-9][A-Z0-9]+")
        callsigns = list()

        self._write("Import german callsings")
        with requests.get(url, stream=False) as r:
            if r.ok:
                data = BytesIO(r.content)
                pdf_reader = PyPDF2.PdfFileReader(data)
                number_of_pages = pdf_reader.getNumPages()
                c = collections.Counter(range(number_of_pages))

                for i in c:
                    try:
                        page = pdf_reader.getPage(i)
                        page_content = page.extractText()
                        a = regex.findall(page_content)
                        callsigns.extend(a)
                    except KeyError:
                        continue

                unique_callsigns = set(callsigns)

                for callsign in unique_callsigns:
                    callsign_instance, _ = self._handle_callsign(callsign, official=True, source="germany_official")
                    if not callsign_instance._official_validated:
                        callsign_instance._official_validated = True
                        callsign_instance.save()

    def finland(self):
        url = "https://eservices.viestintavirasto.fi/Licensesservices/Forms/AmateurLicenses.aspx"
        payload = {'__EVENTTARGET': '', 'ButtonDownload': ''}
        callsigns = list()

        self._write("Import finnish callsings")
        with requests.post(url, data=payload, stream=False) as r:
            if r.ok:
                for i in r.iter_lines(decode_unicode=True):
                    if not i:
                        continue
                    try:
                        callsign, status = i.split("\t", 1)
                    except ValueError:
                        # Handle invalid data in callsign list e.g.:
                        # OG73WR
                        #           VARAUS
                        self._write(f"Invalid data: {i}")
                    if status == "VOIMAS\t":
                        callsigns.append(callsign)

                    for callsign in set(callsigns):
                        callsign_instance, _ = self._handle_callsign(callsign, official=True, source="finland_official")
                        if not callsign_instance._official_validated:
                            callsign_instance._official_validated = True
                            callsign_instance.save()

    def usa(self):
        pass

    def austria(self):
        pass

    def handle(self, *args, **options):
        self.germany()
        self.finland()
        self.austria()
        self.usa()

        self._finish()
