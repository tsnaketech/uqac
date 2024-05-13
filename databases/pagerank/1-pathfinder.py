#!/usr/bin/python3
# -*- coding: utf-8 -*-

###### Import ########

import json
import re
import requests
import signal
import sqlite3
import sys
from bs4 import BeautifulSoup
from pymongo import MongoClient

###### Variable ######

# File SQLite
file = 'pathfinder.sql'

# MongoDB configuration
server = 'localhost'
port = 27017
database = 'pathfinder'
column = 'spells'

# Web
url = "http://www.dxcontent.com/SDB_SpellBlock.asp?SDBID={0}"

sys.argv[1] = int(sys.argv[1])

###### Function ######

def signal_exit(sig, frame):
        print('You pressed Ctrl + C !')
        if sys.argv[1] == 2 or sys.argv[1] == 3:
            closeSQLite(sqliteCon)
        exit(0)
signal.signal(signal.SIGINT, signal_exit)

def flevel(stat,l=1):
    level = (stat[0].text).split(";")[l][6:].split(",")
    for i in range(len(level)):
        wizard = re.findall('wizard',level[i])
        if wizard:
            num = re.findall('[0-9]',level[i])[0]
            return num
    try:
        num = re.findall('[0-9]',level[0])[0]
    except:
        num = flevel(stat,2)
    return num

def fcomponents(stat):
    components = (stat[2].text)[10:].split(",")
    l = []
    for i in range(len(components)): 
        slash = re.findall('[/]',components[i])
        char = re.findall('[A-Z]',components[i])
        if slash:
            component = components[i].strip()[:4]
            l.append(component)
        elif len(char) == 2:
            component = components[i].strip()[:2]
            l.append(component)
        elif len(char) == 0:
            continue
        else:
            component = re.findall('[A-Z]',components[i].strip())
            l.append(component[0])
    return l

def fresistance(stat):
    resistance = (stat[-1].text).split(";")
    for i in range(len(resistance)):
        resist = re.findall('Spell Resistance',resistance[i])
        if resist:
            resist = resistance[i].strip()[16:].strip()
            if resist == "see text":
                return 'no'
            else:
                return resist
    return 'no'

def conMongoDB(server, port, database, column):
    # MongoDB
    client = MongoClient(server, port)
    db = client[database]
    table = db[column]
    return table

def conSQLite(column, file):
    # SQLite
    sqliteCon  = sqlite3.connect(file)
    cursor = sqliteCon.cursor()
    sql = """
      CREATE TABLE IF NOT EXISTS {0}(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT NOT NULL,
        level INTEGER NOT NULL,
        components TEXT NOT NULL,
        spell_resistance TEXT NOT NULL
        )
    """.format(column)
    cursor.execute(sql)
    sqliteCon.commit()
    return sqliteCon, cursor

def insertMongoDB(table, spell):
    result = table.insert_one(spell)
    print('One post on MongoDB: {0}'.format(result.inserted_id))
    return 0

def insertSQLite(cursor, spell):
    spell['components'] = json.dumps(spell['components'])
    cursor.execute("""INSERT INTO spells(name, level,components,spell_resistance) VALUES(:name, :level,:components,:spell_resistance)""", spell)
    result = cursor.lastrowid
    print('One post on SQLite: {0}'.format(result))

def closeSQLite(sqliteCon):
    sqliteCon.commit()
    sqliteCon.close()

###### Program #######

if sys.argv[1] == 1 or sys.argv[1] == 3 :
    table = conMongoDB(server, port, database, column)
elif sys.argv[1] == 2 or sys.argv[1] == 3 :
    sqliteCon, cursor = conSQLite(column, file)
else:
    print('Select one argument, 1 for MongoDB, 2 for SQLite and 3 for MongoDB and SQLite')
    exit(1)

for j in range(1, 1975):
    if j == 1841 or j == 1972:
        continue
    page = requests.get(url.format(j))
    soup = BeautifulSoup(page.text, 'html.parser')
    print
    name = soup.find(class_='heading').text
    stat = soup.find_all(class_='SPDet')
    level = flevel(stat)
    components = fcomponents(stat)
    resistance = fresistance(stat)

    spell = {
        "name": name,
        "level": level,
        "components" : components,
        "spell_resistance" : resistance
    }
    # print(spell)
    if sys.argv[1] == 1 or sys.argv[1] == 3 :
        insertMongoDB(table, spell)
    elif sys.argv[1] == 2 or sys.argv[1] == 3 :
        insertSQLite(cursor, spell)

if sys.argv[1] == 2 or sys.argv[1] == 3:
    closeSQLite(sqliteCon)

exit(0)