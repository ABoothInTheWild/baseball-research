# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 18:21:39 2017

@author: Alexander
"""

# Twitter Bot

# Imports
# prepare for Python version 3x features and functions
from __future__ import division, print_function
import time
import tweepy
import sys
import requests
import json
import random
from abc import ABCMeta, abstractmethod
from datetime import datetime

class TwitterBot(object):
    
    __metaclass__ = ABCMeta
    
    #Get time. Don't post in the middle of the night
    timeStart = datetime.strptime('7:00AM', "%I:%M%p").time()
    timeEnd = datetime.strptime('11:00PM', "%I:%M%p").time()
    
    #inits
    name = ""
    retweetTags = []
    followTags = []
    
    def __init__(self, ckey, csec, akey, asec, fb_url):
        self.fb_url = fb_url
        
        auth = tweepy.OAuthHandler(ckey, csec)
        auth.set_access_token(akey, asec)
        self.api = tweepy.API(auth)
        
    def postRetweet(self, tag, minRetweetCount=100):
        try:
            c = tweepy.Cursor(self.api.search, q=tag)
            for tweet in c.items():
                timeNow = datetime.now().time()
                if self.isNowInTimePeriod(self.timeStart, self.timeEnd, timeNow) and tweet.retweet_count > minRetweetCount:
                    if self.check_tweet(tweet):
                        self.api.retweet(tweet.id)
                        db_tweet = {"id": tweet.id}
                        requests.post(self.fb_url, json.dumps(db_tweet))
                        break
        # Exceptions
        except KeyboardInterrupt:
            sys.exit("KeyboardInterrupt")
        except Exception as e:
            print(e)
            pass    

    def check_tweet(self, tweet):
        try:
            r = requests.get(self.fb_url)
            r = r.json()
            for i in r:
                if tweet.id == r[i]["id"]:
                    return False
       # Exceptions 
        except KeyboardInterrupt:
            sys.exit("KeyboardInterrupt")
        except Exception as e:
            print(e)
            pass
        finally:
            return True  
    
    @staticmethod
    def isNowInTimePeriod(startTime, endTime, nowTime):
        rtnBool = False
        if startTime < endTime:
            rtnBool = nowTime >= startTime and nowTime <= endTime
        else: #Over midnight
            rtnBool = nowTime >= startTime or nowTime <= endTime
        
        return rtnBool
    
    @staticmethod
    def sleepyBaby():
        time1 = random.randint(1, 4)
        if time1 == 1:
            time.sleep(2100) #Tweet every 35 minutes
        elif time1 == 2:
            time.sleep(3900) #Tweet every 65 minutes
        elif time1 == 3:
            time.sleep(2760) #Tweet every 46 minutes
        else:
            time.sleep(1410) #Tweet every 23.5 minutes
     
    @abstractmethod
    def getStatus(self):
        """"Return a string to update as the status"""
        pass
    
    def postStatus(self, status):
        rtnBool = True
        timeNow = datetime.now().time()
        if self.isNowInTimePeriod(self.timeStart, self.timeEnd, timeNow):
            if status and not status is None:
                try:
                    self.api.update_status(status)
                # Additions below
                except KeyboardInterrupt:
                    sys.exit("KeyboardInterrupt")
                except Exception as e:
                    print(e)
                    rtnBool = False
        return rtnBool
    
    def doAction(self):
        potentialActions = ["retweet", "status", "status", "nothing", "nothing"]
        action = random.choice(potentialActions)
        
        if action == "retweet":
            self.postRetweet(random.choice(self.retweetTags))
        elif action == "status":
            self.postStatus(self.getStatus())
        else:
            pass
        
        self.sleepyBaby()