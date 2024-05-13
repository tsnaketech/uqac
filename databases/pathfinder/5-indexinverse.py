#!/usr/bin/python3
# -*- coding: utf-8 -*-

# https://docs.databricks.com/data/data-sources/read-json.html
# https://stackoverflow.com/questions/39880269/pyspark-typeerror-condition-should-be-string-or-column
# https://stackoverflow.com/questions/29717257/pyspark-groupbykey-returning-pyspark-resultiterable-resultiterable

###### Import ########

import json
from pyspark import SparkConf, SparkContext, SQLContext

###### Variable ######

appName = 'Inverse'
master = 'local'

head = """
<!DOCTYPE html>
<html>
    <head>
        <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 5px;
                text-align: left;    
            }
        </style>
    </head>
"""
body = """
    <body>
        <table style='width:100%'>
            <tr>
                <th>Spells</th>
                <th>Monsters</th>
            </tr>
{0}
        </table>
    </body>
</html>
"""

# File
file_html = "./SpellsHTMLTable.html"
file_json = "./indexInverse.json"

# List
rows_list = []
spells = []

# Spark configuration
# sc = pyspark.SparkContext("local", "Spells")

###### Function ######

def s(name, monsters):
    jsn = {}
    jsn['name'] = name
    jsn['monsters'] = monsters
    return jsn

###### Program #######

conf = SparkConf().setAppName(appName).setMaster(master)
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
rddMonsters = sqlContext.read.option("multiline", "true").json('./monsters.json')
rddMonsters = rddMonsters.distinct().rdd.filter(lambda x: x[0] != None and x[0] != " " and x[1])
rddInverse = rddMonsters.flatMap(lambda x: map(lambda y: (y,x['name']),x['spells'])).groupByKey().map(lambda x : (x[0], list(x[1]))).collect()

for x in rddInverse:
    spell = x[0]
    monsters = ", ".join(x[1])
    rows_list.append('<tr colspan="1"><th>{0}</th><td>{1}</td></tr>'.format(spell,monsters))
    spells.append(s(x[0],x[1]))

body = body.format('\n'.join(rows_list))
html = head + body
 
with open(file_html, 'w') as f:
    f.write(html)

with open (file_json, "w") as f:
    json.dump(spells, f, indent=3, sort_keys=False)

exit(0)