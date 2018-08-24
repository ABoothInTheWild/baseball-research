# -*- coding: utf-8 -*-
"""
Created on Sun Aug 05 22:49:05 2018

@author: Alexander
"""

#2018 Preseason Playoff Odds
import heapq
from collections import Counter
import pandas as pd
import numpy as np
from scipy.stats import beta
import os

#read data
os.chdir('C:/Users/abooth/Documents/Python Scripts/PastPreds/mlbPlayoffOdds2018')
beta18Pre = pd.read_csv("mlb2018PreSeasonBetaEstimates.csv")

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
            alphaEst = beta18Pre[beta18Pre.Team_Abbr == team]["PriorAlpha"].values[0]
            betaEst = beta18Pre[beta18Pre.Team_Abbr == team]["PriorBeta"].values[0]
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
resultsDF["DivisionOdds20180328"] = divOdds
resultsDF["WildCardOdds20180328"] = wcOdds
resultsDF["PlayoffOdds20180328"] = resultsDF.DivisionOdds20180328 + resultsDF.WildCardOdds20180328 
resultsDF["ExpectedWins20180328"] = expectedWins

#Attach point win estimates and confidence itervals
#resultsDF = resultsDF.sort_values(by=["Teams"]).reset_index(drop=True)
#beta18PreSorted = beta18Pre.sort_values(by=["Team_Abbr"]).reset_index(drop=True)
#resultsDF_Full = pd.concat([resultsDF, beta18PreSorted.iloc[:,19:37]], axis=1)

#resultsDF.to_csv("mlb2017PreseasonPlayoffPreds.csv", index=False)
###############################################################################

#Create playoff odds per day per prior per team

#read data downloaded from xmlStats API
mlb18Results = pd.read_csv("mlb2018SeasonResults.csv")

from datetime import timedelta, date
#https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

dates = []
start_date = date(2018, 3, 29)
end_date = date(2018, 8, 24)
for single_date in daterange(start_date, end_date):
    dates.append(single_date.strftime("%Y%m%d"))
    
dateLen = len(dates)
 
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
                priorA = beta18Pre[beta18Pre.Team_Abbr == team]["PriorAlpha"].values[0]
                priorB = beta18Pre[beta18Pre.Team_Abbr == team]["PriorBeta"].values[0]
                #get posteriors
                team18Res = mlb18Results[mlb18Results.Team_Abbr==team].iloc[:,2:((2*dateLen)+2)]
                teamWins = team18Res.iloc[:,range(0,(2*dateLen),2)].values[0]
                teamLosses = team18Res.iloc[:,range(1,(2*dateLen)+1,2)].values[0]
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
    
resultsDF.to_csv("mlb2018PlayoffPreds.csv", index=False)

#######################################################################

#Playoff Odds

resultsDF = pd.read_csv("mlb2018PlayoffPreds.csv")

#import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
import datetime

