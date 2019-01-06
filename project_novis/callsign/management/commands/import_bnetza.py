import re
import collections
from io import BytesIO

import requests
import PyPDF2

from . import ImportCommand


class Command(ImportCommand):
    help = 'Import user data from German Federal Network Agency'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='?', type=str, default="https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Telekommunikation/Unternehmen_Institutionen/Frequenzen/Amateurfunk/Rufzeichenliste/Rufzeichenliste_AFU.pdf?__blob=publicationFile&v=48")

    def handle(self, *args, **options):
        regex = re.compile(r"D[A-Z][0-9][A-Z0-9]+")
        callsings = list()

        with requests.get(options['url'], stream=False) as r:
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
                        callsings.extend(a)
                    except KeyError:
                        continue

                unique_callsings = set(callsings)

                for callsing in unique_callsings:
                    self._handle_callsign(callsing)

                self._finish()
