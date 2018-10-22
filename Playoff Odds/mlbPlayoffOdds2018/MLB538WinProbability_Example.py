# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 11:45:10 2018

@author: ABooth
"""

import os

from MLBWinProbability import *
from MLB538WinProbability import *
import pandas as pd
from xmlstats import xmlstats
from datetime import timedelta, datetime, date
import time
import numpy as np

#https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
#for dates in daterange(datetime(2018,3,29), datetime.today()):
    #print(dates)
    
access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
user_agent = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    
df = pd.read_csv("https://projects.fivethirtyeight.com/mlb-api/mlb_elo.csv")
df = df[df.season == 2018]
df.date = pd.to_datetime(df.date)
df = df.sort_values(["date"]).reset_index(drop=True)

print(getMLBGamesFromDate(datetime(2018, 4, 1), df))

#last year data
endOfReg2017 = datetime(2017, 10, 2)  #2017 last day
stats1 = xmlstats.Xmlstats(access_token, user_agent)
date_format1 = endOfReg2017.strftime("%Y%m%d")    
lastYearStandingsOnDate = stats1.standings(date=date_format1, sport="mlb")

print(MLBWinProbability('TBR', 'BOS', np.NAN, lastYearStandingsOnDate, True, datetime(2018, 4, 1)))
print(MLB538WinProbability('TBR', 'BOS', datetime(2018, 4, 1), df))

start_date = datetime(2018, 3, 29)
end_date = datetime(2018, 9, 27)   
ssGameScore = 0
fivGameScore = 0
ssBrierScore = 0
fivBrierScore = 0
totalGames = 0
for single_date in daterange(start_date, end_date):
    games = getMLBGamesFromDate(single_date, df)
    stats = xmlstats.Xmlstats(access_token, user_agent)
    date_format = single_date.strftime("%Y%m%d")    
    xmlStandingsOnDate = stats.standings(date=date_format, sport="mlb")
    totalGames += len(games)
    for gamePair in games:
        homeTeam = gamePair[0]
        awayTeam = gamePair[1]
        ssProb = MLBWinProbability(homeTeam, awayTeam, xmlStandingsOnDate, lastYearStandingsOnDate)
        five38Prob = MLB538WinProbability(homeTeam, awayTeam, single_date, df)
        homeWon = getMLBResultsFromTeamsAndDate(homeTeam, awayTeam, single_date, df)[0]
        #print("On " + str(single_date.strftime("%Y%m%d")) + ", " + homeTeam + " has a " + str(round(ssProb, 3)) + " prob of beating " + awayTeam + " from SaberSmart and a " + str(round(five38Prob, 3)) + " from 538.")
        ssGameScore += getGameScore(ssProb, homeWon)
        fivGameScore += getGameScore(five38Prob, homeWon)
        ssBrierScore += getBrierScore(ssProb, homeWon)
        fivBrierScore += getBrierScore(five38Prob, homeWon)
    print(str(single_date.strftime("%Y%m%d")))
    time.sleep(12)        
print(ssGameScore)
print(fivGameScore)
print(ssBrierScore)
print(fivBrierScore)

###############################################################
stats = xmlstats.Xmlstats(access_token, user_agent)
date_format = datetime.today().strftime("%Y%m%d")    
xmlStandingsOnDate = stats.standings(date=date_format, sport="mlb")
#last year data
endOfReg2017 = datetime(2017, 10, 2)  #2017 last day
stats1 = xmlstats.Xmlstats(access_token, user_agent)
date_format1 = endOfReg2017.strftime("%Y%m%d")    
lastYearStandingsOnDate = stats1.standings(date=date_format1, sport="mlb")

MLBWinProbability('MIL', 'COL', xmlStandingsOnDate, lastYearStandingsOnDate)


print(1-MLBWinProbability('SFG', 'LAD', xmlStandingsOnDate, lastYearStandingsOnDate))
print(MLBWinProbability('COL', 'WSN', xmlStandingsOnDate, lastYearStandingsOnDate))


print(MLBWinProbability('MIL', 'DET', xmlStandingsOnDate, lastYearStandingsOnDate))
#1.84

print(MLBWinProbability('CHC', 'STL', xmlStandingsOnDate, lastYearStandingsOnDate))
#2.24

(1 - MLBWinProbability('SFG', 'LAD', xmlStandingsOnDate, lastYearStandingsOnDate))**2 * (1-MLBWinProbability('COL', 'WSN', xmlStandingsOnDate, lastYearStandingsOnDate))**2


2*((1 - MLBWinProbability('SFG', 'LAD', xmlStandingsOnDate, lastYearStandingsOnDate))**2 * (MLBWinProbability('COL', 'WSN', xmlStandingsOnDate, lastYearStandingsOnDate)*(1-MLBWinProbability('COL', 'WSN', xmlStandingsOnDate, lastYearStandingsOnDate)))) + (1 - MLBWinProbability('SFG', 'LAD', xmlStandingsOnDate, lastYearStandingsOnDate))**2 * ((1-MLBWinProbability('COL', 'WSN', xmlStandingsOnDate, lastYearStandingsOnDate))**2) + 2*(((1 - MLBWinProbability('SFG', 'LAD', xmlStandingsOnDate, lastYearStandingsOnDate))*MLBWinProbability('SFG', 'LAD', xmlStandingsOnDate, lastYearStandingsOnDate)) * ((1-MLBWinProbability('COL', 'WSN', xmlStandingsOnDate, lastYearStandingsOnDate))**2))


2*((MLBWinProbability('MIL', 'DET', xmlStandingsOnDate, lastYearStandingsOnDate))**2 * (MLBWinProbability('CHC', 'STL', xmlStandingsOnDate, lastYearStandingsOnDate)*(1-MLBWinProbability('CHC', 'STL', xmlStandingsOnDate, lastYearStandingsOnDate)))) + (MLBWinProbability('MIL', 'DET', xmlStandingsOnDate, lastYearStandingsOnDate))**2 * ((1-MLBWinProbability('CHC', 'STL', xmlStandingsOnDate, lastYearStandingsOnDate))**2) + 2*(((MLBWinProbability('MIL', 'DET', xmlStandingsOnDate, lastYearStandingsOnDate))*(1-MLBWinProbability('MIL', 'DET', xmlStandingsOnDate, lastYearStandingsOnDate))) * ((1-MLBWinProbability('CHC', 'STL', xmlStandingsOnDate, lastYearStandingsOnDate))**2))

(MLBWinProbability('MIL', 'DET', xmlStandingsOnDate, lastYearStandingsOnDate))**2 * (1-MLBWinProbability('CHC', 'STL', xmlStandingsOnDate, lastYearStandingsOnDate))**2





print((1-MLBWinProbability('COL', 'WSN', xmlStandingsOnDate, lastYearStandingsOnDate))*MLBWinProbability('SFG', 'LAD', xmlStandingsOnDate, lastYearStandingsOnDate) + (1-MLBWinProbability('SFG', 'LAD', xmlStandingsOnDate, lastYearStandingsOnDate))*MLBWinProbability('COL', 'WSN', xmlStandingsOnDate, lastYearStandingsOnDate))

print(MLBWinProbability('CHC', 'STL', xmlStandingsOnDate, lastYearStandingsOnDate)*MLBWinProbability('MIL', 'DET', xmlStandingsOnDate, lastYearStandingsOnDate) + (1-MLBWinProbability('MIL', 'DET', xmlStandingsOnDate, lastYearStandingsOnDate))*(1-MLBWinProbability('CHC', 'STL', xmlStandingsOnDate, lastYearStandingsOnDate)))



print(1-MLB538WinProbability('SFG', 'LAD', datetime(2018, 9, 30), df))
print(MLB538WinProbability('COL', 'WSN', datetime(2018, 9, 30), df))

print(MLB538WinProbability('MIL', 'DET', datetime(2018, 9, 30), df))
print(MLB538WinProbability('CHC', 'STL', datetime(2018, 9, 30), df))

print((1-MLB538WinProbability('SFG', 'LAD', datetime(2018, 9, 30), df))*MLB538WinProbability('COL', 'WSN', datetime(2018, 9, 30), df) + (1-MLB538WinProbability('COL', 'WSN', datetime(2018, 9, 30), df))*MLB538WinProbability('SFG', 'LAD', datetime(2018, 9, 30), df))

print(MLB538WinProbability('CHC', 'STL', datetime(2018, 9, 30), df) * MLB538WinProbability('MIL', 'DET', datetime(2018, 9, 30), df) + (1-MLB538WinProbability('MIL', 'DET', datetime(2018, 9, 30), df))*(1-MLB538WinProbability('CHC', 'STL', datetime(2018, 9, 30), df)))



print(MLBWinProbability('CHC', 'COL', xmlStandingsOnDate, lastYearStandingsOnDate))


###############################################################

print(MLBWinProbability('CHC', 'COL', xmlStandingsOnDate, lastYearStandingsOnDate))
print(MLB538WinProbability('CHC', 'COL', datetime(2018, 10, 2), df))

print(MLBWinProbability('NYY', 'OAK', xmlStandingsOnDate, lastYearStandingsOnDate))
print(MLB538WinProbability('NYY', 'OAK', datetime(2018, 10, 3), df))
