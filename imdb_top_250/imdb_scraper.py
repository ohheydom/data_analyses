import requests
import os
from bs4 import BeautifulSoup

class IMDBScraper:
    """ IMDB Scraper that collects the data from all Top 250 movies.
    """
    TOP_250_LIST = 'http://www.imdb.com/chart/top'

    def __init__(self):
        pass

    def download_data(self):
        """Downloads the page for every movie listed in the Top 250 charts
        """
        content = requests.get(self.TOP_250_LIST)
        soup = BeautifulSoup(content.content, 'lxml')
        movies = soup.select('tbody.lister-list tr')
        for m in movies:
            title_column = m.select('td.titleColumn')
            link = self.format_link(title_column[0].a['href'])
            title = self.format_title(title_column[0].a.string.encode('utf-8'))
            path = 'pages/{}.html'.format(title)
            if os.path.isfile(path):
                continue
            response = requests.get(link)
            with open(path, 'wr') as f:
                f.write(response.content)

    def format_title(self, title):
        """Formats title into proper unix filename format

        Parameters
        ----------
        title : str
            The title of the movie with all original punctuation

        Returns
        -------
        new_title : str
            A properly formatted unix filename
        """
        new_title = ''.join(word.lower().strip('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ ') for word in title)
        return new_title

    def format_link(self, link):
        """Removes extra querydata from the end of each link

        Parameters
        ----------
        link : str
            The imdb link

        Returns
        -------
        new_link : str
            The imdb link without extra information
        """
        new_link = "/".join(link.split("/")[0:3])
        return "http://www.imdb.com" + new_link
