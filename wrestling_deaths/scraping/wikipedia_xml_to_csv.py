from xml.etree import ElementTree as ET
import mwparserfromhell as mw
import pandas as pd
import re
from os import walk

class WikipediaXMLToCSV:
    def __init__(self):
        pass

    def convert_to_csv(self, folder, infoboxes, newfile):
        files = []
        for (dirpath, dirnames, filenames) in walk(folder):
            files = ['{}/{}'.format(dirpath, i) for i in filenames]
        df = pd.DataFrame()
        for f in sorted(files):
            df = df.append(self.clean_xml(f, infoboxes), ignore_index=True)
        df = df[['name', 'birth_city', 'birth_state', 'birth_country', 'death_city', 
            'death_state', 'death_country', 'birth_date', 'death_date']]
        df['birth_year'], df['birth_month'], df['birth_day'] = zip(*df['birth_date'])
        df['death_year'], df['death_month'], df['death_day'] = zip(*df['death_date'])
        df.drop(['birth_date', 'death_date'], axis=1, inplace=True)
        df.to_csv(newfile, encoding='utf-8', index=False)
        return df

    def find_errors(self, filename):
        """Finds errors in the files that need to be manually corrected
        """
        players = self.clean_xml(filename)
        errors = []
        previous = ''
        for p in players:
            if (not 'name' in p) or (not 'birth_date' in p):
                errors.append(previous)
            else:
                previous = p['name']
        return errors

    def clean_xml(self, filename, infoboxes, overwrite=False):
        """Reads the XML file and attempts to correct any missing information.
        You still need to go into the XML to manually correct items
        Paramters
        ---------
        filename : str
            The local filename of the xml file containing all the players
            of a certain letter

        returns
        -------
        player_list : list
            A list of dictionaries of all the players birthdates, birthplaces, deathdates,
            and deathplaces
        """
        p = []
        tree = ET.parse(filename)
        players = tree.findall('.//{http://www.mediawiki.org/xml/export-0.10/}text')
        for player in players:
            d = {'birth_country': 'US', 'death_country': 'US'}
            player_text = mw.parse(player.text)
            infobox = False
            for t in player_text.filter_templates():
                if t.name.matches('death date and age'):
                    d['death_date'] = [str(i) for i in t.params[0:3]]
                    d['birth_date'] = [str(i) for i in t.params[3:]]
                    continue
                if t.name.matches('birth date and age'):
                    d['birth_date'] = [str(i) for i in t.params]
                    d['death_date'] = ['', '', '']
                    continue
                if t.name.lower().strip() in infoboxes:
                    infobox = True
                    if 'name' in t:
                        d['name'] = t.get('name').value.encode('utf-8').strip()
                    if 'death_place' in t:
                        dp = t.get('death_place').value.strip().replace('[[', '').replace(']]','')
                        dps = dp.split(',')
                        if len(dps) > 1:
                            d['death_city'] = dps[0].strip()
                            d['death_state'] = dps[1].strip()
                        else:
                            d['death_city'] = dp.strip()
                    if 'birth_place' in t:
                        bp = t.get('birth_place').value.strip().replace('[[', '').replace(']]','')
                        bps = bp.split(',')
                        if len(bps) > 1:
                            d['birth_city'] = bps[0].strip()
                            d['birth_state'] = bps[1].strip()
                        else:
                            d['birth_city'] = bp.strip()
            p.append(d)
            if infobox == False and overwrite == True:
                player.text = """
{{Infobox NBA biography
| name = FILLINHERE
| birth_date = {{birth date and age|}}
| birth_place = [[ ]]
| death_date = {{death date and age|}}
| death_place = [[ ]]
}}""" + player.text
        if overwrite == True:
            tree.write(filename)
        return p

w = WikipediaXMLToCSV()

## NBA
#infoboxes = ['infobox basketball biography', 'infobox nba biography', 'infobox person']
#b.convert_to_csv('nba/xml_data', infoboxes, 'nba.csv')

## NHL

## Wrestling
