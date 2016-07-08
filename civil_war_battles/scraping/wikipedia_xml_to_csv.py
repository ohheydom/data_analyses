from xml.etree import ElementTree as ET
import mwparserfromhell as mw
import pandas as pd
import re
from os import walk
from helpers import parse_coordinates, print_full, city_state_split, parse_casualties, parse_combatant, parse_result, parse_strength
import pprint

class WikipediaXMLToCSV:
    def __init__(self):
        pass

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
        """


        files = []
        for (dirpath, dirnames, filenames) in walk(folder):
            files = ['{}/{}'.format(dirpath, i) for i in filenames]
        df = pd.DataFrame()
        for f in sorted(files):
            rows = self.clean_xml(f, infoboxes)
            df = df.append(rows, ignore_index=True)
        df.replace('unknown', '', inplace=True)
        df['start_year'], df['start_month'], df['start_day'] = zip(*df['start_date'])
        df['end_year'], df['end_month'], df['end_day'] = zip(*df['end_date'])
        df.drop(['start_date', 'end_date'], axis=1, inplace=True)
        df = df[['conflict', 'city', 'state', 'latitude', 'longitude', 'start_year', \
                'start_month', 'start_day', 'end_year', 'end_month', 'end_day', 'combatants', \
                'result', 'u_strength', 'c_strength', 'i_strength', 'uc_wounded', \
                'uc_captured', 'uc_killed', 'uc_total', 'cc_wounded', 'cc_captured', \
                'cc_killed', 'cc_total', 'ic_wounded', 'ic_captured', 'ic_killed', \
                'ic_total', 'a_wounded', 'a_captured', 'a_killed', 'a_total']]
        df = df.sort_values('conflict')
        df.to_csv(newfile, encoding='utf-8', index=False)

    def clean_xml(self, filename, infoboxes):
        """Reads the XML file and attempts to correct any missing information.
        You still need to go into the XML to manually correct items

        Parameters
        ---------
        filename : str
            The local filename of the xml file containing all the players
            of a certain letter
        infoboxes : list
            An array of possible matches for the infobox title data

        Returns
        -------
        p : list
            A list of dictionaries of all the pertinent information about the wars including:
                conflict title
                coordinates
                place
                dates
                combatants
                strengths
                casualties
                result
        """
        p = []
        uri = {'page': "http://www.mediawiki.org/xml/export-0.10/"}
        ET.register_namespace('', uri['page'])
        tree = ET.parse(filename)
        pages = tree.findall('.//page:page', uri)
        counter = 0
        for page in pages:
            title = page.find('page:title', uri).text
            page_text = page.find('page:revision/page:text', uri)
            d = {}
            casualties1 = {}
            casualties2 = {}
            casualties3 = {}
            combatant1 = ''
            combatant2 = ''
            strength1 = ''
            strength2 = ''
            battle_text = mw.parse(page_text.text)
            coords = False
            for t in battle_text.filter_templates():
                #Latitude/Longitude
                if coords == False and (t.name.matches('Coord') or t.name.matches('coord')):
                    d['latitude'], d['longitude'] = parse_coordinates(t.params)
                    coords = True
                    continue

                if t.name.lower().strip() in infoboxes:
                    #Strength
                    if 'strength1' in t:
                        strength1 = parse_strength(t.get('strength1').value.encode('utf-8'))
                    if 'strength2' in t:
                        strength2 = parse_strength(t.get('strength2').value.encode('utf-8'))
                    #Results
                    if 'result' in t:
                        d['result'] = parse_result(t.get('result').value.encode('utf-8'))

                    #Casualties
                    if 'casualties1' in t:
                        casualties1 = parse_casualties(t.get('casualties1').value.encode('utf-8'))
                    if 'casualties2' in t:
                        casualties2 = parse_casualties(t.get('casualties2').value.encode('utf-8'))
                    if 'casualties3' in t:
                        casualties3 = parse_casualties(t.get('casualties3').value.encode('utf-8'))

                    if casualties3:
                        d['a_wounded'], d['a_captured'], \
                        d['a_killed'], d['a_total'] = casualties3

                    #Combatants
                    if 'combatant1' in t:
                        combatant1 = parse_combatant(t.get('combatant1').value.encode('utf-8'))
                        if combatant1 == 0:
                            d['uc_wounded'], d['uc_captured'], \
                            d['uc_killed'], d['uc_total'] = casualties1
                            d['u_strength'] = strength1
                        if combatant1 == 1:
                            d['cc_wounded'], d['cc_captured'], \
                            d['cc_killed'], d['cc_total'] = casualties1
                            d['c_strength'] = strength1
                        if combatant1 == 2:
                            d['ic_wounded'], d['ic_captured'], \
                            d['ic_killed'], d['ic_total'] = casualties1
                            d['i_strength'] = strength1
                    if 'combatant2' in t:
                        combatant2 = parse_combatant(t.get('combatant2').value.encode('utf-8'))
                        if combatant2 == 0:
                            d['uc_wounded'], d['uc_captured'], \
                            d['uc_killed'], d['uc_total'] = casualties2
                            d['u_strength'] = strength2
                        if combatant2 == 1:
                            d['cc_wounded'], d['cc_captured'], \
                            d['cc_killed'], d['cc_total'] = casualties2
                            d['c_strength'] = strength2
                        if combatant2 == 2:
                            d['ic_wounded'], d['ic_captured'], \
                            d['ic_killed'], d['ic_total'] = casualties2
                            d['i_strength'] = strength2
                    d['combatants'] = combatant1 + combatant2

                    #Conflict
                    try:
                        d['conflict'] = t.get('conflict').value.encode('utf-8').strip()
                    except:
                        d['conflict'] = title

                    #Start Date
                    if 'date' in t:
                        dates = str(t.get('date').value)
                        dates_sp = dates[:dates.index("}}")].split('|')[1:]
                        d['start_date'] = [str(i) for i in dates_sp[0:3]]
                        if len(dates_sp) == 3:
                            d['end_date'] = [str(i) for i in dates_sp[0:3]]
                        else:
                            d['end_date'] = [str(i) for i in dates_sp[3:6]]

                    #Place
                    if 'place' in t:
                        csp = city_state_split(t.get('place').value)
                        d['city'], d['state'], d['country'] = csp
            p.append(d)
        return p

w = WikipediaXMLToCSV()
infoboxes = ['Infobox military conflict', 'infobox military conflict']
#w.clean_xml('battles/xml_data/battle_list_3.xml', infoboxes)
w.convert_to_csv('battles/xml_data/', infoboxes, '../csv/civil_war_battles.csv')
