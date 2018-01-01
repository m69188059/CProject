from pymongo import MongoClient
client = MongoClient()
db= client['senti_Test']
collect= db['Test']

for post in collect.find():
	document = dict(post)
	test= document['content']
	print(test)
