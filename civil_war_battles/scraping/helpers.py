# -*- coding: utf-8 -*-
import re
import pandas as pd

STATES = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY',
}

def file_to_list(f):
    with open(f) as l:
        return l.read().splitlines()

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

def parse_coordinates(lat_lon):
    if len(lat_lon) == 0:
        return 0, 0
    if len(lat_lon) < 8:
        if lat_lon[1] == 'N':
            return float(str(lat_lon[0])), float("-" + str(lat_lon[2]))
        return float(str(lat_lon[0])), float(str(lat_lon[1]))
    return dms_to_dd(lat_lon[0:4]), dms_to_dd(lat_lon[4:8])

def dms_to_dd(v):
    val = round(float(str(v[0])) + float(str(v[1]))/60 + float(str(v[2]))/3600, 6)
    if v[3] == 'S':
        val *= -1
    if v[3] == 'W':
        val *= -1
    return val

def lat_lon_to_dd(lat_lon):
    """ lat_lon_to_dd converts latitude and longitude values from degrees, minutes
    and seconds to decimal degrees

    Arguments
    ---------
    lat_lon : str
        Latitude and longitude in degrees, minutes, seconds

    Returns
    -------
    lat : str
        Latitude in decimal degrees
    lon : str
        Longitude in decimal degrees
    pass
    """

    matcher = "(\d+)°(\d+)′(\d+)″(\w)"
    lat_lon_split = re.findall(matcher, lat_lon)
    la = lat_lon_split[0]
    lo = lat_lon_split[1]
    lat = round(float(la[0]) + float(la[1])/60 + float(la[2])/3600, 6)
    lon = round(float(lo[0]) + float(lo[1])/60 + float(lo[2])/3600, 6)
    if la[3] == 'S':
        lat *= -1
    if lo[3] == 'W':
        lon *= -1
    return (lat, lon)

def parse_casualties(st):
    """ parse_casualties takes an unmodified input string and attempts to split
    the casualties into four groups:
        total
        killed
        wounded
        captured/missing
    
    Arguments
    ---------
    st : string
        Unmodified input string from mediawiki

    Returns
    -------
    tuple
        (wounded, captured/missing, killed, total)
        A python tuple with the values of each category in the above order
    """

    st = st.strip()
    casualties = {'wounded':'', 'captured/missing': '', 'killed':''}
    if st.lower() == 'unknown':
        return '', '', '', ''
    if st.lower() == 'none':
        return '', '', '', 0
    matcher = re.compile("([~\d,-]+|unknown)\s?(range)?-?(wounded|killed|captured|casualties|missing|total|dead|kia)+", re.I)
    matches = re.findall(matcher, st)
    if matches:
        for m in matches:
            val = m[0]
            r = m[1]
            category = m[2].lower()
            if category in ['killed', 'dead', 'kia']:
                casualties['killed'] = val
            if category == 'wounded':
                casualties['wounded'] = val
            if category in ['captured', 'missing']:
                casualties['captured/missing'] = val
            if category in ['total', 'casualties']:
                casualties['total'] = val

        if len(casualties) > 1 and 'total' not in casualties:
            casualties['total'] = add_casualties(casualties)
        return casualties['wounded'], casualties['captured/missing'], casualties['killed'], casualties['total']
    try:
        v = int(st.replace(',', ''))
        casualties['total'] = v
        return casualties['wounded'], casualties['captured/missing'], casualties['killed'], casualties['total']
    except:
        return '', '', '', st

def add_casualties(d):
    adder_low = 0
    adder_high = 0
    sign = ''
    using_high = False
    for k, v in d.iteritems():
        if v == '':
            continue
        if v == 'unknown':
            sign = '+'
            continue
        if '-' in v:
            using_high = True
            v_low, v_high = v.split('-')
            if adder_high == 0:
                adder_high += adder_low
            adder_high += int(v_high.replace(',', '').replace('~', ''))
            adder_low += int(v_low.replace(',', '').replace('~', ''))
        else:
            adder_low += int(v.replace(',', '').replace('~', ''))
            if using_high == True:
                adder_high += int(v.replace(',', '').replace('~', ''))
    if adder_high == 0:
        return str(adder_low) + sign
    else:
        return str(adder_low) + sign + "-" + str(adder_high) + sign

def parse_combatant(st):
    if any(x in st for x in ['Union', 'United', 'USA']):
        return 0 #Union
    if any(x in st for x in ['Confederate', 'Missouri', 'CSA', 'Confederacy']):
        return 1 #Confederacy
    return 2 #Indians

def parse_result(st):
    if any(x in st for x in ['Union', 'United', 'USA']):
        return 1 #Union
    if any(x in st for x in ['Confederate', 'Missouri', 'CSA', 'Confederacy']):
        return 2 #Confederacy
    if any(x in st for x in ['Indians', 'Indian']):
        return 3 #Indians
    return 4 #Inconclusive

def city_state_split(city_state):
    """ Splits a city and a state if separated by a comma. If no comma is
    found, city_state_split returns an empty city and the original value
    as the state. The method also attempts to determine the country based on
    either the state value or if the second value in the input is a country.

    Arguments
    ---------
    city_state : str
        A string containing the city and the state

    Returns
    python typle
        Three strings: city, state, country
    """
    csp = city_state.strip().replace('[[', '').replace(']]', '').split(',')
    city = ''
    state = ''
    country = 'US'
    if len(csp) > 1:
        city = csp[0].strip()
        state = csp[1].strip()
        try:
            e = state.index('|')
        except:
            e = None
        state = state[:e]
    else:
        state = city_state.strip()
    if state in STATES:
        state = STATES[state]
    return city, state, country
