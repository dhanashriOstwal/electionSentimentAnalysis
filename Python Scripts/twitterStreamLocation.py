# -*- coding: utf-8 -*-

from twython import TwythonStreamer
import sys
import json
import os
import random
from datetime import datetime
tweets = []
startTime = datetime.now()
class MyStreamer(TwythonStreamer):
    #'''our own subclass of TwythonStremer'''

# overriding
    def on_success(self, data):
        
        if  'text' in data:
            if data['lang'] == 'en': #and data['user']['location'] != None:
                if keyword in data['text'].encode('utf-8'):
                    print data['text'].encode('utf-8')        
                    details = []
                    content = data['text'].split(':',1)
                    created_at = data['user']['created_at'].split()
                    date = created_at[1] + created_at[2] + created_at[-1]
                    if content[0].startswith('RT '):
                        line = content[1].split('http')
                    else:
                        line = content[0].split('http')
                        details.append(date)
                        details.append(line[0])
                        tweets.append(details)
                        print 'received tweet #', len(tweets), data['text'][:100].encode('utf-8')
    #                    t = random.random()
#                    print("Sleeping for:",t)
#                    time.sleep(t)
    
        if len(tweets) >= 5:
           self.store_json()
           self.disconnect()
		 

    # overriding
    def on_error(self, status_code, data):
        print status_code, data
        #self.disconnect()

    def store_json(self):
        loc = "SF"
        if os.path.isfile('tweet_stream_{}_{}.json'.format(keyword,loc)):
            with open('tweet_stream_{}_{}.json'.format(keyword,loc), 'r') as f:    
                lines = json.load(f)
                #lines = f.readlines()
                if len(lines) > 0:
                    lines += tweets
        else:
            lines = tweets
        with open('tweet_stream_{}_{}.json'.format(keyword,loc), 'w') as f:
            json.dump(lines, f, indent=4)


if __name__ == '__main__':

    with open('priyanka_twitter_credentials.json', 'r') as f:
        credentials = json.load(f)

    # create your own app to get consumer key and secret
    CONSUMER_KEY = credentials['CONSUMER_KEY']
    CONSUMER_SECRET = credentials['CONSUMER_SECRET']
    ACCESS_TOKEN = credentials['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = credentials['ACCESS_TOKEN_SECRET']

    try:
        stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
        if len(sys.argv) > 1:
            keyword = sys.argv[1]
        else:
            keyword = 'trump'
    
        stream.statuses.filter(locations="-122.75,36.8,-121.75,37.8")
    except:
        stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
        if len(sys.argv) > 1:
            keyword = sys.argv[1]
            #secondkeyword = sys.argv[2]
        else:
            keyword = 'trump'
            #secondkeyword = 'dallas'
            
    
        stream.statuses.filter(locations="-122.75,36.8,-121.75,37.8")
        #Dallas = 32.776664,-96.796988
        #New York = -74,40,-73,41
        #San Francisco, CA = -122.75,36.8,-121.75,37.8
        #Los Angeles, CA = 34.052234, -118.243685
        #Chicago, IL = 41.878114,-87.629798
        #Washington DC = 38.907192, -77.036871
        #Atlanta GA = 33.748995, -84.387982
