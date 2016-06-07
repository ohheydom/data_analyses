import requests

class IMDBScraper:
    """ IMDB Scraper that collects the data from all Top 250 movies.
    """
    TOP_250_LIST = 'http://www.imdb.com/chart/top'

    def __init__(self):
        pass

    def download_data(self):
        """Downloads the page for every movie listed in the Top 250 charts
        """
