#!/usr/bin/python3
# -*- coding: utf-8 -*-

########## For read json file ##########

# import json

# with open('Cours/BDD/monsters.txt', 'r') as f:
#     monsters = json.load(f)
# spark = [[k,v] for monster in monsters for k,v in monster.items()]

###### Import ########

import json
import re
import requests
import signal
import sqlite3
import string
import sys
from bs4 import BeautifulSoup

###### Variable ######

# List
spells = []

# URL for parcing
url = "https://www.d20pfsrd.com/magic/all-spells/{0}"

# File
output = "spells.json"

# Debug
i = 0 
n = 5

###### Function ######

def signal_exit(sig, frame):
        print('You pressed Ctrl + C !')
        if sys.argv[1] == 2 or sys.argv[1] == 3:
            closeSQLite(sqliteCon)
        exit(0)
signal.signal(signal.SIGINT, signal_exit)

def get_name(sub_soup):
    return re.sub("(â|\u00e2\u0080\u0099|\u2018|\u2019)", "'",sub_soup.select('h1')[0].text.strip().title())

def get_values(all_p):
    level = []
    classes = []
    values = [p.text for p in all_p if re.search('Level', p.text)]
    values = values[0].split(";")
    if len(values) > 1:
        values = [v for v in values if re.search('Level', v)]
        values = values[0][6:].split()
    elif len(values) == 1:
        if re.findall('[:]',values[0]):
            values = values[0].split(":")
            values = values[1][6:].split()
        else:
            values = values[0].split("Level")
            values = values[1].split()
    else:
        values = values[1][6:].split()
    for i in range(len(values)):
        if re.findall('[/]',values[i]):
            classe = values[i].split("/")
            [classes.append(cla.title().strip()) for cla in classe]
        elif not re.findall('[0-9]',values[i]):
            classes.append(values[i].title().strip())
        elif re.findall('[0-9]',values[i]):
            level = re.findall('[0-9]',values[i])
    try:
        level = int(level[0])
    except:
        level = 0
    return list(set(classes)), level

def get_components(all_p):
    components = []
    values = [p.text for p in all_p if re.search('Components', p.text)]
    try:
        values = values[0].split("Components")[1].split()
    except:
        return components
    for i in range(len(values)): 
        char = re.findall('V|S|M|DF',values[i])
        if re.findall('[/]',values[i]):
            chars = values[i].split('/')
            [components.append(c) for c in chars]
        elif char:
            components.append(''.join(char))
    return list(set(components))

def get_description(sub_soup):

    try:
        try:
            desc = re.sub("(â|\u00e2\u0080\u0099|\u2018|\u2019)", "'", sub_soup.find('p', class_='divider', text='DESCRIPTION').find_next('p').text)
        except:
            desc = re.sub("(â|\u00e2\u0080\u0099|\u2018|\u2019)", "'", sub_soup.find('p', style='font-size: 12px;font-weight: bold;border-top: thin solid;border-bottom: thin solid', text='DESCRIPTION').find_next('p').text)
    except:
        return ''
    return re.sub("(â)|â", "–", desc)

def spells_in_json(name, level, classes, components, description, url):
    jsn = {}
    jsn['name'] = name
    jsn['level'] = level
    jsn['classes'] = classes
    jsn['components'] = components 
    jsn['description'] = description
    jsn['url'] = url
    return jsn

###### Program #######

for c in string.ascii_lowercase:
    page = requests.get(url.format(c))
    soup = BeautifulSoup(page.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True) if a.text if re.search(f'{url.format(c)}/',a['href'])]
    
    for l in links:
        print(l)
        sub_page = requests.get(l)
        sub_soup = BeautifulSoup(sub_page.text, 'html.parser')
        all_p = sub_soup.find_all('p')
        name = get_name(sub_soup)
        classes, level = get_values(all_p)
        components = get_components(all_p)
        description = get_description(sub_soup)
        spells.append(spells_in_json(name, level, classes, components, description, l))

        print(name, level, classes, components, description, l)

        # # For Debug
        # if i == n:
        #     break
        # i = i + 1
    # break


with open (output, "w") as f:
    json.dump(spells, f, indent=3, sort_keys=False)

exit(0)