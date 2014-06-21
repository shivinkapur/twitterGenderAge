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

class ModifiedWPTokenizer( nltk.tokenize.RegexpTokenizer):
    def __init__(self):
        nltk.tokenize.RegexpTokenizer.__init__(self, r'\w+|[^\w\s]|\s+')

def save_to_mongo(data,mongo_db,mongo_db_coll,**mongo_conn_kw):
	client1=pymongo.MongoClient(**mongo_conn_kw)
	db1=client1[mongo_db]
	coll1=db1[mongo_db_coll]
	return coll1.insert(data)


# Sentence Classification Class
# Based on O'Reilly, pp234 but also uses whitespace information
class SentenceTokenizer():

    # extract punctuation features from word list for position i
    # Features are: this word; previous word (lower case);
    # is the next word capitalized?; previous word only one char long?
    def punct_features(self, tokens, i):
        return {'next-word-capitalized': (i<len(tokens)-1) and tokens[i+1][0].isupper(),
                'prevword': tokens[i-1].lower(),
                'punct': tokens[i],
                'prev-word-is-one-char': len(tokens[i-1]) == 1}

    # Same as punct_features, but works with a list of
    # (word,bool) tuples for the tokesn. Word is used as above, but the bool
    # flag (whitespace separator?) is ignored
    # This allows the same features to be extracted from tuples instead of
    # words
    def punct_features2(self,tokens, i):
        return {'next-word-capitalized': (i<len(tokens)-1) and tokens[i+1][0][0].isupper(),
                'prevword': tokens[i-1][0].lower(),
                'punct': tokens[i][0],
                'prev-word-is-one-char': len(tokens[i-1][0]) == 1}

    # The constructor builds a classifier using treebank training data
    # Naive Bayes is used for fast training
    # The entire dataset is used for training
    def __init__(self):
        self.tokenizer = ModifiedWPTokenizer()

        training_sents = nltk.corpus.treebank_raw.sents()
        tokens = []
        boundaries = set()
        offset = 0
        for sent in nltk.corpus.treebank_raw.sents():
            tokens.extend(sent)
            offset += len(sent)
            boundaries.add(offset-1)

        # Create training features
        featuresets = [(self.punct_features(tokens,i), (i in boundaries))
                       for i in range(1, len(tokens)-1)
                       if tokens[i] in '.?!']

        train_set = featuresets
        self.classifier = nltk.NaiveBayesClassifier.train(train_set)

    # Use the classifier to segment word tokens into sentences
    # words is a list of (word,bool) tuples
    def classify_segment_sentences(self,words):
        start = 0
        sents = []
        for i, word in enumerate(words):
            if word[0] in '.?!' and self.classifier.classify(self.punct_features2(words,i)) == True:
                sents.append(words[start:i+1])
                start = i+1
        if start < len(words):
            sents.append(words[start:])
        return sents

    # Segment text into sentences and words
    # returns a list of sentences, each sentence is a list of words
    # punctuation chars are classed as word tokens (except abbreviations)
    def segment_text(self,full_text):

        # Split (tokenize) text into words. Count whitespace as
        # words. Keeping this information allows us to distinguish between
        # abbreviations and sentence terminators
        text_words_sp = self.tokenizer.tokenize(full_text)

        # Take tokenized words+spaces and create tuples of (token,bool)
        # with the bool entry indicating if the token is whitespace.
        # All whitespace is collapsed down to single sp chars
        word_tuples = []
        i =0
        while (i<len(text_words_sp)):
            word = text_words_sp[i]
            if (word.isspace()):
                word = " "    # convert all whitespace to a single sp char
            if (i == len(text_words_sp)-1):
                word_tuples.append( (word,False) )
            else:
                word2 = text_words_sp[i+1]
                if (word2.isspace()):
                    i = i +1
                    word_tuples.append( (word,True) )
                else:
                    word_tuples.append( (word,False) )
            i = i +1

        # Create list of sentence using the classifier
        sentences = []
        for sent in self.classify_segment_sentences(word_tuples):
            # sent holds the next sentence list of tokens
            # this is actually a list of (token,bool) tuples as above
            sentence = []
            i = 0
            tok = ""
            # loop over each token tuple, using separator boolean
            # to collapse abbreviations into single word tokens
            for i,tup in enumerate(sent):
                if (tup[0][0] in string.punctuation and not tup[0][0] in '.?!'):
                    # punctuation that should be kept as a single token
                    if (len(tok) > 0):
                        sentence.append(tok)
                        tok=""
                    sentence.append(tup[0])
                elif (tup[1]):
                    # space character - finish a word token
                    sentence.append( tok+tup[0] )
                    tok = ""
                elif (i == len(sent)-2):
                    # penultimate end of the sentence - break off the punctuation
                    sentence.append( tok+tup[0] )
                    tok = ""           
                else:            
                    # no space => accumulate a token in tok
                    tok = tok + tup[0]
            # Add this token to the current sentence
            if len(tok) > 0:
                sentence.append(tok)
            # The sentence has been procssed => save it
            sentences.append(sentence)

        # return the resulting list of sentences
        return sentences


connection = Connection('localhost', 27017)
db = connection['followers_jsonfiles1']
collection = db['follower_ids']

# names=[]

# with open('names.csv', 'rb') as csvfile:
# 	spamreader = csv.reader(csvfile, delimiter=',')
# 	for row in spamreader:
# 		#print ', '.join(row)
# 		names.append(row[1])

bottle_list = []
with open('names.csv', 'rb') as b:
	bottles = csv.reader(b)
	bottle_list.extend(bottles)


myNamesDict = dict() 
for line, row in enumerate(bottle_list):
	#print line,',',row[1]
	myNamesDict[line] = row[1]


print 'Morgan' in myNamesDict.values()


sent_tokenizer=nltk.data.load('nltk:tokenizers/punkt/english.pickle')
validLetters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVYXYZ"
invalid=" "


def words(stringIterable):
    #upcast the argument to an iterator, if it's an iterator already, it stays the same
	lineStream = iter(stringIterable)
	for line in lineStream: #enumerate the lines
		for word in line.split(): #further break them down
			yield word



with open('out.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',')
	spamwriter.writerow(["user_id","name","screen_name","description","tweet","gender"])
	for cursor in db.follower_ids.find():
		tmp_name=cursor["name"]
		sents = sent_tokenizer.tokenize(tmp_name)
		lines_text = sents
		full_text = ""
		for s in lines_text:
		    full_text = full_text + " " + s
		myTokenizer = SentenceTokenizer()
		sentences = myTokenizer.segment_text(full_text)
		for sentence1 in sentences:
			tmpfirstName=''.join([char for char in sentence1[0] if char in validLetters])
			firstChar=tmpfirstName[:1].upper()
			firstName=firstChar+tmpfirstName[1:]
			#print firstName
			if(firstName in myNamesDict.values()):
				print firstName
				theIndex=[k for k, v in myNamesDict.iteritems() if v == firstName][0]
				#print theIndex
				save_to_mongo({'user_id':cursor["user_id"], 'name':cursor["name"],'screen_name':cursor["screen_name"],'description':cursor["description"],'tweet': cursor["tweet"], 'gender':bottle_list[theIndex][2]}, 'gender_db', 'collection1')
				spamwriter.writerow([cursor["user_id"], cursor["name"], cursor["screen_name"],cursor["description"],cursor["tweet"],bottle_list[theIndex][2]])
				break










