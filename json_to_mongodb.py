import json
import io
import os, fnmatch
import bz2
import pymongo
import re
import nltk
import nltk.data
from nltk.tokenize import RegexpTokenizer

#---------Saving JSON to MongoDB----------------------------------

client1=pymongo.MongoClient('localhost', 27017)
def save_to_mongo(data,mongo_db,mongo_db_coll):
    db1=client1[mongo_db]
    coll1=db1[mongo_db_coll]
    return coll1.insert(data)


#-----------------Finding files in the directory-----------------
def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename



#-------------------------------Reading each file and saving from Json to Mongo------------------

#for filename in find_files('/Users/shivinkapur/Desktop/246Code/2013', '*.bz2'):
for filename in find_files('/Users/shivinkapur/Desktop/246Code/TestJson', '*.bz2'):
    f = bz2.BZ2File(filename, "r")
    print filename
    for line in f:
        while True:
            try:
                jfile = json.loads(line)
                if('user' in jfile.keys()):
                    line1=jfile["user"]["screen_name"]
                    sent_tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
                    sentences= sent_tokenizer.tokenize(line1)
                    validLetters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVYXYZ ' "

                    for sentence in sentences:
                        newsentence = ''.join([char for char in sentence if char in validLetters])

                    line2=jfile["text"]#+","+jfile["user"]["screen_name"]
                    sentences= sent_tokenizer.tokenize(line2)

                    for sentence in sentences:
                        newsentence2 = ''.join([char for char in sentence if char in validLetters])

                    line3=jfile["user"]["description"]#+","+jfile["user"]["screen_name"]
                    sentences= sent_tokenizer.tokenize(line3)

                    for sentence in sentences:
                        newsentence3 = ''.join([char for char in sentence if char in validLetters])

                    line4=jfile["user"]["name"]#+","+jfile["user"]["screen_name"]
                    sentences= sent_tokenizer.tokenize(line4)

                    for sentence in sentences:
                        newsentence4 = ''.join([char for char in sentence if char in validLetters])

                    if("hashtags" in jfile["entities"].keys()):
                        if(jfile["entities"]["hashtags"] is not None):
                            a=[]
                            a=jfile["entities"]["hashtags"]
                            print(a[0]["text"])
                            #if(["entities"]["hashtags"][0] is not None):# is not ''):
                            line5=jfile["entities"]["hashtags"][0]#+","+jfile["user"]["screen_name"]
                            print(line5)
                            # sentences= sent_tokenizer.tokenize(line5)

                            # for sentence in sentences:
                            #     newsentence5 = ''.join([char for char in sentence if char in validLetters])
                    else:
                        newsentence5=''


                    if ((len(newsentence)>2) and (newsentence[0]!='') and (jfile["lang"]=="en")):
                        
                        json_to_store_into_mongo={
                        #'tweet':jfile["text"],
                        'tweet':newsentence2,
                        'source':jfile["source"],
                        'user_id':jfile["user"]["id"],
                        'orig_name':jfile["user"]["name"],
                        'name':newsentence4,
                        'orig_screen_name':jfile["user"]["screen_name"],
                        'screen_name':newsentence,
                        #'description':jfile["user"]["description"],
                        'description':newsentence3,
                        'followers':jfile["user"]["followers_count"],
                        'friends':jfile["user"]["friends_count"],
                        'created_at':jfile["user"]["created_at"],
                        'favourites_count':jfile["user"]["favourites_count"],
                        'time_zone':jfile["user"]["time_zone"],
                        #'hashtags':jfile["entities"]["hashtags"],
                        #'hashtags':newsentence5,
                        'language':jfile["lang"]
                        }

                        #print jfile["user"]["screen_name"]
                        
                        #save_to_mongo(json_to_store_into_mongo, '246ProjData', 'twittercoll1')
                        save_to_mongo(json_to_store_into_mongo, 'followers_jsonfiles', 'follower_ids')
                break
            except ValueError:
                line += next(f)

