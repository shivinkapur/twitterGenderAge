import pymongo
import csv
from pymongo import Connection
import nltk
import string
import os
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import brown
from nltk.corpus import stopwords

import re
from itertools import groupby


# myNamesDict = dict() 
# noOfLines = 0

# with open('dict1.csv', 'wb') as csvfile:
# 	with open('dict_1.txt', 'rb') as b:
# 		bottles11 = file.read(b)
# 		word_tokenizer = RegexpTokenizer(r'\w+')
# 		tokenized_words1 = word_tokenizer.tokenize(bottles11)
# 		spamwriter = csv.writer(csvfile, delimiter=',')
# 		for w in tokenized_words1:
# 			spamwriter.writerow([w])
# 			#print w

# with open('dict2.csv', 'wb') as csvfile:
# 	with open('dict_2.txt', 'rb') as b2:
# 		bottles11 = file.read(b2)
# 		word_tokenizer = RegexpTokenizer(r'\w+')
# 		tokenized_words1 = word_tokenizer.tokenize(bottles11)
# 		spamwriter = csv.writer(csvfile, delimiter=',')
# 		for w in tokenized_words1:
# 			spamwriter.writerow([w])
# 			#print w

# with open('dict3.csv', 'wb') as csvfile:
# 	with open('dict_3.txt', 'rb') as b2:
# 		bottles11 = file.read(b2)
# 		word_tokenizer = RegexpTokenizer(r'\w+')
# 		tokenized_words1 = word_tokenizer.tokenize(bottles11)
# 		spamwriter = csv.writer(csvfile, delimiter=',')
# 		for w in tokenized_words1:
# 			spamwriter.writerow([w])
# 			#print w

# with open('dict4.csv', 'wb') as csvfile:
# 	with open('dict_4.txt', 'rb') as b2:
# 		bottles11 = file.read(b2)
# 		word_tokenizer = RegexpTokenizer(r'\w+')
# 		tokenized_words1 = word_tokenizer.tokenize(bottles11)
# 		spamwriter = csv.writer(csvfile, delimiter=',')
# 		for w in tokenized_words1:
# 			spamwriter.writerow([w])
# 			#print w

# with open('dict5.csv', 'wb') as csvfile:
# 	with open('dict_5.txt', 'rb') as b2:
# 		bottles11 = file.read(b2)
# 		word_tokenizer = RegexpTokenizer(r'\w+')
# 		tokenized_words1 = word_tokenizer.tokenize(bottles11)
# 		spamwriter = csv.writer(csvfile, delimiter=',')
# 		for w in tokenized_words1:
# 			spamwriter.writerow([w])
# 			#print w


# noOfLines=0
# bott_list = []
# with open('dict1.csv', 'rb') as bb:
# 	bott = csv.reader(bb)
# 	bott_list.extend(bott)

# myNamesDict = dict() 
# for line, row in enumerate(bott_list):
# 	myNamesDict[line] = row[0]
# 	noOfLines=noOfLines+1


# bott_list = []
# with open('dict2.csv', 'rb') as bb:
# 	bott = csv.reader(bb)
# 	bott_list.extend(bott)

# for line, row in enumerate(bott_list):
# 	myNamesDict[noOfLines+line] = row[0]
# 	noOfLines=noOfLines+1


# bott_list = []
# with open('dict3.csv', 'rb') as bb:
# 	bott = csv.reader(bb)
# 	bott_list.extend(bott)

# for line, row in enumerate(bott_list):
# 	myNamesDict[noOfLines+line] = row[0]
# 	noOfLines=noOfLines+1

# bott_list = []
# with open('dict4.csv', 'rb') as bb:
# 	bott = csv.reader(bb)
# 	bott_list.extend(bott)

# for line, row in enumerate(bott_list):
# 	myNamesDict[noOfLines+line] = row[0]
# 	noOfLines=noOfLines+1


# bott_list = []
# with open('dict5.csv', 'rb') as bb:
# 	bott = csv.reader(bb)
# 	bott_list.extend(bott)

# for line, row in enumerate(bott_list):
# 	myNamesDict[noOfLines+line] = row[0]
# 	noOfLines=noOfLines+1


#print 'newspeak' in myNamesDict.values()
#print myNamesDict.values()



def viterbi_segment(text):
    probs, lasts = [1.0], [0]
    for i in range(1, len(text) + 1):
        prob_k, k = max((probs[j] * word_prob(text[j:i]), j)
                        for j in range(max(0, i - max_word_length), i))
        probs.append(prob_k)
        lasts.append(k)
    words = []
    i = len(text)
    while 0 < i:
        words.append(text[lasts[i]:i])
        i = lasts[i]
    words.reverse()
    return words #, probs[-1]

