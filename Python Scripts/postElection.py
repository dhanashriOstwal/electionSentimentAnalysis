# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import TfidfVectorizer
import sentimentAnalysis as sA
import sys
import os
import numpy as np
from sklearn import decomposition
from gensim import corpora, models

if len(sys.argv) > 1:
    keyword = sys.argv[1]
else:
    keyword = 'data'
        
locationList = ["","Dallas","NY","SF","LA","Chicago","Washington","Atlanta"]

#Calculating the highest positive and negative comments for all locations and without any location constraint 
for location in locationList:
    resultPolarityTrump, resultSubjectivityTrump = sA.main("trump",location)
    resultPolarityHillary, resultSubjectivityHillary = sA.main("hillary",location)
    resultPolarityObama, resultSubjectivityObama = sA.main("obama",location)
    print("Trump:",resultPolarityTrump, resultSubjectivityTrump)
    print("Hillary:",resultPolarityHillary, resultSubjectivityHillary)
    print("Obama:",resultPolarityObama, resultSubjectivityObama)
 
    if resultPolarityObama > resultPolarityTrump and resultPolarityObama > resultPolarityHillary:
        highestPol = "Obama"#resultPolarityObama
    elif resultPolarityTrump >  resultPolarityObama and resultPolarityTrump > resultPolarityHillary:
        highestPol = "Trump"#resultPolarityTrump
    else:
        highestPol = "Hillary"#resultPolarityHillary
    
    if resultSubjectivityObama > resultSubjectivityTrump and resultSubjectivityObama > resultSubjectivityHillary:
        highestSub = "Obama"#resultSubjectivityObama
    elif resultSubjectivityTrump >  resultSubjectivityObama and resultSubjectivityTrump > resultSubjectivityHillary:
        highestSub = "Trump"#resultSubjectivityTrump
    else:
        highestSub = "Hillary"#resultSubjectivityHillary
    
    print("{} has highest positive comments.".format(highestPol))
    print("{} has highest negative comments.".format(highestSub))
    
    #JSON Dataset that has tweets    
    corpus=['tweet_stream_hillary.json','tweet_stream_obama.json','tweet_stream_trump.json']
    
    #Topic Analysis, LDA 
    fname=[]
    corpus=[]
    docs=[]
    corpus_root='Corpus Data'
    for filename in os.listdir(corpus_root):
        file = open(os.path.join(corpus_root, filename), "r")
        doc = file.read()
        words=doc.split()
        file.close()
        fname.append(filename)
        corpus.append(doc)
        docs.append(words)
    
    vectorizer = TfidfVectorizer(stop_words='english', min_df=2)
    dtm = vectorizer.fit_transform(corpus)
    vocab = vectorizer.get_feature_names()
    
    num_topics=3
    num_top_words=10
    clf = decomposition.NMF(n_components=num_topics, random_state=1)
    doctopic = clf.fit_transform(dtm)
    print num_topics, clf.reconstruction_err_
    
    topic_words = []
    for topic in clf.components_:
        word_idx = np.argsort(topic)[::-1][0:num_top_words]
        topic_words.append([vocab[i] for i in word_idx])
        
    for t in range(len(topic_words)):
        print "Topic {}: {}".format(t, ' '.join(topic_words[t][:15]))
        
    dic = corpora.Dictionary(docs)
    corp = [dic.doc2bow(text) for text in docs]
    tfidf = models.TfidfModel(corp)
    corpus_tfidf = tfidf[corp]
    model = models.ldamodel.LdaModel(corpus_tfidf, num_topics=num_topics, id2word=dic, update_every=1, passes=100)
    print("LDA model")
    topics_found = model.print_topics(20)
    counter = 1
    for t in topics_found:
        print("Topic #{} {}".format(counter, t))
        counter += 1
    topics_found2 = model.print_topics(50)
    counter2 = 1
    for t in topics_found2:
        print("Topic #{} {}".format(counter2, t))
        counter2 += 1
    