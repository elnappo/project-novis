import os
import re
import urllib.request

from bs4 import BeautifulSoup

# Download raw data from reverse beacon network and save under rbn/
html_page = urllib.request.urlopen("http://www.reversebeacon.net/raw_data/")
soup = BeautifulSoup(html_page)

for link in soup.findAll('a', attrs={'href': re.compile(r"dl\.php\?f=\d+")}):
    url = f"http://www.reversebeacon.net/raw_data/{link.get('href')}"
    filename = f"rbn/{link.get('href').split('=')[1]}.zip"
    if not os.path.isfile(filename):
        print(f"Downloading: {url}")
        urllib.request.urlretrieve(url, filename+".tmp")
        os.rename(filename+".tmp", filename)
