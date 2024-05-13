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
monsters = []

# URL for parcing
url = "https://www.d20pfsrd.com/bestiary/bestiary-alphabetical/"

# For parcing
index = "index-monsters-{0}"

# File
output = "monsters.json"

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

def get_name(mod_soup):
    if mod_soup.find(class_ = re.compile("(^title$|^text$)")):
        #return mod_soup.find(class_ = re.compile("(^title|^text$)")).get_text().split("CR")[0].strip().replace("â", "'").replace("\u00e2\u0080\u0099", "'")
        return re.sub("(â|\u00e2\u0080\u0099|\u2018|\u2019)", "'", mod_soup.find(class_ = re.compile("(^title|^text$)")).get_text().split("CR")[0].strip())
    else:
        return None

def get_spells(mod_soup):
    spells = []
    if mod_soup.find_all('p', style=re.compile("margin-left:*")):
        for s in  mod_soup.find_all('p', style=re.compile("margin-left:*")):
            if s.find_all(class_ = "spell"):
                for spell in s.find_all(class_ = "spell"):
                    spells.append(re.sub("(â|\u00e2\u0080\u0099|\u2018|\u2019)", "'", spell.get_text().title().strip()))
        return list(set(spells))
    else:
        return []

def m(name, spells):
    jsn = {}
    jsn['name'] = name
    jsn['spells'] = spells
    return jsn

###### Program #######
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')


for alpha in soup.find_all(class_= 'page new parent'):
    first = True
    sub_page = requests.get(alpha.a['href'])
    sub_soup = BeautifulSoup(sub_page.text, 'html.parser')
    for sub_alpha in sub_soup.find_all('a'):
        monster = {}
        if sub_alpha.get('href') != None:
            if re.search('monster-listings',sub_alpha.get('href')):
                if first:
                    first = False
                    continue
                print(sub_alpha.get('href'))
                mob = requests.get(sub_alpha.get('href'))
                mod_soup = BeautifulSoup(mob.text, 'html.parser')
                name = get_name(mod_soup)
                spells = get_spells(mod_soup)
                print(f"[{name},{spells}]")
                if name:  
                    # monsters.append({name: spells})
                    monsters.append(m(name, spells))

    #             # For Debug
    #             if i == n:
    #                 break
    #             i = i + 1
    # break

with open (output, "w") as f:
    json.dump(monsters, f, indent=3, sort_keys=False)

exit(0)