import os
import re
import pandas as pd
from bs4 import BeautifulSoup as bs

sk_movies = pd.read_csv('csvs/stephen_king_movies.csv')
sk_books = pd.read_csv('csvs/stephen_king_books.csv')

def convert_title(s):
    return re.sub(r"[\'-\.:;/ ]", '', s).lower()

def update_book_ratings():
    for i, r in sk_books.iterrows():
        t = r['title']
        y = str(r['year'])
        if y == 'nan':
            y = ''
        filename = convert_title(t+y) + '.html'
        print filename
        if os.path.isfile('pages/gr_' + filename):
            with open('pages/gr_' + filename, 'r') as f:
                soup = bs(f, 'lxml')
                book_meta = soup.find('div', id='bookMeta')
                if not book_meta:
                    continue
                rating_value = book_meta.find('span', class_='average').string
                rating_count = re.search('(\d+,?\d+)', book_meta.find('span', class_='value-title').string)
                if rating_count:
                    rating_count = rating_count.group(0)
                print rating_count
                sk_books.loc[i, 'gr_rating'] = rating_value
                sk_books.loc[i, 'gr_rating_count'] = rating_count

    sk_books.to_csv('csvs/stephen_king_books.csv', index=False)

def update_movie_ratings():
    for i, r in sk_movies.iterrows():
        t = r['title']
        y = r['year']
        if y == '2017':
            continue
        filename = convert_title(t+y) + '.html'
        if os.path.isfile('pages/rt_' + filename):
            # imdb
            with open('pages/imdb_' + filename, 'r') as f:
                soup = bs(f, 'lxml')
                print filename
                imdbRatingdiv = soup.find('div', class_='imdbRating')
                if not imdbRatingdiv:
                    continue
                rating_value = imdbRatingdiv.find('span', {'itemprop': 'ratingValue'}).string
                rating_count = imdbRatingdiv.find('span', {'itemprop': 'ratingCount'}).string.replace(',', '')
                sk_movies.loc[i, 'imdb_rating'] = rating_value
                sk_movies.loc[i, 'imdb_rating_count'] = rating_count

            # rt
            with open('pages/rt_' + filename, 'r') as f:
                soup = bs(f, 'lxml')
                rtRatingdiv = soup.find('div', id='scorePanel')
                if not rtRatingdiv:
                    continue
                print filename
                rt_score_stats = rtRatingdiv.find('div', id='scoreStats')
                if rt_score_stats:
                    rating_divs = rt_score_stats.find_all('div')
                    critic_value = re.search('(\d\.?\d?)', rating_divs[0].text).group(0) #out of 10
                    critic_count = rating_divs[1].find_all('span')[1].string
                    sk_movies.loc[i, 'rt_critic_rating'] = critic_value
                    sk_movies.loc[i, 'rt_critic_count'] = critic_count

                audience_info = rtRatingdiv.find('div', class_='audience-info')
                if audience_info:
                    rating_divs = audience_info.find_all('div')
                    audience_value = re.search('(\d\.?\d?)', rating_divs[0].text).group(0) #out of 5
                    audience_count = re.search('(\d+\,?\d*)', rating_divs[1].text).group(0) #out of 5
                    sk_movies.loc[i, 'rt_audience_rating'] = audience_value
                    sk_movies.loc[i, 'rt_audience_count'] = audience_count

    sk_movies.to_csv('csvs/stephen_king_movies.csv', index=False)

#update_movie_ratings()
#update_book_ratings()
