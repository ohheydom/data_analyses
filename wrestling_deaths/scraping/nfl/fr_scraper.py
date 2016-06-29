import requests
import pandas as pd
import numpy as np
from os import walk
import re


nfl_data = pd.read_csv('../../csvs/nfl.csv')
years = np.arange(1948, 1949, 1)
names = np.array([])
for y in years:
    d = nfl_data[(nfl_data['birth_year'] == y) & (pd.isnull(nfl_data['death_year']))]['name'].tolist()
    names = np.concatenate((names, d), axis=0)

counter = 0
#last = 100
for n in names[counter:]:
    name = n.replace(" ", "+")
    with open("players/{}".format(n), 'w') as f:
        url = "http://www.pro-football-reference.com/search/search.fcgi?search={}&results=".format(name)
        r = requests.get(url)
        f.write(r.content)

dtypes = {'death_month': str, 'death_year': str, 'death_day': str, 'birth_month': str, 'birth_year': str, 'birth_day': str,
        'year_start': str, 'year_end': str}
nfl = pd.read_csv('../../csvs/nfl.csv', dtype=dtypes)
added = []
s = 'data-death="([\d-]+)"'
for (dirpath, dirnames, filenames) in walk('players'):
    for fi in filenames:
        with open('players/{}'.format(fi), 'r') as f:
            for l in f:
                v= re.search(s, l)
                if v != None:
                    b = v.group(1)
                    year, month, day = b.split('-')
                    idx = nfl[(nfl['name'] == fi) & (nfl['birth_year'] == '1948')].index
                    if len(idx) == 0:
                        print 'Not found'
                        continue
                    nfl.set_value(idx[0], 'death_year', year)
                    added.append(fi)
                    if month == '00':
                        continue
                    nfl.set_value(idx[0], 'death_month', month)
                    if not day == '00':
                        nfl.set_value(idx[0], 'death_day', day)
            
print added
nfl.to_csv('../../csvs/nfl.csv', index=False)
