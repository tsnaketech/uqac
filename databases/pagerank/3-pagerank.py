#!/usr/bin/python3
# -*- coding: utf-8 -*-

###### Import ########

from bson.code import Code
from pprint import pprint
from pymongo import MongoClient

###### Variable ######

# MongoDB configuration
server = 'localhost'
port = 27017
database = 'pathfinder'
col = 'pagerank'

# Itération
iteration = 20

graph = [
    { '_id':"A" , 
        'value':{'pagerank' : float(1) , 'links': ["B", "C"]}},
    { '_id':"B",
        'value':{'pagerank' : float(1) , 'links': ["C"]}},
    { '_id':"C",
        'value':{'pagerank' : float(1) , 'links': ["A"]}},
    { '_id':"D", 
        'value':{'pagerank' : float(1) , 'links': ["C"]}},
]

###### Function ######

def _exit_rank():
    print("Fin du programme !!!")
    exit(0)

def _print(results, i):
    if i+1 != 1 :
        print('*'*40 + '\n' + '*'*40 + '\n' + '*'*40)
    print(f"Valeur de I = {i+1}")
    for result in results.find():
        print(result)

def _conMongoDB(server, port, database, column):
    # MongoDB
    client = MongoClient(server, port)
    db = client[database]
    collection = db[column]
    return collection

def pagerank(graph, map, reduce, col, iteration = 20):
    for i in range(iteration):
        results = collection.map_reduce(map , reduce, col)
        _print(results, i)
    _exit_rank()
    return 0

###### Program #######

# Connexion à MongoDB
collection = _conMongoDB(server, port, database, col)
# Création de la collection dans MongoDB
try:
    collection.insert_many(graph)
except:
    pass

map = Code(
"function() {                           "
"   var page = this._id;                "
"   var pagerank = this.value.pagerank; "                  
"   var links = this.value.links;       "
"   var rank = pagerank / links.length; "
"   links.forEach(function(link) {      "
"       emit(link, rank);               "
"   });                                 "
"   emit(page, 0);                      "
"   emit(page, links);                  "
"}                                      "
)

reduce = Code(
"function(key, values) {                                                "
"   var damping = 0.85;                                                 "
"   var outlink_list = [];                                              "
"   var pagerank = 0;                                                   "
"   values.forEach(function(value) {                                    "
"       if (typeof(value) == 'object') {                                "
"           outlink_list = value                                        "
"       }   else   {                                                    "
"           pagerank += value                                           "
"       }                                                               "
"   });                                                                 "
"   pagerank = 1 - damping + ( damping * pagerank );                    "
"   return {'pagerank' : pagerank , 'links': outlink_list};"
"}                                                                      "
)

# Fonction pour l'exécution du MapReduce sur la collection
pagerank(graph, map, reduce, col)

# Suppression de la collection
collection.drop()

# Sortie du programme
exit(0)