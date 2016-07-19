import requests
import re
import os
from bs4 import BeautifulSoup as bs

page = 'http://www.baseball-reference.com/'
search = 'http://www.baseball-reference.com/search/search.fcgi?search='
gl_link = 'http://www.baseball-reference.com/players/gl.cgi?id={}&t=p&year={}'

def downloadFiles(soup):
    player_link = soup.select('head link[rel="canonical"]')[0]['href']
    player_id = re.search("http:\/\/.+\/(.+)\.", player_link).group(1)
    debut_link = soup.find(text='Debut').parent['href']
    debut = int(re.search("(\d+)", debut_link).group(0))
    retired = 2016
    last_game_link = soup.find(text='Last Game')
    if last_game_link:
        retired = int(re.search("(\d+)", last_game_link.parent['href']).group(0))
    for i in range(max(1988, debut), retired+1):
        path = 'pitchers/{}/{}.html'.format(player_id, i)
        if not os.path.exists('pitchers/' + player_id):
            os.makedirs('pitchers/' + player_id)
        if os.path.isfile(path):
            continue
        response = requests.get(gl_link.format(player_id, i))
        if soup.find(text='No Data for this season'):
            continue
        with open(path, 'wr') as f:
            f.write(response.content)

def iterate_over_players:
    with open('top_50_pitchers', 'r') as pitchers:
        for pitcher in pitchers:
            p = pitcher.strip().replace(" ", "+")
            c = requests.get(search + p)
            soup = bs(c.content, 'lxml')
            if soup.find(text='MLB Players '):
                print "Multiple: {}".format(p)
                continue

            print "Working: {}".format(p)
            downloadFiles(soup)

#iterate_over_players
