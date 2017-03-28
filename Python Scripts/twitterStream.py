
from twython import TwythonStreamer
import sys
import json
import time
import random
import os
from datetime import datetime
from pprint import pprint
tweets = []
path = "."
startTime = datetime.now()
class MyStreamer(TwythonStreamer):
    #'''our own subclass of TwythonStremer'''

# overriding
    def on_success(self, data):
        if  'text' in data:
            if data['lang'] == 'en':
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
    
        if len(tweets) >= 500:
           self.store_json()
           self.disconnect()
		 

    # overriding
    def on_error(self, status_code, data):
        print status_code, data
        #self.disconnect()
        #, startTime.strftime("%Y-%m-%d %H-%M-%S")
    def store_json(self):
        if os.path.isfile('tweet_stream_{}.json'.format(keyword)):
            print("I am here!!!!")                  
            with open('tweet_stream_{}.json'.format(keyword), 'r') as f:    
                lines = json.load(f)
                #lines = f.readlines()
                if len(lines) > 0:
                    lines += tweets
        else:
            lines = tweets
        #pprint(lines)       
        with open('tweet_stream_{}.json'.format(keyword), 'w') as f:
            json.dump(lines, f, indent=4)
            #f.write('\n')
#        with open('tweet_stream_{}.json'.format(keyword), 'r') as f:    
#            lines = json.load(f)
        #pprint(lines)


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
            keyword = 'data'
    
        stream.statuses.filter(track=keyword)
    except:
        stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
        if len(sys.argv) > 1:
            keyword = sys.argv[1]
        else:
            keyword = 'data'
    
        stream.statuses.filter(track=keyword)
	
