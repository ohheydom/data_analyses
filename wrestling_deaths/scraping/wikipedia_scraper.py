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

        Arguments
        ---------
        folder : str
            Folder location of the list of athletes
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
        folder_prefix : str
            Folder location to save the list of athletes to
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
                            f.write(urllib.unquote(v[6:]) + '\n')
                return
        for s in suffixes:
            content = requests.get(link+s)
            soup = BeautifulSoup(content.content, 'lxml')
            athletes = soup.select(select_statement)
            with open('{}/{}_{}_player_list'.format(folder_prefix, file_prefix, s), 'w') as f:
                for p in athletes:
                    v = p.a
                    if v:
                        v = v['href']
                        if v.startswith('/wiki'):
                            f.write(urllib.unquote(v[6:]) + '\n')

## NBA
suffixes = ['(A)', '(B)', '(C)', '(D)', '(E-F)', '(G)', '(H)', '(I-J)', '(K)', '(L)', '(M)', '(N-O)', '(P-Q)', '(R)', '(S)', '(T-V)', '(W-Z)']
link = "https://en.wikipedia.org/wiki/List_of_National_Basketball_Association_players_"
select_statement = 'div#mw-content-text div.div-col ul li'
file_prefix = 'nba'
folder_prefix = 'nba/name_lists'
nba = {'suffixes': suffixes, 'link': link, 'select_statement': select_statement,
        'file_prefix': file_prefix, 'folder_prefix': folder_prefix}

## NHL
suffixes = ['(A)', '(B)', '(C)', '(D)', '(E)', '(F)', '(G)', '(H)', '(I)', 
    '(J)', '(K)', '(L)', '(M)', '(N)', '(O)', '(P)', '(Q)', '(R)', '(S)', 
    '(T)', '(U-V)', '(W)', '(X-Z)']
link = "https://en.wikipedia.org/wiki/List_of_NHL_players_"
select_statement = 'div#mw-content-text div.div-col ul li'
file_prefix = 'nhl'
folder_prefix = 'nhl/name_lists'
nhl = {'suffixes': suffixes, 'link': link, 'select_statement': select_statement,
        'file_prefix': file_prefix, 'folder_prefix': folder_prefix}

## WWE
suffixes = ['(A-C)', '(D-H)', '(I-M)', '(N-R)', '(S-Z)']
link = 'https://en.wikipedia.org/wiki/List_of_WWE_alumni_'
select_statement = 'span.sorttext'
file_prefix = 'wwe_alumni'
folder_prefix = 'wrestling/name_lists'
wwe = {'suffixes': suffixes, 'link': link, 'select_statement': select_statement,
        'file_prefix': file_prefix, 'folder_prefix': folder_prefix}

## ECW
suffixes = None
link = 'https://en.wikipedia.org/wiki/List_of_Extreme_Championship_Wrestling_alumni'
select_statement = 'span.sorttext'
file_prefix = 'ecw_alumni'
folder_prefix = 'wrestling/name_lists'
ecw = {'suffixes': suffixes, 'link': link, 'select_statement': select_statement,
        'file_prefix': file_prefix, 'folder_prefix': folder_prefix}

## WCW
suffixes = None
link = 'https://en.wikipedia.org/wiki/List_of_World_Championship_Wrestling_alumni'
select_statement = 'span.sorttext'
file_prefix = 'wcw_alumni'
folder_prefix = 'wrestling/name_lists'
wcw = {'suffixes': suffixes, 'link': link, 'select_statement': select_statement,
        'file_prefix': file_prefix, 'folder_prefix': folder_prefix}

## AWA
suffixes = None
link = 'https://en.wikipedia.org/wiki/List_of_American_Wrestling_Association_alumni'
select_statement = 'div#mw-content-text ul li'
file_prefix = 'awa_alumni'
folder_prefix = 'wrestling/name_lists'
awa = {'suffixes': suffixes, 'link': link, 'select_statement': select_statement,
        'file_prefix': file_prefix, 'folder_prefix': folder_prefix}

## NWA
suffixes = None
link = 'https://en.wikipedia.org/wiki/List_of_NWA_Central_States_alumni'
select_statement = 'span.sorttext'
file_prefix = 'nwa_alumni'
folder_prefix = 'wrestling/name_lists'
nwa = {'suffixes': suffixes, 'link': link, 'select_statement': select_statement,
        'file_prefix': file_prefix, 'folder_prefix': folder_prefix}

## TNA Current
suffixes = None
link = 'https://en.wikipedia.org/wiki/List_of_Total_Nonstop_Action_Wrestling_personnel'
select_statement = 'span.vcard span.fn'
file_prefix = 'tna_current'
folder_prefix = 'wrestling/name_lists'
tna_current = {'suffixes': suffixes, 'link': link, 'select_statement': select_statement,
        'file_prefix': file_prefix, 'folder_prefix': folder_prefix}

## TNA Alumni
suffixes = None
link = 'https://en.wikipedia.org/wiki/List_of_Total_Nonstop_Action_Wrestling_alumni'
select_statement = 'span.sorttext'
file_prefix = 'tna_alumni'
folder_prefix = 'wrestling/name_lists'
tna_alumni = {'suffixes': suffixes, 'link': link, 'select_statement': select_statement,
        'file_prefix': file_prefix, 'folder_prefix': folder_prefix}

## Stampede Wrestling
suffixes = None
link = 'https://en.wikipedia.org/wiki/List_of_Stampede_Wrestling_alumni'
select_statement = 'span.sorttext'
file_prefix = 'stampede_alumni'
folder_prefix = 'wrestling/name_lists'
stampede = {'suffixes': suffixes, 'link': link, 'select_statement': select_statement,
        'file_prefix': file_prefix, 'folder_prefix': folder_prefix}

#w = WikipediaScraper()
#l = None
#w.save_lists_of_athletes(l['link'], l['suffixes'], l['select_statement'],
#        l['folder_prefix'], l['file_prefix'])
#w.download_data("{}/awa".format(l['folder_prefix']))


