from bs4 import BeautifulSoup
import requests
class NBAScraper:
    """ Scrapes the data from wikipedia and downloads the XML files
    """

    def __init__(self):
        pass

    def download_data(self):
        """Downloads the XML file for each individual letter
        """

    def save_lists_of_players(self, folder):
        links = ['B'] #['A', 'B', 'C', 'D', 'E-F', 'G', 'H', 'I-J', 'K', 'L', 'M', 'N-O', 'P-Q', 'R', 'S', 'T-V', 'W-Z']
        counter = 0
        for l in links:
            page = "https://en.wikipedia.org/wiki/List_of_National_Basketball_Association_players_({})".format(l)
            content = requests.get(page)
            soup = BeautifulSoup(content.content, 'lxml')
            players = soup.select('div#mw-content-text div.div-col ul li')
            with open('{}/{}_player_list'.format(folder, l), 'w') as f:
                for p in players:
                    v = p.a['href']
                    if v.startswith('/wiki'):
                        f.write(v[6:] + '\n')

# With these files, I'll input the text into https://en.wikipedia.org/wiki/Special:Export and download the XML file manually.
#scraper = NBAScraper()
#scraper.save_lists_of_players('players')
