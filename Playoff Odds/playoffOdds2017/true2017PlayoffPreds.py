# -*- coding: utf-8 -*-
"""
Created on Sun Aug 05 22:49:05 2018

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
os.chdir('C:/Users/abooth/Documents/Python Scripts/PastPreds/playoffOdds/2018')
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
DivisionsLeague = [AL, NL]

AL_Teams = ["TEX", "HOU", "SEA", "OAK", "LAA", "CLE", "DET", "CHW", "MIN", "KCR",
            "BOS", "NYY", "TOR", "BAL", "TBR"]
NL_Teams = ["LAD", "SFG", "SDP", "ARI", "COL", "STL", "CHC", "MIL", "PIT", "CIN",
            "PHI", "WSN", "MIA", "NYM", "ATL"]
LeagueTeams = [AL_Teams, NL_Teams]

#init Odds arrays
resultsDF = pd.DataFrame()
teams = []
divOdds = []
wcOdds = []
expectedWins = []

ntrials=100000

np.random.seed(seed=54321)
for league in DivisionsLeague:
    #Init wildcard counters per league
    resultsWC = Counter({0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0
                     , 10: 0, 11: 0, 12: 0, 13: 0, 14: 0})
    wcTempResults = []
    for div in league:
        #init div winner counters
        results = Counter({0: 0, 1: 0, 2: 0, 3: 0, 4: 0})
        tempResults = []
        for team in div:
            alphaEst = beta17Pre[beta17Pre.Team_Abbr == team]["PriorAlpha"].values[0]
            betaEst = beta17Pre[beta17Pre.Team_Abbr == team]["PriorBeta"].values[0]
            sample = beta.rvs(alphaEst, betaEst, size=ntrials)
            tempResults.append(np.round(sample*162,0))
            expectedWins.append(np.round(np.mean(sample*162),0))
        #Find division winners
        divMaxesIndx = np.argmax(np.array(tempResults), axis=0)
        results.update(divMaxesIndx)    
        teams.extend(div)
        divOdds.extend(np.array(list(results.values()))/float(ntrials))
        #remove division winners
        tempResults = np.transpose(np.array(tempResults))
        tempResults[np.arange(len(tempResults)), np.argmax(tempResults, axis=1)] = 0
        wcTempResults.extend(np.transpose(tempResults))
    #find league wildcards    
    wcTempResults = np.array(wcTempResults)
    argMaxesIndx = [heapq.nlargest(2, range(len(wcTempResults[:,i])), 
                    key=wcTempResults[:,i].__getitem__) 
                    for i in range(np.size(wcTempResults,1))]
    resultsWC.update(np.array(argMaxesIndx).flatten())
    wcOdds.extend(np.array(list(resultsWC.values()))/float(ntrials))
        
        
resultsDF["Teams"] = teams
resultsDF["DivisionOdds20170401"] = divOdds
resultsDF["WildCardOdds20170401"] = wcOdds
resultsDF["PlayoffOdds20170401"] = resultsDF.DivisionOdds20170401 + resultsDF.WildCardOdds20170401
resultsDF["ExpectedWins20170401"] = expectedWins

#Attach point win estimates and confidence itervals
#resultsDF = resultsDF.sort_values(by=["Teams"]).reset_index(drop=True)
#beta17PreSorted = beta17Pre.sort_values(by=["Team_Abbr"]).reset_index(drop=True)
#resultsDF_Full = pd.concat([resultsDF, beta17PreSorted.iloc[:,19:37]], axis=1)

#resultsDF.to_csv("mlb2017PreseasonPlayoffPreds.csv", index=False)
###############################################################################

#Create playoff odds per day per prior per team

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
 
#resultsDF = pd.DataFrame()
for i in range(len(dates)):
    currDate = dates[i]
    
    #init Odds arrays
    teams = []
    divOdds = []
    wcOdds = []
    expectedWins = []
    
    ntrials=100000
    np.random.seed(seed=54321)
    for league in DivisionsLeague:
        #Init wildcard counters per league
        resultsWC = Counter({0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0
                         , 10: 0, 11: 0, 12: 0, 13: 0, 14: 0})
        wcTempResults = []
        for div in league:
            #init div winner counters
            results = Counter({0: 0, 1: 0, 2: 0, 3: 0, 4: 0})
            tempResults = []
            for team in div:
                #get priors
                priorA = beta17Pre[beta17Pre.Team_Abbr == team]["PriorAlpha"].values[0]
                priorB = beta17Pre[beta17Pre.Team_Abbr == team]["PriorBeta"].values[0]
                #get posteriors
                team17Res = mlb17Results[mlb17Results.Team_Abbr==team].iloc[:,2:368]
                teamWins = team17Res.iloc[:,range(0,366,2)].values[0]
                teamLosses = team17Res.iloc[:,range(1,367,2)].values[0]
                posteriorAlpha = priorA + teamWins[i]
                posteriorBeta = priorB + teamLosses[i]    
                #where the magic happens
                sample = beta.rvs(posteriorAlpha, posteriorBeta, size=ntrials)
                gamesLeft = 162 - teamWins[i] - teamLosses[i]
                winEstimate = np.round(teamWins[i] + sample*gamesLeft,0)
                tempResults.append(winEstimate)
                expectedWins.append(np.round(np.mean(teamWins[i] + sample*gamesLeft),0))
            #Find division winners
            divMaxesIndx = np.argmax(np.array(tempResults), axis=0)
            results.update(divMaxesIndx)    
            teams.extend(div)
            divOdds.extend(np.array(list(results.values()))/float(ntrials))
            #remove division winners
            tempResults = np.transpose(np.array(tempResults))
            tempResults[np.arange(len(tempResults)), np.argmax(tempResults, axis=1)] = 0
            wcTempResults.extend(np.transpose(tempResults))
        #find league wildcards    
        wcTempResults = np.array(wcTempResults)
        argMaxesIndx = [heapq.nlargest(2, range(len(wcTempResults[:,j])), 
                        key=wcTempResults[:,j].__getitem__) 
                        for j in range(np.size(wcTempResults,1))]
        resultsWC.update(np.array(argMaxesIndx).flatten())
        wcOdds.extend(np.array(list(resultsWC.values()))/float(ntrials))
            
            
    resultsDF["Teams"] = teams
    resultsDF["DivisionOdds" + currDate] = divOdds
    resultsDF["WildCardOdds" + currDate] = wcOdds
    resultsDF["PlayoffOdds" + currDate] = resultsDF["DivisionOdds" + currDate] + resultsDF["WildCardOdds" + currDate]
    resultsDF["ExpectedWins" + currDate] = expectedWins
    
resultsDF.to_csv("mlb2017PlayoffPreds.csv", index=False)
##############################################################################

#Playoff Odds

resultsDF = pd.read_csv("mlb2017PlayoffPreds.csv")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

dates = []
start_date = date(2017, 4, 1)
end_date = date(2017, 10, 2)
for single_date in daterange(start_date, end_date):
    dates.append(single_date)

#NL West
NLWestPreds = resultsDF[resultsDF.Teams.isin(NL_West)]
teamHeaders = NLWestPreds.Teams.values
playoffCols = NLWestPreds.columns[NLWestPreds.columns.str.startswith('PlayoffOdds')]
NLWestPreds = NLWestPreds[playoffCols]
NLWestPreds = pd.DataFrame(np.transpose(NLWestPreds.values))
NLWestPreds.columns = teamHeaders
      
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
plt.plot(dates, NLWestPreds['LAD'], c='b', label='_nolegend_') 
ax.scatter(dates, NLWestPreds['LAD'], c='b', marker="o", label='LAD')
plt.plot(dates, NLWestPreds['ARI'], c='r', label='_nolegend_')
ax.scatter(dates, NLWestPreds['ARI'], c='r', marker="o", label='ARI')
plt.plot(dates, NLWestPreds['COL'], c='purple', label='_nolegend_')
ax.scatter(dates, NLWestPreds['COL'], c='purple', marker="o", label='COL')
plt.plot(dates, NLWestPreds['SDP'], c='green', label='_nolegend_')
ax.scatter(dates, NLWestPreds['SDP'], c='green', marker="o", label='SDP')
plt.plot(dates, NLWestPreds['SFG'], c='orange', label='_nolegend_')
ax.scatter(dates, NLWestPreds['SFG'], c='orange', marker="o", label='SFG')
ax.legend(loc='best', frameon=False)
plt.title('NL West 2017 Bayesian Playoff Probabilities')
plt.ylabel('Playoff Probabilities')
plt.xlabel('')
ax.set_ylim(0, 1.05)
myFmt = mdates.DateFormatter('%B')
ax.xaxis.set_major_formatter(myFmt)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
fig.savefig('NLWest2017PlayoffOdds.png', bbox_inches='tight')

#NL Central
NLCentralPreds = resultsDF[resultsDF.Teams.isin(NL_Central)]
teamHeaders = NLCentralPreds.Teams.values
playoffCols = NLCentralPreds.columns[NLCentralPreds.columns.str.startswith('PlayoffOdds')]
NLCentralPreds = NLCentralPreds[playoffCols]
NLCentralPreds = pd.DataFrame(np.transpose(NLCentralPreds.values))
NLCentralPreds.columns = teamHeaders
      
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
plt.plot(dates, NLCentralPreds['CHC'], c='b', label='_nolegend_') 
ax.scatter(dates, NLCentralPreds['CHC'], c='b', marker="o", label='CHC')
plt.plot(dates, NLCentralPreds['STL'], c='r', label='_nolegend_')
ax.scatter(dates, NLCentralPreds['STL'], c='r', marker="o", label='STL')
plt.plot(dates, NLCentralPreds['PIT'], c='black', label='_nolegend_')
ax.scatter(dates, NLCentralPreds['PIT'], c='black', marker="o", label='PIT')
plt.plot(dates, NLCentralPreds['MIL'], c='green', label='_nolegend_')
ax.scatter(dates, NLCentralPreds['MIL'], c='green', marker="o", label='MIL')
plt.plot(dates, NLCentralPreds['CIN'], c='orange', label='_nolegend_')
ax.scatter(dates, NLCentralPreds['CIN'], c='orange', marker="o", label='CIN')
ax.legend(loc='best', frameon=False)
plt.title('NL Central 2017 Bayesian Playoff Probabilities')
plt.ylabel('Playoff Probabilities')
plt.xlabel('')
ax.set_ylim(0, 1.05)
myFmt = mdates.DateFormatter('%B')
ax.xaxis.set_major_formatter(myFmt)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
fig.savefig('NLCentral2017PlayoffOdds.png', bbox_inches='tight')

#NL East
NLEastPreds = resultsDF[resultsDF.Teams.isin(NL_East)]
teamHeaders = NLEastPreds.Teams.values
playoffCols = NLEastPreds.columns[NLEastPreds.columns.str.startswith('PlayoffOdds')]
NLEastPreds = NLEastPreds[playoffCols]
NLEastPreds = pd.DataFrame(np.transpose(NLEastPreds.values))
NLEastPreds.columns = teamHeaders
      
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
plt.plot(dates, NLEastPreds['NYM'], c='b', label='_nolegend_') 
ax.scatter(dates, NLEastPreds['NYM'], c='b', marker="o", label='NYM')
plt.plot(dates, NLEastPreds['WSN'], c='r', label='_nolegend_')
ax.scatter(dates, NLEastPreds['WSN'], c='r', marker="o", label='WSN')
plt.plot(dates, NLEastPreds['PHI'], c='purple', label='_nolegend_')
ax.scatter(dates, NLEastPreds['PHI'], c='purple', marker="o", label='PHI')
plt.plot(dates, NLEastPreds['ATL'], c='green', label='_nolegend_')
ax.scatter(dates, NLEastPreds['ATL'], c='green', marker="o", label='ATL')
plt.plot(dates, NLEastPreds['MIA'], c='orange', label='_nolegend_')
ax.scatter(dates, NLEastPreds['MIA'], c='orange', marker="o", label='MIA')
ax.legend(loc='best', frameon=False)
plt.title('NL East 2017 Bayesian Playoff Probabilities')
plt.ylabel('Playoff Probabilities')
plt.xlabel('')
ax.set_ylim(0, 1.05)
myFmt = mdates.DateFormatter('%B')
ax.xaxis.set_major_formatter(myFmt)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
fig.savefig('NLEast2017PlayoffOdds.png', bbox_inches='tight')

#AL West
ALWestPreds = resultsDF[resultsDF.Teams.isin(AL_West)]
teamHeaders = ALWestPreds.Teams.values
playoffCols = ALWestPreds.columns[ALWestPreds.columns.str.startswith('PlayoffOdds')]
ALWestPreds = ALWestPreds[playoffCols]
ALWestPreds = pd.DataFrame(np.transpose(ALWestPreds.values))
ALWestPreds.columns = teamHeaders
      
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
plt.plot(dates, ALWestPreds['TEX'], c='b', label='_nolegend_') 
ax.scatter(dates, ALWestPreds['TEX'], c='b', marker="o", label='TEX')
plt.plot(dates, ALWestPreds['LAA'], c='r', label='_nolegend_')
ax.scatter(dates, ALWestPreds['LAA'], c='r', marker="o", label='LAA')
plt.plot(dates, ALWestPreds['SEA'], c='purple', label='_nolegend_')
ax.scatter(dates, ALWestPreds['SEA'], c='purple', marker="o", label='SEA')
plt.plot(dates, ALWestPreds['OAK'], c='green', label='_nolegend_')
ax.scatter(dates, ALWestPreds['OAK'], c='green', marker="o", label='OAK')
plt.plot(dates, ALWestPreds['HOU'], c='orange', label='_nolegend_')
ax.scatter(dates, ALWestPreds['HOU'], c='orange', marker="o", label='HOU')
ax.legend(loc='best', frameon=False)
plt.title('AL West 2017 Bayesian Playoff Probabilities')
plt.ylabel('Playoff Probabilities')
plt.xlabel('')
ax.set_ylim(0, 1.05)
myFmt = mdates.DateFormatter('%B')
ax.xaxis.set_major_formatter(myFmt)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
fig.savefig('ALWest2017PlayoffOdds.png', bbox_inches='tight')

#AL Central
ALCentralPreds = resultsDF[resultsDF.Teams.isin(AL_Central)]
teamHeaders = ALCentralPreds.Teams.values
playoffCols = ALCentralPreds.columns[ALCentralPreds.columns.str.startswith('PlayoffOdds')]
ALCentralPreds = ALCentralPreds[playoffCols]
ALCentralPreds = pd.DataFrame(np.transpose(ALCentralPreds.values))
ALCentralPreds.columns = teamHeaders
      
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
plt.plot(dates, ALCentralPreds['KCR'], c='b', label='_nolegend_') 
ax.scatter(dates, ALCentralPreds['KCR'], c='b', marker="o", label='KCR')
plt.plot(dates, ALCentralPreds['CLE'], c='r', label='_nolegend_')
ax.scatter(dates, ALCentralPreds['CLE'], c='r', marker="o", label='CLE')
plt.plot(dates, ALCentralPreds['CHW'], c='black', label='_nolegend_')
ax.scatter(dates, ALCentralPreds['CHW'], c='black', marker="o", label='CHW')
plt.plot(dates, ALCentralPreds['MIN'], c='green', label='_nolegend_')
ax.scatter(dates, ALCentralPreds['MIN'], c='green', marker="o", label='MIN')
plt.plot(dates, ALCentralPreds['DET'], c='orange', label='_nolegend_')
ax.scatter(dates, ALCentralPreds['DET'], c='orange', marker="o", label='DET')
ax.legend(loc='best', frameon=False)
plt.title('AL Central 2017 Bayesian Playoff Probabilities')
plt.ylabel('Playoff Probabilities')
plt.xlabel('')
ax.set_ylim(0, 1.05)
myFmt = mdates.DateFormatter('%B')
ax.xaxis.set_major_formatter(myFmt)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
fig.savefig('ALCentral2017PlayoffOdds.png', bbox_inches='tight')

#AL East
ALEastPreds = resultsDF[resultsDF.Teams.isin(AL_East)]
teamHeaders = ALEastPreds.Teams.values
playoffCols = ALEastPreds.columns[ALEastPreds.columns.str.startswith('PlayoffOdds')]
ALEastPreds = ALEastPreds[playoffCols]
ALEastPreds = pd.DataFrame(np.transpose(ALEastPreds.values))
ALEastPreds.columns = teamHeaders
      
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
plt.plot(dates, ALEastPreds['TOR'], c='b', label='_nolegend_') 
ax.scatter(dates, ALEastPreds['TOR'], c='b', marker="o", label='TOR')
plt.plot(dates, ALEastPreds['BOS'], c='r', label='_nolegend_')
ax.scatter(dates, ALEastPreds['BOS'], c='r', marker="o", label='BOS')
plt.plot(dates, ALEastPreds['NYY'], c='black', label='_nolegend_')
ax.scatter(dates, ALEastPreds['NYY'], c='black', marker="o", label='NYY')
plt.plot(dates, ALEastPreds['TBR'], c='green', label='_nolegend_')
ax.scatter(dates, ALEastPreds['TBR'], c='green', marker="o", label='TBR')
plt.plot(dates, ALEastPreds['BAL'], c='orange', label='_nolegend_')
ax.scatter(dates, ALEastPreds['BAL'], c='orange', marker="o", label='BAL')
ax.legend(loc='best', frameon=False)
plt.title('AL East 2017 Bayesian Playoff Probabilities')
plt.ylabel('Playoff Probabilities')
plt.xlabel('')
ax.set_ylim(0, 1.05)
myFmt = mdates.DateFormatter('%B')
ax.xaxis.set_major_formatter(myFmt)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
fig.savefig('ALEast2017PlayoffOdds.png', bbox_inches='tight')

############################################################################

#Divisional Odds
#NL West
NLWestPreds = resultsDF[resultsDF.Teams.isin(NL_West)]
teamHeaders = NLWestPreds.Teams.values
playoffCols = NLWestPreds.columns[NLWestPreds.columns.str.startswith('DivisionOdds')]
NLWestPreds = NLWestPreds[playoffCols]
NLWestPreds = pd.DataFrame(np.transpose(NLWestPreds.values))
NLWestPreds.columns = teamHeaders
      
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
plt.plot(dates, NLWestPreds['LAD'], c='b', label='_nolegend_') 
ax.scatter(dates, NLWestPreds['LAD'], c='b', marker="o", label='LAD')
plt.plot(dates, NLWestPreds['ARI'], c='r', label='_nolegend_')
ax.scatter(dates, NLWestPreds['ARI'], c='r', marker="o", label='ARI')
plt.plot(dates, NLWestPreds['COL'], c='purple', label='_nolegend_')
ax.scatter(dates, NLWestPreds['COL'], c='purple', marker="o", label='COL')
plt.plot(dates, NLWestPreds['SDP'], c='green', label='_nolegend_')
ax.scatter(dates, NLWestPreds['SDP'], c='green', marker="o", label='SDP')
plt.plot(dates, NLWestPreds['SFG'], c='orange', label='_nolegend_')
ax.scatter(dates, NLWestPreds['SFG'], c='orange', marker="o", label='SFG')
ax.legend(loc='best', frameon=False)
plt.title('NL West 2017 Bayesian Division Probabilities')
plt.ylabel('Division Probabilities')
plt.xlabel('')
ax.set_ylim(0, 1.05)
myFmt = mdates.DateFormatter('%B')
ax.xaxis.set_major_formatter(myFmt)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
fig.savefig('NLWest2017DivisionOdds.png', bbox_inches='tight')

#NL Central
NLCentralPreds = resultsDF[resultsDF.Teams.isin(NL_Central)]
teamHeaders = NLCentralPreds.Teams.values
playoffCols = NLCentralPreds.columns[NLCentralPreds.columns.str.startswith('DivisionOdds')]
NLCentralPreds = NLCentralPreds[playoffCols]
NLCentralPreds = pd.DataFrame(np.transpose(NLCentralPreds.values))
NLCentralPreds.columns = teamHeaders
      
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
plt.plot(dates, NLCentralPreds['CHC'], c='b', label='_nolegend_') 
ax.scatter(dates, NLCentralPreds['CHC'], c='b', marker="o", label='CHC')
plt.plot(dates, NLCentralPreds['STL'], c='r', label='_nolegend_')
ax.scatter(dates, NLCentralPreds['STL'], c='r', marker="o", label='STL')
plt.plot(dates, NLCentralPreds['PIT'], c='black', label='_nolegend_')
ax.scatter(dates, NLCentralPreds['PIT'], c='black', marker="o", label='PIT')
plt.plot(dates, NLCentralPreds['MIL'], c='green', label='_nolegend_')
ax.scatter(dates, NLCentralPreds['MIL'], c='green', marker="o", label='MIL')
plt.plot(dates, NLCentralPreds['CIN'], c='orange', label='_nolegend_')
ax.scatter(dates, NLCentralPreds['CIN'], c='orange', marker="o", label='CIN')
ax.legend(loc='best', frameon=False)
plt.title('NL Central 2017 Bayesian Division Probabilities')
plt.ylabel('Division Probabilities')
plt.xlabel('')
ax.set_ylim(0, 1.05)
myFmt = mdates.DateFormatter('%B')
ax.xaxis.set_major_formatter(myFmt)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
fig.savefig('NLCentral2017DivisionOdds.png', bbox_inches='tight')

#NL East
NLEastPreds = resultsDF[resultsDF.Teams.isin(NL_East)]
teamHeaders = NLEastPreds.Teams.values
playoffCols = NLEastPreds.columns[NLEastPreds.columns.str.startswith('DivisionOdds')]
NLEastPreds = NLEastPreds[playoffCols]
NLEastPreds = pd.DataFrame(np.transpose(NLEastPreds.values))
NLEastPreds.columns = teamHeaders
      
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
plt.plot(dates, NLEastPreds['NYM'], c='b', label='_nolegend_') 
ax.scatter(dates, NLEastPreds['NYM'], c='b', marker="o", label='NYM')
plt.plot(dates, NLEastPreds['WSN'], c='r', label='_nolegend_')
ax.scatter(dates, NLEastPreds['WSN'], c='r', marker="o", label='WSN')
plt.plot(dates, NLEastPreds['PHI'], c='purple', label='_nolegend_')
ax.scatter(dates, NLEastPreds['PHI'], c='purple', marker="o", label='PHI')
plt.plot(dates, NLEastPreds['ATL'], c='green', label='_nolegend_')
ax.scatter(dates, NLEastPreds['ATL'], c='green', marker="o", label='ATL')
plt.plot(dates, NLEastPreds['MIA'], c='orange', label='_nolegend_')
ax.scatter(dates, NLEastPreds['MIA'], c='orange', marker="o", label='MIA')
ax.legend(loc='best', frameon=False)
plt.title('NL East 2017 Bayesian Division Probabilities')
plt.ylabel('Division Probabilities')
plt.xlabel('')
ax.set_ylim(0, 1.05)
myFmt = mdates.DateFormatter('%B')
ax.xaxis.set_major_formatter(myFmt)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
fig.savefig('NLEast2017DivisionOdds.png', bbox_inches='tight')

#AL West
ALWestPreds = resultsDF[resultsDF.Teams.isin(AL_West)]
teamHeaders = ALWestPreds.Teams.values
playoffCols = ALWestPreds.columns[ALWestPreds.columns.str.startswith('DivisionOdds')]
ALWestPreds = ALWestPreds[playoffCols]
ALWestPreds = pd.DataFrame(np.transpose(ALWestPreds.values))
ALWestPreds.columns = teamHeaders
      
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
plt.plot(dates, ALWestPreds['TEX'], c='b', label='_nolegend_') 
ax.scatter(dates, ALWestPreds['TEX'], c='b', marker="o", label='TEX')
plt.plot(dates, ALWestPreds['LAA'], c='r', label='_nolegend_')
ax.scatter(dates, ALWestPreds['LAA'], c='r', marker="o", label='LAA')
plt.plot(dates, ALWestPreds['SEA'], c='purple', label='_nolegend_')
ax.scatter(dates, ALWestPreds['SEA'], c='purple', marker="o", label='SEA')
plt.plot(dates, ALWestPreds['OAK'], c='green', label='_nolegend_')
ax.scatter(dates, ALWestPreds['OAK'], c='green', marker="o", label='OAK')
plt.plot(dates, ALWestPreds['HOU'], c='orange', label='_nolegend_')
ax.scatter(dates, ALWestPreds['HOU'], c='orange', marker="o", label='HOU')
ax.legend(loc='best', frameon=False)
plt.title('AL West 2017 Bayesian Division Probabilities')
plt.ylabel('Division Probabilities')
plt.xlabel('')
ax.set_ylim(0, 1.05)
myFmt = mdates.DateFormatter('%B')
ax.xaxis.set_major_formatter(myFmt)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
fig.savefig('ALWest2017DivisionOdds.png', bbox_inches='tight')

#AL Central
ALCentralPreds = resultsDF[resultsDF.Teams.isin(AL_Central)]
teamHeaders = ALCentralPreds.Teams.values
playoffCols = ALCentralPreds.columns[ALCentralPreds.columns.str.startswith('DivisionOdds')]
ALCentralPreds = ALCentralPreds[playoffCols]
ALCentralPreds = pd.DataFrame(np.transpose(ALCentralPreds.values))
ALCentralPreds.columns = teamHeaders
      
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
plt.plot(dates, ALCentralPreds['KCR'], c='b', label='_nolegend_') 
ax.scatter(dates, ALCentralPreds['KCR'], c='b', marker="o", label='KCR')
plt.plot(dates, ALCentralPreds['CLE'], c='r', label='_nolegend_')
ax.scatter(dates, ALCentralPreds['CLE'], c='r', marker="o", label='CLE')
plt.plot(dates, ALCentralPreds['CHW'], c='black', label='_nolegend_')
ax.scatter(dates, ALCentralPreds['CHW'], c='black', marker="o", label='CHW')
plt.plot(dates, ALCentralPreds['MIN'], c='green', label='_nolegend_')
ax.scatter(dates, ALCentralPreds['MIN'], c='green', marker="o", label='MIN')
plt.plot(dates, ALCentralPreds['DET'], c='orange', label='_nolegend_')
ax.scatter(dates, ALCentralPreds['DET'], c='orange', marker="o", label='DET')
ax.legend(loc='best', frameon=False)
plt.title('AL Central 2017 Bayesian Division Probabilities')
plt.ylabel('Division Probabilities')
plt.xlabel('')
ax.set_ylim(0, 1.05)
myFmt = mdates.DateFormatter('%B')
ax.xaxis.set_major_formatter(myFmt)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
fig.savefig('ALCentral2017DivisionOdds.png', bbox_inches='tight')

#AL East
ALEastPreds = resultsDF[resultsDF.Teams.isin(AL_East)]
teamHeaders = ALEastPreds.Teams.values
playoffCols = ALEastPreds.columns[ALEastPreds.columns.str.startswith('DivisionOdds')]
ALEastPreds = ALEastPreds[playoffCols]
ALEastPreds = pd.DataFrame(np.transpose(ALEastPreds.values))
ALEastPreds.columns = teamHeaders
      
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
plt.plot(dates, ALEastPreds['TOR'], c='b', label='_nolegend_') 
ax.scatter(dates, ALEastPreds['TOR'], c='b', marker="o", label='TOR')
plt.plot(dates, ALEastPreds['BOS'], c='r', label='_nolegend_')
ax.scatter(dates, ALEastPreds['BOS'], c='r', marker="o", label='BOS')
plt.plot(dates, ALEastPreds['NYY'], c='black', label='_nolegend_')
ax.scatter(dates, ALEastPreds['NYY'], c='black', marker="o", label='NYY')
plt.plot(dates, ALEastPreds['TBR'], c='green', label='_nolegend_')
ax.scatter(dates, ALEastPreds['TBR'], c='green', marker="o", label='TBR')
plt.plot(dates, ALEastPreds['BAL'], c='orange', label='_nolegend_')
ax.scatter(dates, ALEastPreds['BAL'], c='orange', marker="o", label='BAL')
ax.legend(loc='best', frameon=False)
plt.title('AL East 2017 Bayesian Division Probabilities')
plt.ylabel('Division Probabilities')
plt.xlabel('')
ax.set_ylim(0, 1.05)
myFmt = mdates.DateFormatter('%B')
ax.xaxis.set_major_formatter(myFmt)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
fig.savefig('ALEast2017DivisionOdds.png', bbox_inches='tight')

############################################################################

#WildCard Odds
#NL West
NLWestPreds = resultsDF[resultsDF.Teams.isin(NL_West)]
teamHeaders = NLWestPreds.Teams.values
playoffCols = NLWestPreds.columns[NLWestPreds.columns.str.startswith('WildCardOdds')]
NLWestPreds = NLWestPreds[playoffCols]
NLWestPreds = pd.DataFrame(np.transpose(NLWestPreds.values))
NLWestPreds.columns = teamHeaders
      
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
plt.plot(dates, NLWestPreds['LAD'], c='b', label='_nolegend_') 
ax.scatter(dates, NLWestPreds['LAD'], c='b', marker="o", label='LAD')
plt.plot(dates, NLWestPreds['ARI'], c='r', label='_nolegend_')
ax.scatter(dates, NLWestPreds['ARI'], c='r', marker="o", label='ARI')
plt.plot(dates, NLWestPreds['COL'], c='purple', label='_nolegend_')
ax.scatter(dates, NLWestPreds['COL'], c='purple', marker="o", label='COL')
plt.plot(dates, NLWestPreds['SDP'], c='green', label='_nolegend_')
ax.scatter(dates, NLWestPreds['SDP'], c='green', marker="o", label='SDP')
plt.plot(dates, NLWestPreds['SFG'], c='orange', label='_nolegend_')
ax.scatter(dates, NLWestPreds['SFG'], c='orange', marker="o", label='SFG')
ax.legend(loc='best', frameon=False)
plt.title('NL West 2017 Bayesian WildCard Probabilities')
plt.ylabel('WildCard Probabilities')
plt.xlabel('')
ax.set_ylim(0, 1.05)
myFmt = mdates.DateFormatter('%B')
ax.xaxis.set_major_formatter(myFmt)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
fig.savefig('NLWest2017WildCardOdds.png', bbox_inches='tight')

#NL Central
NLCentralPreds = resultsDF[resultsDF.Teams.isin(NL_Central)]
teamHeaders = NLCentralPreds.Teams.values
playoffCols = NLCentralPreds.columns[NLCentralPreds.columns.str.startswith('WildCardOdds')]
NLCentralPreds = NLCentralPreds[playoffCols]
NLCentralPreds = pd.DataFrame(np.transpose(NLCentralPreds.values))
NLCentralPreds.columns = teamHeaders
      
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
plt.plot(dates, NLCentralPreds['CHC'], c='b', label='_nolegend_') 
ax.scatter(dates, NLCentralPreds['CHC'], c='b', marker="o", label='CHC')
plt.plot(dates, NLCentralPreds['STL'], c='r', label='_nolegend_')
ax.scatter(dates, NLCentralPreds['STL'], c='r', marker="o", label='STL')
plt.plot(dates, NLCentralPreds['PIT'], c='black', label='_nolegend_')
ax.scatter(dates, NLCentralPreds['PIT'], c='black', marker="o", label='PIT')
plt.plot(dates, NLCentralPreds['MIL'], c='green', label='_nolegend_')
ax.scatter(dates, NLCentralPreds['MIL'], c='green', marker="o", label='MIL')
plt.plot(dates, NLCentralPreds['CIN'], c='orange', label='_nolegend_')
ax.scatter(dates, NLCentralPreds['CIN'], c='orange', marker="o", label='CIN')
ax.legend(loc='best', frameon=False)
plt.title('NL Central 2017 Bayesian WildCard Probabilities')
plt.ylabel('WildCard Probabilities')
plt.xlabel('')
ax.set_ylim(0, 1.05)
myFmt = mdates.DateFormatter('%B')
ax.xaxis.set_major_formatter(myFmt)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
fig.savefig('NLCentral2017WildCardOdds.png', bbox_inches='tight')

#NL East
NLEastPreds = resultsDF[resultsDF.Teams.isin(NL_East)]
teamHeaders = NLEastPreds.Teams.values
playoffCols = NLEastPreds.columns[NLEastPreds.columns.str.startswith('WildCardOdds')]
NLEastPreds = NLEastPreds[playoffCols]
NLEastPreds = pd.DataFrame(np.transpose(NLEastPreds.values))
NLEastPreds.columns = teamHeaders
      
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
plt.plot(dates, NLEastPreds['NYM'], c='b', label='_nolegend_') 
ax.scatter(dates, NLEastPreds['NYM'], c='b', marker="o", label='NYM')
plt.plot(dates, NLEastPreds['WSN'], c='r', label='_nolegend_')
ax.scatter(dates, NLEastPreds['WSN'], c='r', marker="o", label='WSN')
plt.plot(dates, NLEastPreds['PHI'], c='purple', label='_nolegend_')
ax.scatter(dates, NLEastPreds['PHI'], c='purple', marker="o", label='PHI')
plt.plot(dates, NLEastPreds['ATL'], c='green', label='_nolegend_')
ax.scatter(dates, NLEastPreds['ATL'], c='green', marker="o", label='ATL')
plt.plot(dates, NLEastPreds['MIA'], c='orange', label='_nolegend_')
ax.scatter(dates, NLEastPreds['MIA'], c='orange', marker="o", label='MIA')
ax.legend(loc='best', frameon=False)
plt.title('NL East 2017 Bayesian WildCard Probabilities')
plt.ylabel('WildCard Probabilities')
plt.xlabel('')
ax.set_ylim(0, 1.05)
myFmt = mdates.DateFormatter('%B')
ax.xaxis.set_major_formatter(myFmt)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
fig.savefig('NLEast2017WildCardOdds.png', bbox_inches='tight')

#AL West
ALWestPreds = resultsDF[resultsDF.Teams.isin(AL_West)]
teamHeaders = ALWestPreds.Teams.values
playoffCols = ALWestPreds.columns[ALWestPreds.columns.str.startswith('WildCardOdds')]
ALWestPreds = ALWestPreds[playoffCols]
ALWestPreds = pd.DataFrame(np.transpose(ALWestPreds.values))
ALWestPreds.columns = teamHeaders
      
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
plt.plot(dates, ALWestPreds['TEX'], c='b', label='_nolegend_') 
ax.scatter(dates, ALWestPreds['TEX'], c='b', marker="o", label='TEX')
plt.plot(dates, ALWestPreds['LAA'], c='r', label='_nolegend_')
ax.scatter(dates, ALWestPreds['LAA'], c='r', marker="o", label='LAA')
plt.plot(dates, ALWestPreds['SEA'], c='purple', label='_nolegend_')
ax.scatter(dates, ALWestPreds['SEA'], c='purple', marker="o", label='SEA')
plt.plot(dates, ALWestPreds['OAK'], c='green', label='_nolegend_')
ax.scatter(dates, ALWestPreds['OAK'], c='green', marker="o", label='OAK')
plt.plot(dates, ALWestPreds['HOU'], c='orange', label='_nolegend_')
ax.scatter(dates, ALWestPreds['HOU'], c='orange', marker="o", label='HOU')
ax.legend(loc='best', frameon=False)
plt.title('AL West 2017 Bayesian WildCard Probabilities')
plt.ylabel('WildCard Probabilities')
plt.xlabel('')
ax.set_ylim(0, 1.05)
myFmt = mdates.DateFormatter('%B')
ax.xaxis.set_major_formatter(myFmt)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
fig.savefig('ALWest2017WildCardOdds.png', bbox_inches='tight')

#AL Central
ALCentralPreds = resultsDF[resultsDF.Teams.isin(AL_Central)]
teamHeaders = ALCentralPreds.Teams.values
playoffCols = ALCentralPreds.columns[ALCentralPreds.columns.str.startswith('WildCardOdds')]
ALCentralPreds = ALCentralPreds[playoffCols]
ALCentralPreds = pd.DataFrame(np.transpose(ALCentralPreds.values))
ALCentralPreds.columns = teamHeaders
      
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
plt.plot(dates, ALCentralPreds['KCR'], c='b', label='_nolegend_') 
ax.scatter(dates, ALCentralPreds['KCR'], c='b', marker="o", label='KCR')
plt.plot(dates, ALCentralPreds['CLE'], c='r', label='_nolegend_')
ax.scatter(dates, ALCentralPreds['CLE'], c='r', marker="o", label='CLE')
plt.plot(dates, ALCentralPreds['CHW'], c='black', label='_nolegend_')
ax.scatter(dates, ALCentralPreds['CHW'], c='black', marker="o", label='CHW')
plt.plot(dates, ALCentralPreds['MIN'], c='green', label='_nolegend_')
ax.scatter(dates, ALCentralPreds['MIN'], c='green', marker="o", label='MIN')
plt.plot(dates, ALCentralPreds['DET'], c='orange', label='_nolegend_')
ax.scatter(dates, ALCentralPreds['DET'], c='orange', marker="o", label='DET')
ax.legend(loc='best', frameon=False)
plt.title('AL Central 2017 Bayesian WildCard Probabilities')
plt.ylabel('WildCard Probabilities')
plt.xlabel('')
ax.set_ylim(0, 1.05)
myFmt = mdates.DateFormatter('%B')
ax.xaxis.set_major_formatter(myFmt)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
fig.savefig('ALCentral2017WildCardOdds.png', bbox_inches='tight')

#AL East
ALEastPreds = resultsDF[resultsDF.Teams.isin(AL_East)]
teamHeaders = ALEastPreds.Teams.values
playoffCols = ALEastPreds.columns[ALEastPreds.columns.str.startswith('WildCardOdds')]
ALEastPreds = ALEastPreds[playoffCols]
ALEastPreds = pd.DataFrame(np.transpose(ALEastPreds.values))
ALEastPreds.columns = teamHeaders
      
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
plt.plot(dates, ALEastPreds['TOR'], c='b', label='_nolegend_') 
ax.scatter(dates, ALEastPreds['TOR'], c='b', marker="o", label='TOR')
plt.plot(dates, ALEastPreds['BOS'], c='r', label='_nolegend_')
ax.scatter(dates, ALEastPreds['BOS'], c='r', marker="o", label='BOS')
plt.plot(dates, ALEastPreds['NYY'], c='black', label='_nolegend_')
ax.scatter(dates, ALEastPreds['NYY'], c='black', marker="o", label='NYY')
plt.plot(dates, ALEastPreds['TBR'], c='green', label='_nolegend_')
ax.scatter(dates, ALEastPreds['TBR'], c='green', marker="o", label='TBR')
plt.plot(dates, ALEastPreds['BAL'], c='orange', label='_nolegend_')
ax.scatter(dates, ALEastPreds['BAL'], c='orange', marker="o", label='BAL')
ax.legend(loc='best', frameon=False)
plt.title('AL East 2017 Bayesian WildCard Probabilities')
plt.ylabel('WildCard Probabilities')
plt.xlabel('')
ax.set_ylim(0, 1.05)
myFmt = mdates.DateFormatter('%B')
ax.xaxis.set_major_formatter(myFmt)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
fig.savefig('ALEast2017WildCardOdds.png', bbox_inches='tight')



#######################################################################
#Playoff Odds

resultsDF = pd.read_csv("mlb2017PlayoffPreds.csv")

#import plotly
#plotly.tools.set_credentials_file(username='adbooth01', api_key='ve7oQUzY6m1OXXj9SL1i')

#import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
import datetime

dates = []
start_date = date(2017, 4, 1)
end_date = date(2017, 10, 2)
for single_date in daterange(start_date, end_date):
    dates.append(single_date)
    
def to_unix_time(dt):
    epoch =  datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000

#https://teamcolorcodes.com/mlb-color-codes/
teamColors = dict([('LAD', 'rgb(0,90,156)'), ('ARI', 'rgb(167,25,48)'), ('COL', 'rgb(51,0,111)'),
                   ('SDP', 'rgb(255,199,44)'), ('SFG', 'rgb(253,90,30)'), ('CHC', 'rgb(14,51,134)'),
                   ('STL', 'rgb(196,30,58)'), ('MIL', 'rgb(19,41,75)'), ('PIT', 'rgb(253,184,39)'),
                   ('CIN', 'rgb(198,1,31)'), ('WSN', 'rgb(171,0,3)'), ('PHI', 'rgb(232,24,40)'),
                   ('ATL', 'rgb(19, 39, 79)'), ('MIA', 'rgb(255,102,0)'), ('NYM', 'rgb(0,45, 114)'),
                   ('TEX', 'rgb(0,50,120)'), ('HOU', 'rgb(235,110,31)'), ('LAA', 'rgb(186,0,33)'),
                   ('SEA', 'rgb(0,92,92)'), ('OAK', 'rgb(0,56,49)'), ('CLE', 'rgb(227,25,55)'),
                   ('DET', 'rgb(250,70,22)'), ('KCR', 'rgb(0,70,135)'), ('MIN', 'rgb(0,43,92)'),
                   ('CHW', 'rgb(39,37,31)'), ('NYY', 'rgb(12,35,64)'), ('BOS', 'rgb(189, 48, 57)'),
                   ('BAL', 'rgb(223,70,1)'), ('TBR', 'rgb(143,188,230)'), ('TOR', 'rgb(19,74,142)')])

#Division Aggregate - 24 plots
divNames = ['AL_West', 'AL_Central', 'AL_East', 'NL_West', 'NL_Central', 'NL_East']
dataTypes = ['Playoff', 'Division', 'WildCard', 'ExpectedWins']
i=0
for league in DivisionsLeague:
    for division in league:
        for dataType in dataTypes:
            dataToPlot = resultsDF[resultsDF.Teams.isin(division)]
            teamHeaders = dataToPlot.Teams.values
            cols = dataToPlot.columns[dataToPlot.columns.str.startswith(dataType)]
            dataToPlot = dataToPlot[cols]
            dataToPlot = pd.DataFrame(np.transpose(dataToPlot.values))
            dataToPlot.columns = teamHeaders
            
            divisionName = divNames[i]
            
            if dataType != 'ExpectedWins':
                plotTitle = divisionName + ' 2017 Bayesian ' + dataType + ' Probabilities'
                yLabel = dataType + ' Probability'
                fileName = divisionName + '_2017_' + dataType + '_Probs'
                yStart = 0
                yEnd = 1.05
                hoverFormat = '.2f'
            else:
                plotTitle = divisionName + ' 2017 Bayesian Expected Wins'
                yLabel = "Expected Wins"
                fileName = divisionName + '_2017_' + dataType
                yStart = 50
                yEnd = 120
                hoverFormat = '.0f'
                
            x = dates
            data = []
            for teamAbbr in teamHeaders:
                trace = go.Scatter(
                        x=x,
                        y=dataToPlot[teamAbbr],
                        mode='lines+markers',
                        name = teamAbbr,
                        line = dict(
                                color = teamColors[teamAbbr],
                                width = 4,
                                shape='linear'))
            
                data.append(trace)
                layout = go.Layout(
                    title = plotTitle,
                    yaxis = dict(title = yLabel,
                                 range = [yStart, yEnd],
                                 hoverformat = hoverFormat),
                    xaxis = dict(title = '',
                               range = [to_unix_time(datetime.datetime(2017, 4, 1)),
                                        to_unix_time(datetime.datetime(2017, 10, 2))]))
            
            fig = go.Figure(data = data, layout = layout)
            offline.plot(fig, filename = fileName + '.html')
        i += 1

#League Aggregate - 8 plots
leagueNames = ['American League', 'National League']
i=0
for league in LeagueTeams:
    for dataType in dataTypes:
        dataToPlot = resultsDF[resultsDF.Teams.isin(league)]
        teamHeaders = dataToPlot.Teams.values
        cols = dataToPlot.columns[dataToPlot.columns.str.startswith(dataType)]
        dataToPlot = dataToPlot[cols]
        dataToPlot = pd.DataFrame(np.transpose(dataToPlot.values))
        dataToPlot.columns = teamHeaders
        
        leagueName = leagueNames[i]
            
        if dataType != 'ExpectedWins':
            plotTitle = leagueName + ' 2017 Bayesian ' + dataType + ' Probabilities'
            yLabel = dataType + ' Probability'
            fileName = leagueName + '_2017_' + dataType + '_Probs'
            yStart = 0
            yEnd = 1.05
            hoverFormat = '.2f'
        else:
            plotTitle = leagueName + ' 2017 Bayesian Expected Wins'
            yLabel = "Expected Wins"
            fileName = leagueName + '_2017_' + dataType
            yStart = 50
            yEnd = 120
            hoverFormat = '.0f'
            
        x = dates
        data = []
        for teamAbbr in teamHeaders:
            trace = go.Scatter(
                    x=x,
                    y=dataToPlot[teamAbbr],
                    mode='lines+markers',
                    name = teamAbbr,
                    line = dict(
                            color = teamColors[teamAbbr],
                            width = 4,
                            shape='linear'))
        
            data.append(trace)
            layout = go.Layout(
                title = plotTitle,
                yaxis = dict(title = yLabel,
                             range = [yStart, yEnd],
                             hoverformat = hoverFormat),
                xaxis = dict(title = '',
                           range = [to_unix_time(datetime.datetime(2017, 4, 1)),
                                    to_unix_time(datetime.datetime(2017, 10, 2))]))
        
        fig = go.Figure(data = data, layout = layout)
        offline.plot(fig, filename = fileName + '.html')
    i += 1

#Level Aggregate - 4 plots
levNames = ['MLB']
i=0
for dataType in dataTypes:
    dataToPlot = resultsDF
    teamHeaders = dataToPlot.Teams.values
    cols = dataToPlot.columns[dataToPlot.columns.str.startswith(dataType)]
    dataToPlot = dataToPlot[cols]
    dataToPlot = pd.DataFrame(np.transpose(dataToPlot.values))
    dataToPlot.columns = teamHeaders
    
    levName = levNames[i]
        
    if dataType != 'ExpectedWins':
        plotTitle = levName + ' 2017 Bayesian ' + dataType + ' Probabilities'
        yLabel = dataType + ' Probability'
        fileName = levName + '_2017_' + dataType + '_Probs'
        yStart = 0
        yEnd = 1.05
        hoverFormat = '.2f'
    else:
        plotTitle = levName + ' 2017 Bayesian Expected Wins'
        yLabel = "Expected Wins"
        fileName = levName + '_2017_' + dataType
        yStart = 50
        yEnd = 120
        hoverFormat = '.0f'
        
    x = dates
    data = []
    for teamAbbr in teamHeaders:
        trace = go.Scatter(
                x=x,
                y=dataToPlot[teamAbbr],
                mode='lines+markers',
                name = teamAbbr,
                line = dict(
                        color = teamColors[teamAbbr],
                        width = 4,
                        shape='linear'))
    
        data.append(trace)
        layout = go.Layout(
            title = plotTitle,
            yaxis = dict(title = yLabel,
                         range = [yStart, yEnd],
                         hoverformat = hoverFormat),
            xaxis = dict(title = '',
                       range = [to_unix_time(datetime.datetime(2017, 4, 1)),
                                to_unix_time(datetime.datetime(2017, 10, 2))]))
    
    fig = go.Figure(data = data, layout = layout)
    offline.plot(fig, filename = fileName + '.html')
