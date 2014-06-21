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
import sys
import re
from itertools import groupby
#from stemming.porter2 import stem
from nltk.stem.wordnet import WordNetLemmatizer

lmtzr = WordNetLemmatizer()

noOfConversation=0
noOfFamily=0
noOfTime=0	
noOfWork=0
noOfGames=0
noOfInternet=0
noOfLocation=0
noOfFun=0
noOfFood=0
noOfClothes=0
noOfHealth=0
noOfBooks_Movies=0
noOfReligion=0
noOfRomance=0
noOfSwearing=0
noOfPolitics=0
noOfMusic=0
noOfSchool=0
noOfFeeling=0
noOfBusiness=0
noOfAdjective=0
noOfFollow=0
noOfPositive=0
noOfnegative=0
noOfArticle=0
noOfPersonal_pronoun=0
noOfConjunction=0
noOfPreposition=0
noOfAux_Verbs=0



Conversation=[]
Family=[]
Time=[]
Work=[]
Games=[]
Internet=[]
Location=[]
Fun=[]
Food=[]
Clothes=[]
Health=[]
Books_Movies=[]
Religion=[]
Romance=[]
Swearing=[]
Politics=[]
Music=[]
School=[]
Feeling=[]
Business=[]
Adjective=[]
Follow=[]
Positive=[]
negative=[]
Article=[]
Personal_pronoun=[]
Conjunction=[]
Preposition=[]
Aux_Verbs=[]


spamreader=csv.reader(open('Topics.csv', 'rU'), delimiter=',', dialect=csv.excel_tab)
for row in spamreader:
	if(row[0]!=''):
		Conversation.append(row[0])
	#print Conversation
	if(row[1]!=''):
		Family.append(lmtzr.lemmatize(row[1].lower()))
	if(row[2]!=''):
		Time.append(lmtzr.lemmatize(row[2].lower()))
	if(row[3]!=''):
		Work.append(lmtzr.lemmatize(row[3].lower()))
	if(row[4]!=''):
		Games.append(lmtzr.lemmatize(row[4].lower()))
	if(row[5]!=''):
		Internet.append(lmtzr.lemmatize(row[5].lower()))
	if(row[6]!=''):
		Location.append(lmtzr.lemmatize(row[6].lower()))
	if(row[7]!=''):
		Fun.append(lmtzr.lemmatize(row[7].lower()))
	if(row[8]!=''):
		Food.append(lmtzr.lemmatize(row[8].lower()))
	if(row[9]!=''):
		Clothes.append(lmtzr.lemmatize(row[9].lower()))
	if(row[10]!=''):
		Health.append(lmtzr.lemmatize(row[10].lower()))
	if(row[11]!=''):
		Books_Movies.append(lmtzr.lemmatize(row[11].lower()))
	if(row[12]!=''):
		Religion.append(lmtzr.lemmatize(row[12].lower()))
	if(row[13]!=''):
		Romance.append(lmtzr.lemmatize(row[13].lower()))
	if(row[14]!=''):
		Swearing.append(lmtzr.lemmatize(row[14].lower()))
	if(row[15]!=''):
		Politics.append(lmtzr.lemmatize(row[15].lower()))
	if(row[16]!=''):
		Music.append(lmtzr.lemmatize(row[16].lower()))
	if(row[17]!=''):
		School.append(lmtzr.lemmatize(row[17].lower()))
	if(row[18]!=''):
		Feeling.append(lmtzr.lemmatize(row[18].lower()))
	if(row[19]!=''):
		Business.append(lmtzr.lemmatize(row[19].lower()))
	if(row[20]!=''):
		Adjective.append(lmtzr.lemmatize(row[20].lower()))
	if(row[21]!=''):
		Follow.append(lmtzr.lemmatize(row[21].lower()))
	if(row[22]!=''):
		Positive.append(lmtzr.lemmatize(row[22].lower()))
	if(row[23]!=''):
		negative.append(lmtzr.lemmatize(row[23].lower()))
	if(row[24]!=''):
		Article.append(lmtzr.lemmatize(row[24].lower()))
	if(row[25]!=''):
		Personal_pronoun.append(lmtzr.lemmatize(row[25].lower()))
	if(row[26]!=''):
		Aux_Verbs.append(lmtzr.lemmatize(row[26].lower()))
	if(row[27]!=''):
		Conjunction.append(lmtzr.lemmatize(row[27].lower()))
	if(row[28]!=''):
		Preposition.append(lmtzr.lemmatize(row[28].lower()))
	
#print Preposition

allWordsofTweetAndDescription=[]
allUniqueWords=[]
UniqueWordCount=0
word_tokenizer = RegexpTokenizer(r'\w+')
noOfHitWords=0
age=''

