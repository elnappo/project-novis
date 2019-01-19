import re
import collections
from io import BytesIO

import requests
import PyPDF2

from . import ImportCommand


class Command(ImportCommand):
    help = 'Import user data from Federal Network Agencies'

    def germany(self):
        # update v parameter?
        url = "https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Telekommunikation/Unternehmen_Institutionen/Frequenzen/Amateurfunk/Rufzeichenliste/Rufzeichenliste_AFU.pdf?__blob=publicationFile&v=48"
        regex = re.compile(r"D[A-Z][0-9][A-Z0-9]+")
        callsigns = list()

        self._write("Import german callsings")
        with requests.get(url, stream=False) as r:
            if r.ok:
                data = BytesIO(r.content)
                pdfReader = PyPDF2.PdfFileReader(data)
                number_of_pages = pdfReader.getNumPages()
                c = collections.Counter(range(number_of_pages))

                for i in c:
                    try:
                        page = pdfReader.getPage(i)
                        page_content = page.extractText()
                        a = regex.findall(page_content)
                        callsigns.extend(a)
                    except KeyError:
                        continue

                unique_callsigns = set(callsigns)

                for callsign in unique_callsigns:
                    callsign_instance, _ = self._handle_callsign(callsign, official=True, source="germany_official")
                    if not callsign_instance.official_validated:
                        callsign_instance.official_validated = True
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

                    callsign, status = i.split("\t", 1)
                    if status == "VOIMAS\t":
                        callsigns.append(callsign)

                    unique_callsigns = callsigns
                    for callsign in unique_callsigns:
                        callsign_instance, _ = self._handle_callsign(callsign, official=True, source="finland_official")
                        if not callsign_instance.official_validated:
                            callsign_instance.official_validated = True
                            callsign_instance.save()

    def handle(self, *args, **options):
        self.germany()
        self.finland()

        self._finish()
