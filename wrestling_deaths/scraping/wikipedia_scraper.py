from bs4 import BeautifulSoup
import requests
class WikipediaScraper:
    """ Scrapes the data from wikipedia and downloads the XML files
    """

    def __init__(self):
        pass

    def download_data(self):
        """Downloads the XML file for each individual letter
        """

    def save_lists_of_athletes(self, link, suffixes, select_statement, file_prefix):
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
            with open('{}_player_list'.format(file_prefix), 'w') as f:
                for p in athletes:
                    v = p.a['href']
                    if v.startswith('/wiki'):
                        f.write(v[6:] + '\n')
            return
        for s in suffixes:
            content = requests.get(l+s)
            soup = BeautifulSoup(content.content, 'lxml')
            athletes = soup.select(select_statement)
            with open('{}_{}_player_list'.format(file_prefix, s), 'w') as f:
                for p in athletes:
                    v = p.a['href']
                    if v.startswith('/wiki'):
                        f.write(v[6:] + '\n')

# Scrape NBA Data
suffixes = ['(A)', '(B)', '(C)', '(D)', '(E-F)', '(G)', '(H)', '(I-J)', '(K)', '(L)', '(M)', '(N-O)', '(P-Q)', '(R)', '(S)', '(T-V)', '(W-Z)']
link = "https://en.wikipedia.org/wiki/List_of_National_Basketball_Association_players_"
select_statement = 'div#mw-content-text div.div-col ul li'
file_prefix = 'nba'

# Scrape Wrestling Data

## WWE
suffixes = ['(A-C)', '(D-H)', '(I-M)', '(N-R)', '(S-Z)']
link = 'https://en.wikipedia.org/wiki/List_of_WWE_alumni_'
select_statement = 'span.sorttext'
file_prefix = 'wwe_alumni'

## ECW
suffixes = ['()', '()']
link = 'https://...'
select_statement = 'span.sorttext'
file_prefix = 'ecw_alumni'
