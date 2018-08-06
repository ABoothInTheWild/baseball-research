# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 21:48:19 2018

@author: Alexander
"""

#2017 Preseason Playoff Odds
import heapq
from collections import Counter
import pandas as pd
import numpy as np
from scipy.stats import beta
import os

#read data
os.chdir('C:/Users/Alexander/Documents/baseball/Past Perf Playoffs')
beta17Pre = pd.read_csv("mlb2017PreSeasonBetaEstimates.csv")

#Name Divisions
AL_East = ["BOS", "NYY", "TOR", "BAL", "TBR"]
AL_Central = ["CLE", "DET", "CHW", "MIN", "KCR"]
AL_West = ["TEX", "HOU", "SEA", "OAK", "LAA"]
NL_East = ["PHI", "WSN", "MIA", "NYM", "ATL"]
NL_Central = ["STL", "CHC", "MIL", "PIT", "CIN"]
NL_West = ["LAD", "SFG", "SDP", "ARI", "COL"]

Divisions = [AL_West, AL_Central, AL_East, NL_West, NL_Central, NL_East]
AL = [AL_West, AL_Central, AL_East]
NL = [NL_West, NL_Central, NL_East]

#Divisional Odds
resultsDF = pd.DataFrame()
teams = []
divOdds = []
np.random.seed(seed=54321)
ntrials=100000
for div in Divisions:
    results = Counter({0: 0, 1: 0, 2: 0, 3: 0, 4: 0})
    tempResults = []
    for team in div:
        alphaEst = beta17Pre[beta17Pre.Team_Abbr == team]["PriorAlpha"].values[0]
        betaEst = beta17Pre[beta17Pre.Team_Abbr == team]["PriorBeta"].values[0]
        sample = beta.rvs(alphaEst, betaEst, size=ntrials)
        tempResults.append(np.round(sample*162,0))
    argMaxesIndx = np.argmax(np.array(tempResults), axis=0)
    results.update(argMaxesIndx)
    teams.extend(div)
    divOdds.extend(np.array(results.values())/float(ntrials))
resultsDF["Teams"] = teams
resultsDF["DivisionOdds"] = divOdds

#AL WildCards
wcOdds = []
resultsWC = Counter({0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0
                     , 10: 0, 11: 0, 12: 0, 13: 0, 14: 0})
wcTempResults = []
for div in AL:
    tempResults = []
    for team in div:
        alphaEst = beta17Pre[beta17Pre.Team_Abbr == team]["PriorAlpha"].values[0]
        betaEst = beta17Pre[beta17Pre.Team_Abbr == team]["PriorBeta"].values[0]
        sample = beta.rvs(alphaEst, betaEst, size=ntrials)
        tempResults.append(np.round(sample*162,0))
    tempResults = np.transpose(np.array(tempResults))
    tempResults[np.arange(len(tempResults)), np.argmax(tempResults, axis=1)] = 0
    wcTempResults.extend(np.transpose(tempResults))
wcTempResults = np.array(wcTempResults)
argMaxesIndx = [heapq.nlargest(2, xrange(len(wcTempResults[:,i])), 
                key=wcTempResults[:,i].__getitem__) 
    for i in range(np.size(wcTempResults,1))]
resultsWC.update(np.array(argMaxesIndx).flatten())
wcOdds.extend(np.array(resultsWC.values())/float(ntrials))

#NL WildCards
resultsWC2 = Counter({0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0
                     , 10: 0, 11: 0, 12: 0, 13: 0, 14: 0})
wcTempResults = []
for div in NL:
    tempResults = []
    for team in div:
        alphaEst = beta17Pre[beta17Pre.Team_Abbr == team]["PriorAlpha"].values[0]
        betaEst = beta17Pre[beta17Pre.Team_Abbr == team]["PriorBeta"].values[0]
        sample = beta.rvs(alphaEst, betaEst, size=ntrials)
        tempResults.append(np.round(sample*162,0))
    tempResults = np.transpose(np.array(tempResults))
    tempResults[np.arange(len(tempResults)), np.argmax(tempResults, axis=1)] = 0
    wcTempResults.extend(np.transpose(tempResults))
wcTempResults = np.array(wcTempResults)
argMaxesIndx = [heapq.nlargest(2, xrange(len(wcTempResults[:,i])), 
                key=wcTempResults[:,i].__getitem__) 
    for i in range(np.size(wcTempResults,1))]
resultsWC2.update(np.array(argMaxesIndx).flatten())
wcOdds.extend(np.array(resultsWC.values())/float(ntrials))

resultsDF["WCOdds"] = wcOdds
resultsDF["PlayoffOdds"] = resultsDF.DivisionOdds + resultsDF.WCOdds

#Attach point win estimates and confidence itervals
resultsDF = resultsDF.sort_values(by=["Teams"]).reset_index(drop=True)
beta17PreSorted = beta17Pre.sort_values(by=["Team_Abbr"]).reset_index(drop=True)
resultsDF_Full = pd.concat([resultsDF, beta17PreSorted.iloc[:,19:37]], axis=1)

#Write CSV
#resultsDF_Full.to_csv("mlb2017PreSeasonPlayoffOdds.csv", index=False)

#############################################################################

#July Playoff Odds

#read data downloaded from xmlStats API
mlb17Results = pd.read_csv("mlb2017SeasonResults.csv")

from datetime import timedelta, date
#https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

dates = []
start_date = date(2017, 4, 2)
end_date = date(2017, 10, 2)
for single_date in daterange(start_date, end_date):
    dates.append(single_date.strftime("%Y%m%d"))

#Divisional Odds
resultsDF = pd.DataFrame()
teams = []
divOdds = []
np.random.seed(seed=54321)
ntrials=100000
for div in Divisions:
    results = Counter({0: 0, 1: 0, 2: 0, 3: 0, 4: 0})
    tempResults = []
    for team in div:        
        team17Res = mlb17Results[mlb17Results.Team_Abbr==team].iloc[:,2:368]
        teamWins = team17Res.iloc[:,range(0,366,2)].values[0]
        teamLosses = team17Res.iloc[:,range(1,367,2)].values[0]   
        ix = dates.index('20170711')
        
        alphaEst = beta17Pre[beta17Pre.Team_Abbr == team]["PriorAlpha"].values[0] + teamWins[ix]
        betaEst = beta17Pre[beta17Pre.Team_Abbr == team]["PriorBeta"].values[0] + teamLosses[ix]
        sample = beta.rvs(alphaEst, betaEst, size=ntrials)
        tempResults.append(np.round(sample*162,0))
    argMaxesIndx = np.argmax(np.array(tempResults), axis=0)
    results.update(argMaxesIndx)
    teams.extend(div)
    divOdds.extend(np.array(results.values())/float(ntrials))
resultsDF["Teams"] = teams
resultsDF["DivisionOdds"] = divOdds

#AL WildCards
wcOdds = []
resultsWC = Counter({0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0
                     , 10: 0, 11: 0, 12: 0, 13: 0, 14: 0})
wcTempResults = []
for div in AL:
    tempResults = []
    for team in div:
        team17Res = mlb17Results[mlb17Results.Team_Abbr==team].iloc[:,2:368]
        teamWins = team17Res.iloc[:,range(0,366,2)].values[0]
        teamLosses = team17Res.iloc[:,range(1,367,2)].values[0]   
        ix = dates.index('20170711')
        
        alphaEst = beta17Pre[beta17Pre.Team_Abbr == team]["PriorAlpha"].values[0] + teamWins[ix]
        betaEst = beta17Pre[beta17Pre.Team_Abbr == team]["PriorBeta"].values[0] + teamLosses[ix]
        sample = beta.rvs(alphaEst, betaEst, size=ntrials)
        tempResults.append(np.round(sample*162,0))
    tempResults = np.transpose(np.array(tempResults))
    tempResults[np.arange(len(tempResults)), np.argmax(tempResults, axis=1)] = 0
    wcTempResults.extend(np.transpose(tempResults))
wcTempResults = np.array(wcTempResults)
argMaxesIndx = [heapq.nlargest(2, xrange(len(wcTempResults[:,i])), 
                key=wcTempResults[:,i].__getitem__) 
    for i in range(np.size(wcTempResults,1))]
resultsWC.update(np.array(argMaxesIndx).flatten())
wcOdds.extend(np.array(resultsWC.values())/float(ntrials))

#NL WildCards
resultsWC2 = Counter({0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0
                     , 10: 0, 11: 0, 12: 0, 13: 0, 14: 0})
wcTempResults = []
for div in NL:
    tempResults = []
    for team in div:
        team17Res = mlb17Results[mlb17Results.Team_Abbr==team].iloc[:,2:368]
        teamWins = team17Res.iloc[:,range(0,366,2)].values[0]
        teamLosses = team17Res.iloc[:,range(1,367,2)].values[0]   
        ix = dates.index('20170711')
        
        alphaEst = beta17Pre[beta17Pre.Team_Abbr == team]["PriorAlpha"].values[0] + teamWins[ix]
        betaEst = beta17Pre[beta17Pre.Team_Abbr == team]["PriorBeta"].values[0] + teamLosses[ix]
        sample = beta.rvs(alphaEst, betaEst, size=ntrials)
        tempResults.append(np.round(sample*162,0))
    tempResults = np.transpose(np.array(tempResults))
    tempResults[np.arange(len(tempResults)), np.argmax(tempResults, axis=1)] = 0
    wcTempResults.extend(np.transpose(tempResults))
wcTempResults = np.array(wcTempResults)
argMaxesIndx = [heapq.nlargest(2, xrange(len(wcTempResults[:,i])), 
                key=wcTempResults[:,i].__getitem__) 
    for i in range(np.size(wcTempResults,1))]
resultsWC2.update(np.array(argMaxesIndx).flatten())
wcOdds.extend(np.array(resultsWC.values())/float(ntrials))

resultsDF["WCOdds"] = wcOdds
resultsDF["PlayoffOdds"] = resultsDF.DivisionOdds + resultsDF.WCOdds

#Attach point win estimates and confidence itervals
resultsDF = resultsDF.sort_values(by=["Teams"]).reset_index(drop=True)
beta17PreSorted = beta17Pre.sort_values(by=["Team_Abbr"]).reset_index(drop=True)
resultsDF_Full = pd.concat([resultsDF, beta17PreSorted.iloc[:,19:37]], axis=1)

#Write CSV
#resultsDF_Full.to_csv("mlb2017JulyPlayoffOdds.csv", index=False)