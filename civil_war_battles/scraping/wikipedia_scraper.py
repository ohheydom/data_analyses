from bs4 import BeautifulSoup
import requests
import urllib
from helpers import file_to_list
from os import walk

class WikipediaScraper:
    """ Scrapes the data from wikipedia and downloads the XML files
    """

    def __init__(self):
        pass

    def format_querystring(self, names):
        querystring = "catname=&curonly=1&wpEditToken=%2B%5C&title=Special%3AExport"
        pages = "&pages="
        for n in names:
            pages = pages + n.replace(" ", "+") + "%0D%0A"
        return querystring + pages

    def download_data(self, folder):
        """Downloads the XML file for each battle

        Arguments
        ---------
        folder : str
            Folder location of the list of battles
        """

        files = []
        url = "https://en.wikipedia.org/wiki/Special:Export?"
        directory = ""
        for (dirpath, dirnames, filenames) in walk(folder):
            files = ['{}/{}'.format(dirpath, i) for i in filenames]
            directory = dirpath

        directory = directory.split("/")[0]
        for f in files:
            names = file_to_list(f)
            querystring = self.format_querystring(names)
            r = requests.get(url + querystring)
            newfile = '{}/{}.xml'.format(directory, f.split('/')[-1])
            with open(newfile, "wr") as xfile:
                xfile.write(r.content)

    def save_lists_of_battles(self, links, folder_prefix):
        """Saves a list of the battle links on Wikipedia to be input into
        Wikipedia's XML Export Feature for downloading

        Arguments
        ---------
        link : str
            String of the link without the suffix
        folder_prefix : str
            Folder location to save the list of athletes to
        file_prefix : str
            String to prepend to every saved file
        """

        content = requests.get(link)
        soup = BeautifulSoup(content.content, 'lxml')
        tables = soup.find_all('table', {'class': "sortable"})
        with open('{}/battle_list'.format(folder_prefix), 'w') as f:
            for table in tables:
                for tr in table.find_all('tr'):
                    td = tr.find('td')
                    if td:
                        v = td.a
                        if v:
                            v = v['href']
                            if v.startswith('/wiki'):
                                f.write(urllib.unquote(v[6:]) + '\n')
            return

link = 'https://en.wikipedia.org/wiki/List_of_American_Civil_War_battles'
folder_prefix = 'battles/'
w = WikipediaScraper()
#w.save_lists_of_battles(link, folder_prefix)
w.download_data(folder_prefix)
