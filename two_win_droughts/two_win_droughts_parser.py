import pandas as pd
import pprint as pp
from datetime import datetime as dt

"""
Data should be in a folder called data
All the text files can be found here: http://www.retrosheet.org/gamelogs/index.html

Rows in csv
-----------
0 - date
1 - game number
3 - visiting team
6 - home team
9 - visitor's score
10 - home team's score
"""

team_names = pd.read_csv('data/CurrentNames.csv', header=None)
tn = {}
for i, t in team_names.iterrows():
    tn[t[1]] = "{} {}".format(t[4],t[5])

def write_file(d, filename):
    with open(filename, 'war') as f:
        for t in sorted(d):
            vals = d[t]
            s = dt.strptime(str(vals['start_date']), "%Y%m%d")
            new_s = s.strftime("%m/%d/%Y")
            e = dt.strptime(str(vals['end_date']), '%Y%m%d')
            new_e = e.strftime('%m/%d/%Y')
            f.write("{}|{}|{}|{}\n".format(t, vals['streak'], new_s, new_e))

def update_dict(d, new_d, tn):
    for (t, v) in new_d.iteritems():
        if t in tn:
            t = tn[t]
        if not t in d:
            d[t] = { k: v[k] for k in ['streak', 'start_date', 'end_date'] }
        else:
            if d[t]['streak'] <= v['streak']:
                d[t] = { k: v[k] for k in ['streak', 'start_date', 'end_date'] }
    return d

def alternate_wins(start_year):
    d = {}
    for f in range(start_year, 2016):
        games = pd.read_csv('data/GL{}.TXT'.format(f), header=None)
        temp_d = {}

        gs = games.sort_values([0, 1])
        for i, (_, g) in enumerate(gs.iterrows()):
            h, a = g[6], g[3]
            for v in [a, h]:
                if not v in temp_d:
                    temp_d[v] = { 'past': None, 'current': None, 'streak': 0, 't_start_date': g[0], 'start_date': None, 'end_date': None, 'c_streak': 0 }
            if g[9] == g[10]:
                if temp_d[v]['streak'] < temp_d[v]['c_streak']:
                    temp_d[v]['streak'] = temp_d[v]['c_streak']
                    temp_d[v]['end_date'] = g[0]
                    temp_d[v]['start_date'] = temp_d[v]['t_start_date']
                temp_d[v]['c_streak'] = 1
                temp_d[v]['t_start_date'] = g[0]
                continue

            if g[9] > g[10]:
                temp_d[a]['current'] = 'w'
                temp_d[h]['current'] = 'l'
            else:
                temp_d[a]['current'] = 'l'
                temp_d[h]['current'] = 'w'

            for v in [a, h]:
                if temp_d[v]['current'] != temp_d[v]['past']:
                    temp_d[v]['c_streak'] += 1
                else:
                    if temp_d[v]['streak'] < temp_d[v]['c_streak']:
                        temp_d[v]['streak'] = temp_d[v]['c_streak']
                        temp_d[v]['end_date'] = g[0]
                        temp_d[v]['start_date'] = temp_d[v]['t_start_date']
                    temp_d[v]['c_streak'] = 1
                    temp_d[v]['t_start_date'] = g[0]

                temp_d[v]['past'] = temp_d[v]['current']

        d = update_dict(d, temp_d, tn)
    return d

def two_wins(start_year):
    d = {}
    for f in range(start_year, 2016):
        games = pd.read_csv('data/GL{}.TXT'.format(f), header=None)
        td = {}
        gs = games.sort_values([0, 1])
        for i, (_, g) in enumerate(gs.iterrows()):
            h, a = g[6], g[3]
            for v in [h, a]:
                if not v in td:
                    td[v] = { 'w_streak': 0, 'c_streak': 0, 'streak': 0, 't_start_date': g[0], 'start_date': None, 'end_date': None}
            if g[9] == g[10]:
                for v in [a, h]:
                    if td[v]['w_streak'] >= 2:
                        td[v]['t_start_date'] = g[0]
                    td[v]['w_streak'] = 0
                    td[v]['c_streak'] += 1
                    if td[v]['c_streak'] > td[v]['streak']:
                        td[v]['streak'] = td[v]['c_streak']
                        td[v]['end_date'] = g[0]
                        td[v]['start_date'] = td[v]['t_start_date']
                continue
                
            if g[9] > g[10]: 
                w, l = a, h
            else:
                w, l = h, a
                
            if td[l]['w_streak'] >=2:
                td[l]['t_start_date'] = g[0]

            td[w]['w_streak'] += 1
            if td[w]['w_streak'] >= 2:
                if td[w]['c_streak'] > td[w]['streak']:
                    td[w]['streak'] = td[w]['c_streak']
                    td[w]['end_date'] = g[0]
                    td[w]['start_date'] = td[w]['t_start_date']
                td[w]['c_streak'] = 0
            else:
                td[w]['c_streak'] += 1

            td[l]['w_streak'] = 0
            td[l]['c_streak'] += 1
        d = update_dict(d, td, tn)
    return d

def test_alternating_wins(d):
    assert d['Baltimore Orioles']['streak'] == 10, 'Incorrect value for the Orioles'
    assert d['Chicago Cubs']['streak'] == 15, 'Incorrect value for the Cubs'
    assert d['Kansas City Royals']['streak'] == 13, 'Incorrect value for the Royals'

def test_two_wins(d):
    assert d['Baltimore Orioles']['streak'] == 42, 'Incorrect value for the Orioles'
    assert d['Chicago Cubs']['streak'] == 53, 'Incorrect value for the Cubs'
    assert d['Kansas City Royals']['streak'] == 38, 'Incorrect value for the Royals'

start_year = 1900
alt = alternate_wins(start_year)
test_alternating_wins(alt)
alt_file = 'txts/alternating-w-l2'
write_file(alt, alt_file)

two = two_wins(start_year)
test_two_wins(two)
two_file = 'txts/two-win-droughts2'
write_file(two, two_file)
