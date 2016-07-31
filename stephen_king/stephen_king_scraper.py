import math
import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

def convert_title(s):
    return re.sub(r"[\'-\.:;/ ]", '', s).lower()

sk_movies = pd.read_csv('csvs/stephen_king_movies.csv')
for i, r in sk_movies.iterrows():
    #imdb
    imdb_filename = 'imdb_' + convert_title(r['title']+ r['year']) + '.html'
    if not os.path.isfile('pages/' + imdb_filename):
        imdb_link = r['imdb_link']
        imdb_response = requests.get(imdb_link)
        with open("pages/" + imdb_filename, 'wr') as f:
            f.write(imdb_response.content.strip())
    #rt
    rt_filename = 'rt_' + convert_title(r['title']+ r['year']) + '.html'
    if not os.path.isfile('pages/' + rt_filename):
        rt_link = r['rt_link']
        if math.isnan(rt_link):
            continue
        rt_response = requests.get(rt_link)
        with open("pages/" + rt_filename, 'wr') as f:
            f.write(rt_response.content.strip())


sk_books = pd.read_csv('csvs/stephen_king_books.csv')
for i, r in sk_books.iterrows():
    #gr
    y = r['year']
    if math.isnan(y):
        y = ''
    else:
        y = str(y)
    gr_filename = 'gr_' + convert_title(r['title']+y) + '.html'
    if not os.path.isfile('pages/' + gr_filename):
        gr_link = r['gr_link']
        if str(gr_link) == 'nan':
            continue
        gr_response = requests.get(gr_link)
        with open("pages/" + gr_filename, 'wr') as f:
            f.write(gr_response.content.strip())
