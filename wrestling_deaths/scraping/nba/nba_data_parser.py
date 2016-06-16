from xml.etree import ElementTree as ET
import mwparserfromhell as mw

class NBADataParser:
    def __init__(self):
        pass

    def find_errors(self, filename):
        """Finds errors in the files that need to be manually corrected
        """
        players = self.parse_file(filename)
        errors = []
        previous = ""
        for p in players:
            if (not 'name' in p) or (not 'birth_date' in p):
                errors.append(previous)
            else:
                previous = p['name']
        return errors

    def parse_file(self, filename):
        """ Parses the XML file into a python dictionary

        Paramters
        ---------
        filename : str
            The local filename of the xml file containing all the players
            of a certain letter

        returns
        -------
        player_list : dict
            A list of dictionaries of all the players birthdates, birthplaces, deathdates,
            and deathplaces
        """

        p = []
        tree = ET.parse(filename)
        players = tree.findall(".//{http://www.mediawiki.org/xml/export-0.10/}text")
        for player in players:
            d = {}
            t = mw.parse(player.text)
            tem = t.filter_templates()
            for t in tem:
                if t.name.matches("death date and age"):
                    d['death_date'] = t.params[0:3]
                    d['birth_date'] = t.params[3:]
                    continue
                if t.name.matches("birth date and age"):
                    d['birth_date'] = t.params
                    continue
                
                if t.name.matches("Infobox basketball biography") or t.name.matches("Infobox NBA biography") or t.name.matches("Infobox person"):
                    if "death_place" in t:
                        d['death_place'] = t.get("death_place").value.strip()
                    if 'name' in t:
                        d['name'] = t.get('name').value.encode("utf-8").strip()
                    if 'birth_place' in t:
                        d['birth_place'] = t.get('birth_place').value.strip()
            p.append(d)
        return p
    
b = NBADataParser()
print b.find_errors("players/xml_data/ef.xml")
"""Use the following to fix errors in the xml
{{Infobox NBA biography
| name = 
| birth_date = {{birth date and age|}}
| birth_place = [[ ]]
| death_date = {{death date and age|}}
| death_place = [[ ]]
}}
"""
