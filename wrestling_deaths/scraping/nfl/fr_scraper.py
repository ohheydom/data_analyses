import requests
import pandas as pd
import numpy as np


nfl_data = pd.read_csv('../../csvs/nfl.csv')
years = np.arange(1946, 1947, 1)
names = np.array([])
for y in years:
    d = nfl_data[(nfl_data['birth_year'] == y) & (pd.isnull(nfl_data['death_year']))]['name'].tolist()
    names = np.concatenate((names, d), axis=0)

counter = 100
#last = 100
for n in names[counter:]:
    name = n.replace(" ", "+")
    with open("players/{}".format(n), 'w') as f:
        url = "http://www.pro-football-reference.com/search/search.fcgi?search={}&results=".format(name)
        r = requests.get(url)
        f.write(r.content)
    counter += 1
