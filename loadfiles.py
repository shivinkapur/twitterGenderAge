import os, fnmatch
import bz2
import json
import pymongo
import re
import nltk
import nltk.data
from nltk.tokenize import RegexpTokenizer



#---------Saving JSON to MongoDB----------------------------------

def save_to_mongo(data,mongo_db,mongo_db_coll,**mongo_conn_kw):
	client1=pymongo.MongoClient(**mongo_conn_kw)
	db1=client1[mongo_db]
	coll1=db1[mongo_db_coll]
	return coll1.insert(data)

def load_from_mongo(mongo_db,mongo_db_coll,return_cursor=False, criteria=None, projection=None,**mongo_conn_kw):
	client1=pymongo.MongoClient(**mongo_conn_kw)
	db1=client1[mongo_db]
	coll1=db1[mongo_db_coll]
	if criteria is None:
		criteria={}

	if projection is None:
		cursor=coll1.find(criteria)
		print cursor
	else:
		cursor=coll1.find(criteria,projection)
		print cursor

	if return_cursor:
		return cursor
	else:
		return [ item for item in cursor ]


#-----------------Finding files in the directory-----------------
def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename



#-------------------------------------------------

for filename in find_files('/Users/rumeedhindsa/Documents/quarter3/cs246/project/database/2013/', '*.bz2'):
	f = bz2.BZ2File(filename, "r")
	for line in f:
		while True:
			try:
				jfile = json.loads(line)
				if('user' in jfile.keys()):
					line1=jfile["user"]["screen_name"]#+","+jfile["user"]["screen_name"]
					sent_tokenizer=nltk.data.load('nltk:tokenizers/punkt/english.pickle')
					sents = sent_tokenizer.tokenize(line1)
					validLetters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVYXYZ ' "
					for sentence in sents:
						newsentence = ''.join([char for char in sentence if char in validLetters])
					if (len(newsentence)>2) and (newsentence[0]!=''):
						#print jfile["user"]["screen_name"]
						json_to_store_into_mongo={'screen_name':jfile["user"]["screen_name"],'description':jfile["user"]["description"]}
						#save_to_mongo(json_to_store_into_mongo, '246ProjData', 'twittercoll1')
						save_to_mongo(abc, 'followers_jsonfiles', 'follower_ids')
				break
			except ValueError:
				line += next(f)


