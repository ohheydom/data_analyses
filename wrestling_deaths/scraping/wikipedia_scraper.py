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

        """Downloads the XML file for each individual letter
        """

        files = []
        url = "https://en.wikipedia.org/wiki/Special:Export?"
        directory = ""
        for (dirpath, dirnames, filenames) in walk(folder):
            files = ['{}/{}'.format(dirpath, i) for i in filenames]
            directory = dirpath

        directory = directory.split("/")[0]
        for f in files:
            names = self.file_to_list(f)
            querystring = self.format_querystring(names)
            r = requests.get(url + querystring)
            newfile = '{}/xml_data/{}.xml'.format(directory, f.split('/')[-1])
            with open(newfile, "wr") as xfile:
                xfile.write(r.content)

    def save_lists_of_athletes(self, link, suffixes, select_statement, folder_prefix, file_prefix):
        """Saves a list of the athletes' links on Wikipedia to be input into
        Wikipedia's XML Export Feature for downloading data

        Arguments
        ---------
        link : str
            String of the link without the suffix
        suffixes : list
            List of suffixes to add to the link to fetch the data
        select_statement : str
            Statement to be used to find all the link elements
        file_prefix : str
            String to prepend to every saved file
        """

        if suffixes == None:
            content = requests.get(link)
            soup = BeautifulSoup(content.content, 'lxml')
            athletes = soup.select(select_statement)
            with open('{}/{}_player_list'.format(folder_prefix, file_prefix), 'w') as f:
                for p in athletes:
                    v = p.a
                    if v:
                        v = v['href']
                        if v.startswith('/wiki'):
                            f.write(v[6:] + '\n')
                return
        for s in suffixes:
            content = requests.get(l+s)
            soup = BeautifulSoup(content.content, 'lxml')
            athletes = soup.select(select_statement)
            with open('{}/{}_{}_player_list'.format(folder_prefix, file_prefix, s), 'w') as f:
                for p in athletes:
                    v = p.a
                    if v:
                        v = v['href']
                        if v.startswith('/wiki'):
                            f.write(v[6:] + '\n')

w = WikipediaScraper()

# Scrape NBA Data
suffixes = ['(A)', '(B)', '(C)', '(D)', '(E-F)', '(G)', '(H)', '(I-J)', '(K)', '(L)', '(M)', '(N-O)', '(P-Q)', '(R)', '(S)', '(T-V)', '(W-Z)']
link = "https://en.wikipedia.org/wiki/List_of_National_Basketball_Association_players_"
select_statement = 'div#mw-content-text div.div-col ul li'
file_prefix = 'nba'

#w.save_lists_of_athletes(link, suffixes, select_statement, file_prefix)
#w.download_data("{}/name_lists".format(file_prefix)

# Scrape Wrestling Data

## WWE
suffixes = ['(A-C)', '(D-H)', '(I-M)', '(N-R)', '(S-Z)']
link = 'https://en.wikipedia.org/wiki/List_of_WWE_alumni_'
select_statement = 'span.sorttext'
file_prefix = 'wwe_alumni'
folder_prefix = 'wrestling/name_lists'

#w.save_lists_of_athletes(link, suffixes, select_statement, folder_prefix, file_prefix)
#w.download_data("{}/name_lists/wwe".format(file_prefix)

## ECW
suffixes = None
link = 'https://en.wikipedia.org/wiki/List_of_Extreme_Championship_Wrestling_alumni'
select_statement = 'span.sorttext'
file_prefix = 'ecw_alumni'
folder_prefix = 'wrestling/name_lists'

#w.save_lists_of_athletes(link, suffixes, select_statement, folder_prefix, file_prefix)
#w.download_data("{}/name_lists/ecw".format(file_prefix)

## WCW
suffixes = ['()', '()']
link = 'https://...'
select_statement = 'span.sorttext'
file_prefix = 'wcw_alumni'
folder_prefix = 'wrestling/name_lists'

#w.save_lists_of_athletes(link, suffixes, select_statement, folder_prefix, file_prefix)
#w.download_data("{}/name_lists/wcw".format(file_prefix)
