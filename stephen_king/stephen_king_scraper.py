import re
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

def convert_title(s):
    return re.sub(r"[\'-\.:; ]", '', s).lower()

sk_movies = pd.read_csv('csvs/stephen_king_movies.csv')
for i, r in sk_movies.iterrows():
    filename = 'imdb_' + convert_title(r['title']+ r['year']) + '.html'