with open('testDataForAgeLargeDB.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',')
	spamwriter.writerow(["Conversation","Family","Time","Work","Games","Internet","Location","Fun","Food","Clothes","Health","Books_Movies","Religion","Romance","Swearing","Politics","Music","School","Feeling","Business","Adjective","Follow","Positive","negative","Article","Personal_pronoun","Auxiliary_Verb","Conjunction","Preposition","Male_female","Age_Class"])

	spamreader=csv.reader(open('tweetOutLargeDBModified.csv', 'rU'), delimiter=',', dialect=csv.excel_tab)
	for row in spamreader:
		for row in spamreader:
			allWordsofTweetAndDescription=[]
			allUniqueWords=[]
			noOfHitWords=0
			UniqueWordCount=0
			noOfConversation=0
			noOfFamily=0
			noOfTime=0	
			noOfWork=0
			noOfGames=0
			noOfInternet=0
			noOfLocation=0
			noOfFun=0
			noOfFood=0
			noOfClothes=0
			noOfHealth=0
			noOfBooks_Movies=0
			noOfReligion=0
			noOfRomance=0
			noOfSwearing=0
			noOfPolitics=0
			noOfMusic=0
			noOfSchool=0
			noOfFeeling=0
			noOfBusiness=0
			noOfAdjective=0
			noOfFollow=0
			noOfPositive=0
			noOfnegative=0
			noOfArticle=0
			noOfPersonal_pronoun=0
			noOfConjunction=0
			noOfPreposition=0
			noOfAux_Verbs=0

			tokenized_words1 = word_tokenizer.tokenize(row[1])
			for word in tokenized_words1:
				allWordsofTweetAndDescription.append(word.lower())
			tokenized_words1 = word_tokenizer.tokenize(row[2])
			for word in tokenized_words1:
				allWordsofTweetAndDescription.append(word.lower())
			for word in allWordsofTweetAndDescription:
				#print word
				stemword=lmtzr.lemmatize(word)
				if stemword not in allUniqueWords:
					allUniqueWords.append(stemword)
					UniqueWordCount+=1
				#print UniqueWordCount
				if stemword in Conversation:
					noOfConversation+=1
					noOfHitWords+=1
				if stemword in Family:
					noOfFamily+=1
					noOfHitWords+=1
				if stemword in Time:
					noOfTime+=1
					noOfHitWords+=1
				if stemword in Work:
					noOfWork+=1
					noOfHitWords+=1
				if stemword in Games:
					noOfGames+=1
					noOfHitWords+=1
				if stemword in Internet:
					noOfInternet+=1
					noOfHitWords+=1
				if stemword in Location:
					noOfLocation+=1
					noOfHitWords+=1
				if stemword in Fun:
					noOfFun+=1
					noOfHitWords+=1
				if stemword in Food:
					noOfFood+=1
					noOfHitWords+=1
				if stemword in Clothes:
					noOfClothes+=1
					noOfHitWords+=1
				if stemword in Health:
					noOfHealth+=1
					noOfHitWords+=1
				if stemword in Books_Movies:
					noOfBooks_Movies+=1
					noOfHitWords+=1
				if stemword in Religion:
					noOfReligion+=1
					noOfHitWords+=1
				if stemword in Romance:
					noOfRomance+=1
					noOfHitWords+=1
				if stemword in Swearing:
					noOfSwearing+=1
					noOfHitWords+=1
				if stemword in Politics:
					noOfPolitics+=1
					noOfHitWords+=1
				if stemword in Music:
					noOfMusic+=1
					noOfHitWords+=1
				if stemword in School:
					noOfSchool+=1
					noOfHitWords+=1
				if stemword in Feeling:
					noOfSchool+=1
					noOfHitWords+=1
				if stemword in Business:
					noOfBusiness+=1
					noOfHitWords+=1
				if stemword in Adjective:
					noOfAdjective+=1
					noOfHitWords+=1
				if stemword in Follow:
					noOfFollow+=1
					noOfHitWords+=1
				if stemword in Positive:
					noOfPositive+=1
					noOfHitWords+=1
				if stemword in negative:
					noOfnegative+=1
					noOfHitWords+=1
				if stemword in Article:
					noOfArticle+=1
					noOfHitWords+=1
				if stemword in Personal_pronoun:
					noOfPersonal_pronoun+=1
					noOfHitWords+=1
				if stemword in Aux_Verbs:
					noOfAux_Verbs+=1
					noOfHitWords+=1
				if stemword in Conjunction:
					noOfConjunction+=1
					noOfHitWords+=1
				if stemword in Preposition:
					noOfPreposition+=1
					noOfHitWords+=1
			
			#print row[1]
			#print str(age)
			print noOfHitWords
			if(noOfHitWords>=50):
				spamwriter.writerow([float(noOfConversation)/float(noOfHitWords),float(noOfFamily)/float(noOfHitWords),float(noOfTime)/float(noOfHitWords),float(noOfWork)/float(noOfHitWords),float(noOfGames)/float(noOfHitWords),float(noOfInternet)/float(noOfHitWords),float(noOfLocation)/float(noOfHitWords),float(noOfFun)/float(noOfHitWords),float(noOfFood)/float(noOfHitWords),float(noOfClothes)/float(noOfHitWords),float(noOfHealth)/float(noOfHitWords),float(noOfBooks_Movies)/float(noOfHitWords),float(noOfReligion)/float(noOfHitWords),float(noOfRomance)/float(noOfHitWords),float(noOfSwearing)/float(noOfHitWords),float(noOfPolitics)/float(noOfHitWords),float(noOfMusic)/float(noOfHitWords),float(noOfSchool)/float(noOfHitWords),float(noOfFeeling)/float(noOfHitWords),float(noOfBusiness)/float(noOfHitWords),float(noOfAdjective)/float(noOfHitWords),float(noOfFollow)/float(noOfHitWords),float(noOfPositive)/float(noOfHitWords),float(noOfnegative)/float(noOfHitWords),float(noOfArticle)/float(noOfHitWords),float(noOfPersonal_pronoun)/float(noOfHitWords),float(noOfAux_Verbs)/float(noOfHitWords),float(noOfConjunction)/float(noOfHitWords),float(noOfPreposition)/float(noOfHitWords)])







