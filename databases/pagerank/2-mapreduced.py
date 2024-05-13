#!/usr/bin/python3
# -*- coding: utf-8 -*-

###### Import ########

from bson.code import Code
from pymongo import MongoClient

###### Variable ######

# MongoDB configuration
server = 'localhost'
port = 27017
database = 'pathfinder'
column = 'spells'

###### Function ######

def _conMongoDB(server, port, database, column):
    # MongoDB
    client = MongoClient(server, port)
    db = client[database]
    collection = db[column]
    return collection

###### Program #######

# Connexion à MongoDB
collection = _conMongoDB(server, port, database, column)

# Map
map = Code(
"function() {                                  										"
"	if (this.components.length == 1 & this.components == 'V') {   					"
"		emit(this._id, [this.name, this.level, this.components]);                   "
"	}                                                                               "
"}                                                                                  "
)

# Reduce
reduce = Code(
"function(key, values) {"
"	return values;		"
"}                      "
)

# Exécution du MapReduce du la collection
results = collection.map_reduce(map , reduce, "reduced")

# Affichage du résultat obtenu
for result in results.find():
    print(result)

# Sortie du programme
exit(0)