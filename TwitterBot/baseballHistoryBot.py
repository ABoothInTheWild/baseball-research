# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 20:03:53 2017

@author: Alexander Booth
"""

#Baseball Trivia Twitter Bot
#Data Sourced from Lahman's Baseball Database

# Imports
# prepare for Python version 3x features and functions
from __future__ import division, print_function
import time
import pandas as pd
import tweepy
import sys
import requests
import json
import random
from datetime import datetime

fb_url = "https://baseball-trivya.firebaseio.com/tweets.json"

#enter the corresponding information from your Twitter application:
CONSUMER_KEY = '2gBiPBoAovxg7PDNeX6jXTKLX'
CONSUMER_SECRET = '3YT9LXW7StJ7OoDMHgw8kFVzXZEQK2H2ilnFrseXsUCDLcXSaJ'
ACCESS_KEY = '931373265653784576-4fgDnw0hbNJ1BAV3egNrh07URyPB6FU'
ACCESS_SECRET = 'oM1EGxPDqtWiY8Yrvd7j72dMownO7YGYcaqDDhQFREQzh'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)



def check_tweet(tweet):
    try:
        r = requests.get(fb_url)
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

def search(tag):
    try:
        c = tweepy.Cursor(api.search, q=tag)
        print("Searching "+tag)
        i = 0 
        for tweet in c.items():
            if i < 1 and tweet.retweet_count > 100:
                if check_tweet(tweet):
                    api.retweet(tweet.id)
                    db_tweet = {"id": tweet.id}
                    requests.post(fb_url, json.dumps(db_tweet))
                    i += 1
                    break
    # Exceptions
    except KeyboardInterrupt:
        sys.exit("KeyboardInterrupt")
    except Exception as e:
        print(e)
        pass


#Get Batting Status
def getBattingLine(uniquePlayers, batting, teams, master):

    batData = batting.iloc[[random.randint(0, len(batting)-1)]]
    
    if (not batData.playerID.values[0] in uniquePlayers) or (batData.PA.values[0] == 0):
        getBattingLine(uniquePlayers, batting, teams, master)
        
    else:
        name = master[master.playerID == batData.playerID.values[0]].nameFirst.values[0] + \
                " " + master[master.playerID == batData.playerID.values[0]].nameLast.values[0]
    
        year = batData.yearID.values[0].astype(int)
        
        teamName = teams[(teams.teamID == batData.teamID.values[0]) &
                         (teams.yearID == batData.yearID.values[0])].name.values[0]
        
        games = batData.G.values[0].astype(int)
        plate = batData.PA.values[0].astype(int)
        
        hits = batData.H.values[0].astype(int)
        hrs = batData.HR.values[0].astype(int)
        sos = batData.SO.values[0].astype(int)
        
        line1 = name + " played for the " + teamName + " in the year " + str(year) + ". He had " + \
                str(plate) + " plate appearances in " + str(games) + " games with " + str(hits) + " hits, " + \
                str(hrs) + " homeruns, and " + str(sos) + " strikeouts. #MLB #facts"
                
        line2 = "In the year " + str(year) + ", " + name + " played for the " + teamName +  ". He had " + \
                str(plate) + " plate appearances in " + str(games) + " games with " + str(hits) + " hits, " + \
                str(hrs) + " homeruns, and " + str(sos) + " strikeouts. #MLB #trivia"
                
        line3 = name + " played for the " + teamName + " in the year " + str(year) + ". He had " + \
                str(hits) + " hits, " + str(hrs) + " homeruns, and " + str(sos) + " strikeouts while recording " + \
                str(plate) + " plate appearances in " + str(games) + " games! #MLB #trivia"  
                
        line4 = "In the year " + str(year) + ", " + name + " played for the " + teamName +  ". He had " + \
                str(hits) + " hits, " + str(hrs) + " homeruns, and " + str(sos) + " strikeouts while recording " + \
                str(plate) + " plate appearances in " + str(games) + " games! #MLB #facts"
    
        lines = [line1, line2, line3, line4]
        
        finalLine = lines[random.randint(0, 3)]
        
        return finalLine

#Get Pitching Status
def getPitchingLine(uniquePlayers, pitching, teams, master):

    pitData = pitching.iloc[[random.randint(0, len(pitching)-1)]]
    
    if (not pitData.playerID.values[0] in uniquePlayers) or (pitData.IP.values[0] == 0):
        getPitchingLine(uniquePlayers, pitching, teams, master)
        
    else:
        name = master[master.playerID == pitData.playerID.values[0]].nameFirst.values[0] + \
                " " + master[master.playerID == pitData.playerID.values[0]].nameLast.values[0]
    
        year = pitData.yearID.values[0].astype(int)
        
        teamName = teams[(teams.teamID == pitData.teamID.values[0]) &
                         (teams.yearID == pitData.yearID.values[0])].name.values[0]
        
        games = pitData.G.values[0].astype(int)
        era = pitData.ERA.values[0].astype(float)
        
        whip = round(pitData.WHIP.values[0].astype(float),2)
        ips = round(pitData.IP.values[0].astype(float), 2)
        wins = pitData.W.values[0].astype(int)
        loss = pitData.L.values[0].astype(int)
        
        line1 = name + " pitched for the " + teamName + " in the year " + str(year) + ". He pitched " + \
                str(ips) + " innings over " + str(games) + " games with a " + str(era) + " ERA, " + \
                str(whip) + " WHIP, and a " + str(wins) + "-" + str(loss) + " record. #MLB #trivia"
                
        line2 = "In the year " + str(year) + ", " + name + " pitched for the " + teamName +  ". He pitched " + \
                str(ips) + " innings over " + str(games) + " games with a " + str(era) + " ERA, " + \
                str(whip) + " WHIP, and a " + str(wins) + "-" + str(loss) + " record. #MLB #facts"
                
        line3 = name + " pitched for the " + teamName + " in the year " + str(year) + ". He had a " + \
                str(era) + " ERA, " + str(whip) + " WHIP, and a " + str(wins) + "-" + str(loss) + " record while pitching " + \
                str(ips) + " innings over " + str(games) + " games! #MLB #facts"  
                
        line4 = "In the year " + str(year) + ", " + name + " pitched for the " + teamName +  ". He had a " + \
                str(era) + " ERA, " + str(whip) + " WHIP, and a " + str(wins) + "-" + str(loss) + " record while pitching " + \
                str(ips) + " innings over " + str(games) + " games. #MLB #trivia"  
    
        lines = [line1, line2, line3, line4]
        
        finalLine = lines[random.randint(0, 3)]
        
        return finalLine
    
def getStatus(uniquePlayers, batting, pitching, teams, master):
    path = random.randint(1, 2)
    status = "I hope you have a great day!"
    if path == 1:
        status = getBattingLine(uniquePlayers, batting, teams, master)
    else:
        status = getPitchingLine(uniquePlayers, pitching, teams, master)
    
    return status

def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else: #Over midnight
        return nowTime >= startTime or nowTime <= endTime
    
#Main function. Gets data, connects to twitter, writes status.
def main(): 
    
    #define data
    master = pd.read_csv(r"https://raw.githubusercontent.com/ABoothInTheWild/baseball-research/master/TwitterBot/Data/Master.csv")
    batting = pd.read_csv(r"https://raw.githubusercontent.com/ABoothInTheWild/baseball-research/master/TwitterBot/Data/Batting.csv")
    batting = batting.dropna(subset=["SO"]).fillna(0)
    pitching = pd.read_csv(r"https://raw.githubusercontent.com/ABoothInTheWild/baseball-research/master/TwitterBot/Data/Pitching.csv")
    teams = pd.read_csv(r"https://raw.githubusercontent.com/ABoothInTheWild/baseball-research/master/TwitterBot/Data/Teams.csv")
    batting["PA"] = batting.AB + batting.BB + batting.HBP + batting.SH + batting.SF
    pitching["IP"] = pitching.IPouts / 3.0
    pitching["WHIP"] = (pitching.H + pitching.BB) / pitching.IP
    uniquePlayers = master.playerID.unique()
    
    #enter the corresponding information from your Twitter application:
    CONSUMER_KEY = '2gBiPBoAovxg7PDNeX6jXTKLX'
    CONSUMER_SECRET = '3YT9LXW7StJ7OoDMHgw8kFVzXZEQK2H2ilnFrseXsUCDLcXSaJ'
    ACCESS_KEY = '931373265653784576-4fgDnw0hbNJ1BAV3egNrh07URyPB6FU'
    ACCESS_SECRET = 'oM1EGxPDqtWiY8Yrvd7j72dMownO7YGYcaqDDhQFREQzh'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
        
    #Get time. Don't post in the middle of the night
    timeStart = '7:00AM'
    timeEnd = '11:00PM'
    timeEnd = datetime.strptime(timeEnd, "%I:%M%p").time()
    timeStart = datetime.strptime(timeStart, "%I:%M%p").time()
    
    numTweets = 10
    tweetCount = 0
    
    while tweetCount < numTweets:
        timeNow = datetime.now().time()
        test = random.randint(1, 2)
        #Only post 1 out of 2 tries
        if (isNowInTimePeriod(timeStart, timeEnd, timeNow)) and (test != 1):
            try:
                status = getStatus(uniquePlayers, batting, pitching, teams, master)
                api.update_status(status)
            # Additions below
            except KeyboardInterrupt:
                sys.exit("KeyboardInterrupt")
            except Exception as e:
                print(e)
                status = getStatus(uniquePlayers, batting, pitching, teams, master)
                api.update_status(status)
            tweetCount += 1
            time1 = random.randint(1, 4)
            if time1 == 1:
                time.sleep(2100) #Tweet every 35 minutes
            elif time1 == 2:
                time.sleep(3900) #Tweet every 65 minutes
            elif time1 == 3:
                time.sleep(2760) #Tweet every 46 minutes
            else:
                time.sleep(1410) #Tweet every 23.5 minutes            
            
        else:
            pass
        
if __name__ == "__main__":
    main()