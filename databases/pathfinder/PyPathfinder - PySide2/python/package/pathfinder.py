#!/usr/bin/python3
# -*- coding: utf-8 -*-

###### Import ########

import json
from pymongo import MongoClient

###### Variable ######


###### Function ######

class MongoDB:
	def __init__(self, server, port, database="Pathfinder", collection="Spells"):
		self.server = server
		self.port = int(port)
		self.database = database
		self.collection = collection
		self.connection()

	def connection(self):
		self.client = MongoClient(self.server, self.port)
		base = self.client[self.database]
		self.col = base[self.collection]

	def initJson(self, doc):
		try:
			self.result = self.col.insert_many(doc)
		except:
			pass

	def query(self, list_search):
		self.request = {}
		self.query_name(list_search[0])
		self.query_composents(list_search[1])
		self.query_level(list_search[2])
		self.query_classes(list_search[3])
		self.query_description(list_search[4])
		self.result = self.col.find(self.request)
		return [r for r in self.result]

	def query_name(self, value):
		if value:
			self.request['name'] = {'$regex': '.*{0}.*'.format(value)}

	def query_composents(self, value):
		if value:
			self.request['components'] = {'$all': value}

	def query_level(self, value):
		self.request['level'] = {'$gte': value[0], '$lte': value[1]}

	def query_classes(self, value):
		if value:
			self.request['classes'] = {'$all': value}

	def query_description(self, value):
		if value:
			self.request['description'] = {'$regex': '.*{0}.*'.format(value)}

	def query_monsters(self, name):
		self.mob = {}
		self.mob['name'] = {'$regex': '{0}'.format(name)}
		self.result = self.col.find(self.mob)
		try:
			return self.result[0]
		except:
			return None

###### Program #######

# Test
if __name__ == "__main__":
	mc = MongoDB('127.0.0.1', int('27017'))
	mc.connection()
	with open('C:\\Users\\Mickael\\PycharmProjects\\PyPathfinder\\src\\main\\resources\\base\\json\\spells.json', 'r') as f:
		spells = json.load(f)
		#print(spells)
	mc.initJson(Spells=spells)
	print(mc.result.inserted_ids)

	r = mc.query(['Of', ['M'], [1,1], [], ''])
	[print(a) for a in r]