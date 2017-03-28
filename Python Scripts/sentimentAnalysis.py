# -*- coding: utf-8 -*-

from __future__ import print_function
from nltk.stem.porter import PorterStemmer
from textblob import TextBlob
from wordcloud import WordCloud
import nltk
import json
import matplotlib.pyplot as plt
import os
import string
from textblob.sentiments import NaiveBayesAnalyzer

ps = PorterStemmer()
tweetDict = {}

def main(name,location):
    directory = "Corpus Data"
    count = 0
    
    if location == "":
        filename = 'tweet_stream_{}.json'.format(name)
        fileCorpus = 'tweet_stream_{}.txt'.format(name)
    else:
        filename = 'tweet_stream_{}_{}.json'.format(name,location)
        fileCorpus = 'tweet_stream_{}_{}.txt'.format(name,location)
    print(filename)

    #Read dataset containing tweets
    with open(filename) as json_file:
        tweets = json.load(json_file) 
    
    with open(directory + '/' + fileCorpus, 'w') as f:
        for tweet in tweets:
            #Removal of special characters
            encoded_tweet=tweet[1].encode('utf-8')
            unicode_text = encoded_tweet.decode('unicode_escape').encode('ascii','ignore')
            punct=string.punctuation
            table_p=string.maketrans(punct,len(punct)*" ")
            text=unicode_text.translate(table_p)
            tweetDict[count] = [tweet[0],text]
            if not os.path.exists(directory):
                os.makedirs(directory)
            f.write(tweet[1].encode('utf-8'))
            f.write('\n')
        
            count += 1
        
    sub = []
    pol = []
    cnt = 1
    for key,value in tweetDict.iteritems():
        #if value[0].strip() == dateVal.strip():
        #Call to removal_stop_words
        text_without_stopwords = remove_stop_words(value[1])  
        #TextBlob using NaiveBayes              
        text = TextBlob(text_without_stopwords,analyzer = NaiveBayesAnalyzer())
        pol.append(text.sentiment.p_pos)
        sub.append(text.sentiment.p_neg)
        print(cnt)
        cnt += 1
        #TextBlob without NaiveBayes
#       text = TextBlob(value[1])
#       pol.append(text.sentiment.polarity)
#       sub.append(text.sentiment.subjectivity)
    
    word_cloud()
    resultPolarity = sum(pol)/len(pol)
    resultSubjectivity = sum(sub)/len(sub)
    print(resultPolarity,resultSubjectivity)
    return resultPolarity,resultSubjectivity

#Removal of stopwords
def remove_stop_words(text):
    keyword = ' '
    stop = set(nltk.corpus.stopwords.words('english'))
    for i in text.lower().split():
        if i not in stop:
            #Stemming
            stemmedVar = ps.stem(i)
            keyword += ' ' + stemmedVar
    return keyword

#Word Cloud
def word_cloud():
    keywords_list = ''
    for key,value in tweetDict.iteritems():
        keyword = remove_stop_words(value[1]) 
        keywords_list += ' ' + keyword
    wordcloud = WordCloud().generate(keywords_list)
    plt.imshow(wordcloud)
    plt.axis("off")
    wordcloud = WordCloud(max_font_size=40).generate(keywords_list)
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

    
