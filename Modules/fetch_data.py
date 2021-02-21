import tweepy
import pandas as pd
import csv
import re 
import string
import preprocessor as p
import pandas as pd
from Modules.vader_sentiment import vaderSentiment
from flask import Flask
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
#ssl._create_default_https_context = ssl._create_unverified_context
# Oauth keys
consumer_key = "1ho3OMBb8ydSNSRnE2Nw0GLxy"
consumer_secret = "6gFZjLUuei6E3A6km0UBMLAhnpLcVRa9vB23irskEQs3FRoHhF"
access_token = "940254439746752512-Cb19BHMq4qIkFBLCpcqTUlP2Guf2XMQ"
access_token_secret = "6vUcHUjpEKdciQiHwsLPAnxylz74XihgnQpnPrX3EYmdJ"
# Authentication with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
positiveFeed=[]
negativeFeed=[]
neutralFeed=[]
class fetchData:
    def createCsv(self,searchElement):
        csvFile = open('file-name.csv', 'w')
        csvWriter = csv.writer(csvFile)
        search_words = searchElement      #enter your words
        new_search = search_words + " -filter:retweets"
        for tweet in tweepy.Cursor(api.search,q=new_search,count=10,lang="en",since_id=0).items(40):
            csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8'),tweet.user.screen_name.encode('utf-8'), tweet.user.location.encode('utf-8')])
        csvFile = open('file-name.csv', 'w')
        csvWriter = csv.writer(csvFile)
    def operationHandling(self):
        df=pd.read_csv('file-name.csv',header=None)
        df.to_csv("file-name.csv", header=["date", "tweet", "user","place"], index=False)
        df = pd.read_csv("file-name.csv", usecols = ['tweet'])
        for i in range(0,40):
            obj=vaderSentiment()
            sentence=df['tweet'][i]
            result=obj.sentiment_analyzer_scores(sentence)
            if result['compound']>=0.05:
                positiveFeed.append(result['pos'])
            elif result['compound']<=-0.05:
                negativeFeed.append(result['neg'])
            else:
                neutralFeed.append(result['neu'])
        countPositive=((len(positiveFeed))/(len(positiveFeed)+len(negativeFeed)+len(neutralFeed)))*100
        countNegative=((len(negativeFeed))/(len(positiveFeed)+len(negativeFeed)+len(neutralFeed)))*100
        countNeutral=((len(neutralFeed))/(len(positiveFeed)+len(negativeFeed)+len(neutralFeed)))*100
        resultantDict={}
        resultantDict['Positive']=countPositive
        resultantDict['Negative']=countNegative
        resultantDict['Neutral']=countNeutral
        Keymax=max(resultantDict,key=resultantDict.get)
        return Keymax
    def pie_chart(self):
        df=pd.read_csv('file-name.csv',header=None)
        df.to_csv("file-name.csv", header=["date", "tweet", "user","place"], index=False)
        df = pd.read_csv("file-name.csv", usecols = ['tweet'])
        for i in range(0,40):
            obj=vaderSentiment()
            sentence=df['tweet'][i]
            result=obj.sentiment_analyzer_scores(sentence)
            if result['compound']>=0.05:
                positiveFeed.append(result['pos'])
            elif result['compound']<=-0.05:
                negativeFeed.append(result['neg'])
            else:
                neutralFeed.append(result['neu'])
        countPositive=((len(positiveFeed))/(len(positiveFeed)+len(negativeFeed)+len(neutralFeed)))*100
        countNegative=((len(negativeFeed))/(len(positiveFeed)+len(negativeFeed)+len(neutralFeed)))*100
        countNeutral=((len(neutralFeed))/(len(positiveFeed)+len(negativeFeed)+len(neutralFeed)))*100
        resultantDict={}
        resultantDict['Positive']=countPositive
        resultantDict['Negative']=countNegative
        resultantDict['Neutral']=countNeutral
        countPositive=((len(positiveFeed))/(len(positiveFeed)+len(negativeFeed)+len(neutralFeed)))*100
        countNegative=((len(negativeFeed))/(len(positiveFeed)+len(negativeFeed)+len(neutralFeed)))*100
        countNeutral=((len(neutralFeed))/(len(positiveFeed)+len(negativeFeed)+len(neutralFeed)))*100
        data={'Task':'Pie chart','Positive':countPositive,'Negative':countNegative,'Neutral':countNeutral}
        return data
        


