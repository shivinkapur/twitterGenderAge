from sklearn.naive_bayes import MultinomialNB
import csv
import numpy as np
from scipy import sparse

X=[[[] for xx in xrange(28)] for xx in xrange(80)]
y=[]
test1=[]
test2=[]
testN=[]
test=[[[] for xx in xrange(28)] for xx in xrange(80)]
noOfRows=0

with open('trainingDataForAge.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	next(spamreader, None)
	for row in spamreader:
		testN=[]
		for i in range(0,28):
			X[noOfRows][i]=float(row[i])
			#if noOfRows==4:
			#	test1.append(float(row[i]))
			#if noOfRows==8:
			#	test2.append(float(row[i]))
			testN.append(float(row[i]))
		test[noOfRows]=testN
		y.append(row[29])
		noOfRows+=1

print X[0]
#test[0]=test1
#test[1]=test2


clf = MultinomialNB()
clf.fit(X, y)

print clf.score(X,y)
#print clf.predict(test[0])
#print clf.predict(test[1])
for i in range(0,80):
	#print clf.predict(testN[i])
	print clf.predict(X[i])