dates = []
start_date = date(2018, 3, 28)
end_date = date(2018, 8, 24)
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
            
            if 'AL' in divisionName:
                fileNamePrefix = '/HTML/Division/AL/'
            else:
                fileNamePrefix = '/HTML/Division/NL/'
            
            if dataType != 'ExpectedWins':
                plotTitle = divisionName + ' 2018 Bayesian ' + dataType + ' Probabilities'
                yLabel = dataType + ' Probability'
                fileName = os.getcwd() + fileNamePrefix + divisionName + '_2018_' + dataType + '_Probs'
                yStart = 0
                yEnd = 1.05
                hoverFormat = '.2f'
            else:
                plotTitle = divisionName + ' 2018 Bayesian Expected Wins'
                yLabel = "Expected Wins"
                fileName = os.getcwd() + fileNamePrefix + divisionName + '_2018_' + dataType
                yStart = 45
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
                               range = [to_unix_time(datetime.datetime(2018, 3, 28)),
                                        to_unix_time(datetime.datetime(2018, 8, 24))]))
            
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
        
        if 'American' in leagueName:
            fileNamePrefix = '/HTML/League/AL/'
        else:
            fileNamePrefix = '/HTML/League/NL/'
            
        if dataType != 'ExpectedWins':
            plotTitle = leagueName + ' 2018 Bayesian ' + dataType + ' Probabilities'
            yLabel = dataType + ' Probability'
            fileName = os.getcwd() + fileNamePrefix + leagueName + '_2018_' + dataType + '_Probs'
            yStart = 0
            yEnd = 1.05
            hoverFormat = '.2f'
        else:
            plotTitle = leagueName + ' 2018 Bayesian Expected Wins'
            yLabel = "Expected Wins"
            fileName = os.getcwd() + fileNamePrefix + leagueName + '_2018_' + dataType
            yStart = 45
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
                           range = [to_unix_time(datetime.datetime(2018, 3, 28)),
                                    to_unix_time(datetime.datetime(2018, 8, 24))]))
        
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
    fileNamePrefix = '/HTML/Level/'
        
    if dataType != 'ExpectedWins':
        plotTitle = levName + ' 2018 Bayesian ' + dataType + ' Probabilities'
        yLabel = dataType + ' Probability'
        fileName = os.getcwd() + fileNamePrefix + levName + '_2018_' + dataType + '_Probs'
        yStart = 0
        yEnd = 1.05
        hoverFormat = '.2f'
    else:
        plotTitle = levName + ' 2018 Bayesian Expected Wins'
        yLabel = "Expected Wins"
        fileName = os.getcwd() + fileNamePrefix + levName + '_2018_' + dataType
        yStart = 45
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
                       range = [to_unix_time(datetime.datetime(2018, 3, 28)),
                                to_unix_time(datetime.datetime(2018, 8, 24))]))
    
    fig = go.Figure(data = data, layout = layout)
    offline.plot(fig, filename = fileName + '.html')



########################################################

dates = []
start_date = date(2018, 3, 29)
end_date = date(2018, 8, 24)
for single_date in daterange(start_date, end_date):
    dates.append(single_date.strftime("%Y%m%d"))
    
dateLen = len(dates)

team = "KCR"
ntrials=100000
np.random.seed(seed=54321)

i = dateLen - 1

priorA = beta18Pre[beta18Pre.Team_Abbr == team]["PriorAlpha"].values[0]
priorB = beta18Pre[beta18Pre.Team_Abbr == team]["PriorBeta"].values[0]
#get posteriors
team18Res = mlb18Results[mlb18Results.Team_Abbr==team].iloc[:,2:((2*dateLen)+2)]
teamWins = team18Res.iloc[:,range(0,(2*dateLen),2)].values[0]
teamLosses = team18Res.iloc[:,range(1,(2*dateLen)+1,2)].values[0]
posteriorAlpha = priorA + teamWins[i]
posteriorBeta = priorB + teamLosses[i]    

#where the magic happens
sample = beta.rvs(posteriorAlpha, posteriorBeta, size=ntrials)
gamesLeft = 162 - teamWins[i] - teamLosses[i]
winEstimate = np.round(teamWins[i] + sample*gamesLeft,0)
print(np.mean(winEstimate))
print(np.percentile(winEstimate, 2.5))
print(np.percentile(winEstimate, 97.5))


######################################################################

#init contstants
team = "BOS"
ntrials=100000
np.random.seed(seed=54321)

priorA = beta18Pre[beta18Pre.Team_Abbr == team]["PriorAlpha"].values[0]
priorB = beta18Pre[beta18Pre.Team_Abbr == team]["PriorBeta"].values[0]
#get posteriors
team18Res = mlb18Results[mlb18Results.Team_Abbr==team].iloc[:,2:((2*dateLen)+2)]
teamWins = team18Res.iloc[:,range(0,(2*dateLen),2)].values[0]
teamLosses = team18Res.iloc[:,range(1,(2*dateLen)+1,2)].values[0]
posteriorAlpha = priorA + teamWins[i]
posteriorBeta = priorB + teamLosses[i]
#where the magic happens
sample = beta.rvs(posteriorAlpha, posteriorBeta, size=ntrials)
gamesLeft = 162 - teamWins[i] - teamLosses[i]
sampleWins = np.round(teamWins[i] + sample*gamesLeft,0)
prob = len(sampleWins[sampleWins >= 116])/float(ntrials)
print(prob)