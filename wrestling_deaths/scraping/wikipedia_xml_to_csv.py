from xml.etree import ElementTree as ET
import mwparserfromhell as mw
import pandas as pd
import re
from os import walk
from helpers import city_state_split, print_full

class WikipediaXMLToCSV:
    def __init__(self):
        pass

    def build_promos_list(self, folder):
        """Builds a list of promotions that a wrestler has wrestled in

        Arguments
        ---------
        folder : str
            The location of all the text files of wrestlers names in each promotion

        Returns
        -------
        wrestlers : dict
            Wrestler's name is the key, an array of promotions is the value.
        """

        wrestlers = {}
        for (dirpath, dirnames, filenames) in walk(folder):
            promo = dirpath.split("/")[-1]
            for f in filenames:
                with open(dirpath + '/' + f) as fi:
                for line in fi:
                    t = line.strip().replace("_", " ")
                    if t in wrestlers:
                        wrestlers[t].append(promo)
                    else:
                        wrestlers[t] = [promo]
        return wrestlers

    def convert_to_csv(self, folder, infoboxes, newfile):
        """Converts folders of xml files to a csv

        Arguments
        ---------
        folder : str
            Location of the xml files
        infoboxes : list
            An array of possible matches for the infobox title data
        newfile : str
            The csv file you want to create

        Returns
        -------
        wrestlers : dict
            Wrestler's name is the key, an array of promotions is the value.
        """

        files = []
        for (dirpath, dirnames, filenames) in walk(folder):
            files = ['{}/{}'.format(dirpath, i) for i in filenames]
        df = pd.DataFrame()
        for f in sorted(files):
            rows = self.clean_xml(f, infoboxes)
            df = df.append(rows, ignore_index=True)
        df = df[['name', 'birth_city', 'birth_state', 'birth_country', 'death_city', 
            'death_state', 'death_country', 'birth_date', 'death_date', 'promos']]
        df['birth_year'], df['birth_month'], df['birth_day'] = zip(*df['birth_date'])
        df['death_year'], df['death_month'], df['death_day'] = zip(*df['death_date'])
        df.drop(['birth_date', 'death_date'], axis=1, inplace=True)
        df['sex'] = 'm'
        df.to_csv(newfile, encoding='utf-8', index=False)
        return df

    def find_errors(self, filename, infoboxes, overwrite=False):
        """Finds errors in the files that need to be manually corrected

        Arguments
        ---------
        filename : str
            Location of the xml file to check
        infoboxes : list
            An array of possible matches for the infobox title data
        overwrite : bool
            If you want the program to attempt to fix some of the errors and overwrite
            the original file. It fixes by:
                adding in the title as a missing name
                adding in a missing infobox section

        Returns
        -------
        errors : list
            A list of the previous wrestlers names that had completed information
        """

        players = self.clean_xml(filename, infoboxes, overwrite)
        errors = []
        previous = ''
        for p in players:
            #print_full("{}:{}".format(p['name'], p['birth_date']))
            if (not 'name' in p) or (not 'birth_date' in p):
                errors.append(previous)
            else:
                if len(p['birth_date']) != 3:
                    print p['name']
                previous = p['name']
        return errors

    def clean_xml(self, filename, infoboxes, overwrite=False):
        """Reads the XML file and attempts to correct any missing information.
        You still need to go into the XML to manually correct items

        Parameters
        ---------
        filename : str
            The local filename of the xml file containing all the players
            of a certain letter
        infoboxes : list
            An array of possible matches for the infobox title data
        overwrite : bool
            If you want the program to attempt to fix some of the errors and overwrite
            the original file. It fixes by:
                adding in the title as a missing name
                adding in a missing infobox section

        Returns
        -------
        p : list
            A list of dictionaries of all the athletes birthdates, birthplaces, deathdates,
            and deathplaces
        """
        p = []
        uri = {'page': "http://www.mediawiki.org/xml/export-0.10/"}
        ET.register_namespace('', uri['page'])
        tree = ET.parse(filename)
        pages = tree.findall('.//page:page', uri)
        for page in pages:
            title = page.find('page:title', uri).text
            page_text = page.find('page:revision/page:text', uri)
            #if page_text.text.lower().startswith('#redirect'):
            #    with open('redirects', 'a') as ff:
            #        x = page_text.text
            #        ff.write(x[x.index("[[")+2:x.index("]]")].encode('utf-8') + '\n')
            #    continue
            d = {'page_title': title}
            player_text = mw.parse(page_text.text)
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
                    try:
                        d['name'] = t.get('name').value.encode('utf-8').strip()
                    except:
                        t.add('name', title)
                    if 'death_place' in t:
                        dp = t.get('death_place').value.strip().replace('[[', '').replace(']]','')
                        d['death_city'], d['death_state'], d['death_country'] = city_state_split(dp)
                    try:
                        bp = t.get('birth_place').value.strip().replace('[[', '').replace(']]','')
                        d['birth_city'], d['birth_state'], d['birth_country'] = city_state_split(bp)
                    except:
                        pass
            page_text.text = unicode(player_text)
            p.append(d)
            if infobox == False and overwrite == True:
                page_text.text = """
{{Infobox professional wrestler
| name = """ + title + """
| birth_date = {{birth date and age|FILLIN}}
| birth_place = [[ ]]
| death_date = {{death date and age|}}
| death_place = [[ ]]
}}""" + page_text.text
        if overwrite == True:
            tree.write(filename, encoding='utf-8')
        return p

#w = WikipediaXMLToCSV()
## NBA
#infoboxes = ['infobox basketball biography', 'infobox nba biography', 'infobox person']
#w.convert_to_csv('nba/xml_data', infoboxes, '../csvs/nba.csv')

## NHL
#infoboxes = ['infobox ice hockey player', 'infobox person']
#w.convert_to_csv('nhl/xml_data', infoboxes, '../csvs/nhl.csv')

## Wrestling
#infoboxes = ['infobox professional wrestler', 'infobox person']
#w.find_errors('wrestling/xml_data/4.xml', infoboxes, False)
#w.convert_to_csv('wrestling/xml_data', infoboxes, 'wwe.csv')
