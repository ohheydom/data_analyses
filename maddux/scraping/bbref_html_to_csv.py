from bs4 import BeautifulSoup as bs
from os import walk
import pandas as pd
from datetime import datetime as dt

folder = "pitchers"
d = pd.DataFrame(columns=['player_id', 'date', 'ip', 'pitches', 'runs', 'result'])
counter = 0
rows = []
for (dirpath, dirnames, filenames) in walk(folder):
    if dirpath == 'pitchers':
        continue
    player_id = dirpath.split("/")[1]
    print player_id
    for f in filenames:
        print f
        with open(dirpath + '/' + f) as fi:
            year = f[:4]
            soup = bs(fi, 'lxml')
            r = soup.find('table', id='pitching_gamelogs')
            r = r.find('tbody')
            trs = r.find_all('tr')
            for tr in trs:
                if 'thead' in tr['class']:
                    continue
                row = {'player_id': player_id}
                tds = tr.find_all('td')
                for i, td in enumerate(tds):
                    if i == 3:
                        da = td.text
                        if not da:
                            continue
                        d_header = da.find('(')
                        if d_header != -1:
                            da = da[:d_header]
                        da += " " + year
                        da = da.replace(u'\xa0', ' ')
                        try:
                            v = dt.strptime(da, "%b %d %Y")
                            row['year'] = v.year
                            row['month'] = v.month
                            row['day'] = v.day
                        except:
                            row['year'] = da
                    if i == 4:
                        row['team'] = td.string
                    if i == 6:
                        row['opp'] = td.string
                    if i == 7:
                        row['result'] = td.string
                    if i == 8:
                        row['inngs'] = td.string
                    if i == 11:
                        row['ip'] = td.string
                    if i == 13:
                        row['runs'] = td.string
                    if i == 21:
                        row['pitches'] = td.string
                    if i == 46:
                        row['entered'] = td.string
                        break
                rows.append(row)
d = pd.DataFrame(rows)
d.to_csv("../csvs/game_logs.csv", index=False)
