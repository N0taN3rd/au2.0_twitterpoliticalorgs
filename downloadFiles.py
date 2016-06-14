from bs4 import BeautifulSoup
import re
import zipfile
from urllib import urlopen
from io import BytesIO

if __name__ == '__main__':

    r = open('Index of _FEC_electronic_.html','r')
    dlSoup = BeautifulSoup(r, "lxml")

    for td in dlSoup.find_all('a',href=True):
        match = re.search('^[a-z.:/A-Z]+((\d{4})\d+)\.zip$',td['href'])
        link = td['href']
        if match:
            year = int(match.group(2))
            if year >= 2015:
                print match.group(1)
                zipresp = urlopen(link)
                zipf = zipfile.ZipFile(BytesIO(zipresp.read()))
                zipf.extractall('datafiles/{0}'.format(match.group(1)))
                zipf.close()
                zipresp.close()


