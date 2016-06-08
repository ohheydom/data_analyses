import os
import glob
import re
from bs4 import BeautifulSoup
from helpers import money_converter
class IMDBDataParser:
    """ Parses the downloaded data of each movie and prepares the data
    for insertion into a database
    """
    def __init__(self):
        pass

    def parse_file(self, filename):
        """ Parses the file into a python dictionary

        Parameters
        ----------
        filename : str
            The local filename of the movie page

        Returns
        -------
        movie_list : dict
            A dictionary of all the pertinent movie information
        """
        d = {'cast': [], 'box_office': {}}
        with open(filename) as m_page:
            soup = BeautifulSoup(m_page, 'lxml')
            content = soup.select('div#content-2-wide')[0]

            main_top = content.select('div#main_top div.title-overview div#title-overview-widget')[0]
            d['rating'] = main_top.find('span', {'itemprop': 'ratingValue'}).text

            title_bar = main_top.select('div.titleBar')[0]
            d['title'] = title_bar.h1.contents[0].strip().encode('utf-8')

            subtext = title_bar.find('div', class_='subtext')
            content_rating = subtext.find('meta', {'itemprop': 'contentRating'})
            d['content_rating'] = content_rating['content'] if content_rating else None
            d['duration'] = int(subtext.find('time', {'itemprop': 'duration'})['datetime'][2:-1])
            d['genres'] = [g.text.encode('utf-8') for g in subtext.find_all('span', {'itemprop': 'genre'})]
            d['date_published'] = subtext.find('meta', {'itemprop': 'datePublished'})['content']

            plot_summary = main_top.find('div', class_='plot_summary')
            d['summary'] = plot_summary.find(class_='summary_text').text.encode('utf-8').strip()

            credit_summary_items = plot_summary.find_all('div', class_='credit_summary_item')
            d['director'] = credit_summary_items[0].span.a.span.text.encode('utf-8').strip()
            d['writer'] = credit_summary_items[1].span.a.span.text.encode('utf-8').strip()

            main_bottom = content.select('div#main_bottom')[0]

            d['imdb_rating'] = str(re.search('\d+', main_bottom.find('a', {'href': '/chart/top?ref_=tt_awd'}).text).group(0))
            cast = main_bottom.find('table', class_='cast_list').find_all('tr', class_=['even', 'odd'])
            for a in cast:
                actor = {}
                actor['actor'] = a.find('span', {'itemprop': 'name'}).text.strip().encode('utf-8')
                actor['character'] = a.select('td.character')[0].div.text.strip().encode('utf-8').replace('\n', '').replace('   ', '')
                d['cast'].append(actor)

            title_details = main_bottom.find('div', id='titleDetails')
            d['country'] =  [r.text for r in title_details.find(self.a_contains_country).find_all('a')]

            budget = title_details.find(self.div_contains_budget)
            gross = title_details.find(self.div_contains_gross)
            d['box_office']['budget'] = money_converter(budget.contents[2].encode('utf-8').strip()) if budget else None
            d['box_office']['gross'] = money_converter(gross.contents[2].encode('utf-8').strip()) if gross else None
            print d['box_office']['budget']
            return d

    def a_contains_country(self, elem):
        if elem.a:
            if "/country" in elem.a['href']:
                return True
        return False

    def div_contains_budget(self, elem):
        if elem.text:
            if 'Budget:' in elem.text:
                return True

    def div_contains_gross(self, elem):
        if elem.text:
            if 'Gross:' in elem.text:
                return True

    def parse_files(self, directory):
        movie_list = []
        filenames = glob.glob(directory + '/*.html')
        for f in filenames:
            movie_list.append(self.parse_file(f))
        return movie_list

x = IMDBDataParser()
x.parse_files('pages')
