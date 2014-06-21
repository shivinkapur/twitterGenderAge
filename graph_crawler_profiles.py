from twython import Twython
import twitter
import json
import simplejson
import io
import pymongo
from flask import Flask, request
import multiprocessing
from threading import Timer
from IPython.display import IFrame
from IPython.display import display
from IPython.display import Javascript as JS 
from twitter.oauth_dance import parse_oauth_tokens
from twitter.oauth import read_token_file, write_token_file
from functools import partial
from sys import maxint
import sys
import time
from urllib2 import URLError
from httplib import BadStatusLine
import json
import twitter


CONSUMER_KEY='6eKa01PNqtG7KyIWi9l4WhzKd'
CONSUMER_SECRET='psaYDiH6ai5zahla0v7YPtqlGENOgqGCxbHHQznnq0Xlc8cXIn'
OAUTH_TOKEN='1923796555-ll7KgTrCq8NLunOlqrNklXZCDuwAel8VUORQYXM'
OAUTH_TOKEN_SECRET='N3qJSkILdGddEieddTOELQjNaIjiaceOZELh9XYmHUW3G'

def oauth_login():
	

	auth= twitter.oauth.OAuth(OAUTH_TOKEN,OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
	twitter_api=twitter.Twitter(auth=auth)

	return twitter_api


twitter_api=oauth_login()

print twitter_api



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



#--------getting friends and followers of a user -----------------


def get_friends_followers_ids(twitter_api,screen_name=None,user_id=None,friends_limit=maxint,followers_limit=maxint):
	assert (screen_name!=None) != (user_id!=None), \
	"Must have screen_name or user_id but not both"

	get_friends_ids=partial(make_twitter_request,twitter_api.friends.ids,count=5000)
	get_followers_ids=partial(make_twitter_request,twitter_api.followers.ids,count=5000)

	friends_ids,followers_ids=[],[]

	for twitter_api_func,limit,ids,label in [[get_friends_ids,friends_limit,friends_ids,"friends"],[get_followers_ids,followers_limit,followers_ids,"followers"]]:
		if limit ==0: continue

		cursor=-1
		while cursor!=0:
			if screen_name:
				response=twitter_api_func(screen_name=screen_name,cursor=cursor)
			else:
				response=twitter_api_func(user_id=user_id,cursor=cursor)

			if response is not None:
				ids+=response['ids']
				cursor=response['next_cursor']

			print >> sys.stderr, 'Fetched {0} total {1} ids for {2}'.format(len(ids),label,(user_id or screen_name))

			if len(ids) >=limit or response is None:
				break

	return friends_ids[:friends_limit],followers_ids[:followers_limit]


#--------------making robust twitter requests --------------------


def make_twitter_request(twitter_api_func,max_errors=10,*args,**kw):

	def handle_twitter_http_error(e,wait_period=2,sleep_when_rate_limited=True):

		if wait_period>3600:
			print >> sys.stderr, 'Too many retries. Quitting.'
			raise e

		if e.e.code==401:
			print >> sys.stderr,'Encountered 401 Error (Not Authorized)'
			return None

		elif e.e.code==404:
			print >> sys.stderr,'Encountered 404 Error (Not Found)'
			return None

		elif e.e.code==429:
			print >> sys.stderr,'Encountered 429 Error (Rate Limit Exceeded)'
			if sleep_when_rate_limited:
				print >> sys.stderr, "Retrying in 15 minutes...zzz..."
				sys.stderr.flush()
				time.sleep(60*15+5)
				print >> sys.stderr,'...zzz...Awake now and trying again.'
				return 2
			else:
				raise e
		
		elif e.e.code in (500,502,503,504):
			print >> sys.stderr,'Encountered %i Error. Retrying in %i seconds' % \
			(e.e.code,wait_period)
			time.sleep(wait_period)
			wait_period*=1.5
			return wait_period

		else:
			raise e


	wait_period=2
	error_count=0

	while True:
		try:
			return twitter_api_func(*args,**kw)
		except twitter.api.TwitterHTTPError,e:
			error_count=0
			wait_period=handle_twitter_http_error(e,wait_period)
			if wait_period is None:
				return
		except URLError,e:
			error_count+=1
			print >> sys.stderr, "URLError Encountered. Continuing."
			if error_count>max_errors:
				print >> sys.stderr, "Too many consecutive errors...bexiting."
				raise
		except BadStatusLine,e:
			error_count+=1
			print >> sys.stderr, "BadStatusLine Encountered. Continuing."
			if error_count>max_errors:
				print >> sys.stderr, "Too many consecutive errors...bexiting."
				raise


#--------------getting profile info ------------------------------


def get_user_profile(twitter_api,screen_names=None,user_ids=None):
	assert (screen_names!=None) != (user_ids!=None), \
	"Must have screen_names or user_ids, but not both"

	items_to_info={}
	items=screen_names or user_ids

	while len(items)>0:
		items_str=','.join([str(item) for item in items[:100]])
		items=items[100:]

		if screen_names:
			response=make_twitter_request(twitter_api.users.lookup,screen_name=items_str)
		else:
			response=make_twitter_request(twitter_api.users.lookup,user_id=items_str)

		for user_info in response:
			if screen_names:
				items_to_info[user_info['screen_name']]=user_info
			else:
				items_to_info[user_info['id']]=user_info

	return items_to_info



#----------crawling the graph ------------------------------------


def crawl_followers(twitter_api,screen_name,limit=1000000,depth=2):
	seed_id=str(twitter_api.users.show(screen_name=screen_name)['id'])
	_, next_queue=get_friends_followers_ids(twitter_api,user_id=seed_id,friends_limit=0,followers_limit=limit)

	items_to_info={}
	items=screen_name or seed_id
	if screen_name:
		response=make_twitter_request(twitter_api.users.lookup,screen_name=items)
	else:
		response=make_twitter_request(twitter_api.users.lookup,user_id=items)

	if response is not None:
		for user_info in response:
			if screen_name:
				items_to_info[user_info['screen_name']]=user_info
			else:
				items_to_info[user_info['id']]=user_info
			print user_info
			#-----------------------------------
			#with open('json.txt', 'w') as outfile:
	  		#	json.dump(data, outfile)
			#json = simplejson.loads(data)
			#print json['screen_name']
			import json
			jsondata = simplejson.dumps(user_info, indent=4, skipkeys=True, sort_keys=True)
			filestr="jsondatafile"+str(seed_id)+".json"
			allfilestr="alljsondatafile.json"
			fd = open(filestr, 'w')
			afd = open(allfilestr, 'a')
			fd.write(jsondata)
			afd.write(jsondata)
			fd.close()
			config = json.loads(open(filestr).read())
			print config['screen_name']
			print config['description']
			#-----------------------------------
	#save_to_mongo({'followers':[_id for _id in next_queue],'screen_name':config['screen_name'],'description':config['description'], 'user_profile_info': user_info}, 'followers_crawl6', '{0}-follower_ids'.format(seed_id))
	save_to_mongo({'followers':[_id for _id in next_queue],'screen_name':config['screen_name'],'description':config['description'], 'user_profile_info': user_info}, 'followers_crawl7', 'follower_ids')
	

	d=1


	while d<depth:
		d+=1
		(queue,next_queue)=(next_queue,[])
		for fid in queue:
			follower_ids=get_friends_followers_ids(twitter_api,user_id=fid,friends_limit=0,followers_limit=limit)
			#user_profiles_for_followers=get_user_profile(twitter_api,user_ids=follower_ids)
			#save_to_mongo({'followers':[_id for _id in next_queue], 'user_profile_info':user_profiles_for_followers}, 'followers_crawl', '{0}-follower_ids'.format(fid))
			items_to_info={}
			items=fid
			#if screen_name:
			#	response=make_twitter_request(twitter_api.users.lookup,screen_name=items)
			#else:
			response=make_twitter_request(twitter_api.users.lookup,user_id=items)

			#for _id in next_queue:
				#if screen_name:
				#	items_to_info[user_info['screen_name']]=user_info
				#else:
			if response is not None:
				for user_info in response:
					items_to_info[user_info['id']]=user_info
					print user_info
					#-----------------------------------
					import json
					jsondata = simplejson.dumps(user_info, indent=4, skipkeys=True, sort_keys=True)
					filestr2="jsondatafile"+str(items)+".json"
					allfilestr="alljsondatafile.json"
					fd = open(filestr2, 'w')
					afd = open(allfilestr, 'a')
					fd.write(jsondata)
					afd.write(jsondata)
					fd.close()
					config = json.loads(open(filestr2).read())
					print config['screen_name']
					print config['description']
					#-----------------------------------
			#save_to_mongo({'followers':[_id for _id in next_queue],'screen_name':config['screen_name'],'description':config['description'],'user_profile_info': user_info}, 'followers_crawl6', '{0}-follower_ids'.format(fid))
			save_to_mongo({'followers':[_id for _id in next_queue],'screen_name':config['screen_name'],'description':config['description'],'user_profile_info': user_info}, 'followers_crawl7', 'follower_ids')
			next_queue+=follower_ids



#screen_name="gaby_girrrl"
#screen_name="MakeupGeek"
#screen_name="claudiainnes1"
#screen_name="LizzyAmidon"
#screen_name="SarinShruti"
#screen_name="ninagarcia"
#screen_name="TiffanyALee2"
#screen_name="CayeTanist"
#screen_name="bianca6543"
#screen_name="LucaMolnar"
#screen_name="LadyGagasslave"
#screen_name="dolan_plays"
#screen_name="tomhanks"
screen_name="GieryMatthew"

crawl_followers(twitter_api,screen_name,depth=3,limit=100000)

#load_from_mongo('timoreilly')





