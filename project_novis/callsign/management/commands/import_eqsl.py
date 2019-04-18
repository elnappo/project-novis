from . import ImportCommand


class Command(ImportCommand):
    help = 'Import EQSL user data'
    source = "eqsl.cc"
    task = "callsign_import_eqsl"

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='?', type=str, default="http://www.eqsl.cc/QSLCard/DownloadedFiles/AGMemberlist.txt")

    def run(self, url):
        r = self.session.get(url, stream=False)
        if r.status_code != 200:
            raise Exception(f"Failed to download {url} status code {r.status_code}")

        extra_fields = {"eqsl": True}
        callsign_instances = self._callsign_bulk_create(r.iter_lines(decode_unicode=True), extra_fields=extra_fields)

        # TODO update existing callsigns

    def handle(self, *args, **options):
        self._write(f"Download callsign data from { options['url'] }")

        try:
            self.run(options['url'])
            self._finish()
        except Exception as e:
            self._finish(failed=True, error_message=str(e))
            raise e