def word_prob(word): return dictionary.get(word, 0) / total
def words(text): return re.findall('[a-z]+', text.lower()) 
dictionary = dict((w, len(list(ws)))
                  for w, ws in groupby(sorted(words(open('dictionary.txt').read()))))
#dictionary=myNamesDict
max_word_length = 30#max(map(len, dictionary))
total = float(sum(dictionary.values()))




# connection = Connection('localhost', 27017)
# db = connection['gender_db']
# collection = db['collection1']

# f1 = open("filtered.txt", "w")
# f2 = open("finalfiltered.txt", "w")
# filtered=[]
# for cursor in db.collection1.find():
# 	des=cursor["description"]
# 	twt=cursor["tweet"]
# 	word_tokenizer = RegexpTokenizer(r'\w+')
# 	tokenized_words1 = word_tokenizer.tokenize(des)
# 	tokenized_words2 = word_tokenizer.tokenize(twt)
# 	filtered1 = [w for w in tokenized_words1 if not w in stopwords.words('english')]
# 	for w in filtered1:
# 		filtered.append(w)
# 		f1.write(w+" ")
# 		for ww in viterbi_segment(w.lower()):
# 			if len(ww)>1:
# 				f2.write(ww+" ")
# 	filtered2 = [w for w in tokenized_words2 if not w in stopwords.words('english')]
# 	for w in filtered2:
# 		filtered.append(w)
# 		f1.write(w+" ")
# 		for ww in viterbi_segment(w.lower()):
# 			if len(ww)>1:
# 				f2.write(ww+" ")
# 	#print filtered1,",",filtered2

# #print filtered
# f1.close()
# f2.close()



# -----------------------------------------------------------------------
# 	Following code is for taking an input file in which the data 
# 	is sorted by user name. The script runs through each row,
# 	combining all the tweets of each user and output is saved 
# 	in tweetOut.csv
# -----------------------------------------------------------------------	



noOfRows=0
filtered_des=[[[] for x in xrange(1)] for x in xrange(100000)]
tweet_words=[[[] for x in xrange(1)] for x in xrange(100000)]
des_words=[[[] for x in xrange(1)] for x in xrange(100000)]
name_words=[[[] for x in xrange(1)] for x in xrange(100000)]
word_tokenizer = RegexpTokenizer(r'\w+')
this_name=""
UniqueNamesCount=0

#with open('tweetOut.csv', 'wb') as csvfile:
with open('tweetOutLargeDB.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',')
	#with open('tweets.csv', 'rb') as csvfile:
	with open('tweetsdataLargeDB.csv', 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		next(spamreader, None)
		for row in spamreader:
	# f = open('tweetsdataLargeDB.csv')
	# for loop in range(1,1000):
	# 	f.seek(loop)                  #go to random position
	# 	f.readline()                    # discard - bound to be partial line
	# 	row = f.readline()  
			#print row[0],row[2],row[3]
			#print row[2],row[3],row[4]
			#print ', '.join(row)
			#while UniqueNamesCount!=10:
			prev_name=this_name
			this_name=row[2]#0
			#print prev_name,this_name
			if(prev_name!=this_name):
				UniqueNamesCount+=1
				print UniqueNamesCount
				des_words[noOfRows][0]=row[3]#2
				name_words[noOfRows][0]=this_name
				tokenized_words1 = word_tokenizer.tokenize(des_words[noOfRows][0])
				for w in tokenized_words1:
					for ww in viterbi_segment(w.lower()):
						if len(ww)>1:
							filtered_des[noOfRows][0].append(ww)
					#filtered_des[noOfRows][0].append(w)
				
			#print row[2]
			else:
				tokenized_words1 = word_tokenizer.tokenize(row[4])#3
				#print tokenized_words1
				for w in tokenized_words1:
					for ww in viterbi_segment(w.lower()):
						if len(ww)>1:
							tweet_words[noOfRows][0].append(ww)
						#tweet_words[noOfRows][0].append(w)
							#filtered_des[noOfRows][0].append(ww)
				#noOfRows=noOfRows+1

			if(prev_name!=this_name):
				noOfRows=noOfRows+1

			if UniqueNamesCount==100000:
				break
			

		for i in range(100000):
			spamwriter.writerow([name_words[i][0] ,filtered_des[i][0],tweet_words[i][0]])
	
	#tokenized_words1 = word_tokenizer.tokenize(tweet_words)
	#tokenized_words2 = word_tokenizer.tokenize(des_words)






