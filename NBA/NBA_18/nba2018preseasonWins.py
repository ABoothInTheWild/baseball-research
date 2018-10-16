# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 14:28:39 2018

@author: ABooth
"""

#Imports
import pandas as pd
import os
import numpy as np
from scipy.stats import beta

os.chdir('C:/Users/abooth/Documents/Python Scripts/NBA/NBA_18/')

#Load Data
nba18Pre = pd.read_csv('nba_2018_preseasonWins.csv')

#Get columns
cols = nba18Pre.columns
expEstimatesCols = list(cols[2:11])

##########################################################################

#Reference:
#https://stats.stackexchange.com/questions/12232/calculating-the-parameters-of-a-beta-distribution-using-the-mean-and-variance
def estimateBetaParams(mu, var):
  alpha = ((1 - mu) / var - 1 / mu) * mu ** 2 
  beta = alpha * (1 / mu - 1)
  return({'alpha':alpha, 'beta':beta})
  
from datetime import timedelta, date, datetime
#https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

##########################################################################

totalGames = 82

#Get personal games to regress by
preWinPerc = nba18Pre["Expert_Median"]/totalGames
luckSD = np.sqrt((preWinPerc * (1-preWinPerc))/totalGames)
med5YrSD = np.median(pd.DataFrame(nba18Pre[cols[11:16]]/totalGames).std(axis=1))

talentVar = med5YrSD**2 - luckSD**2
regressedGames = (preWinPerc * (1-preWinPerc))/talentVar

print(np.allclose(np.sqrt((preWinPerc * (1-preWinPerc))/
                  regressedGames), np.sqrt(talentVar))) #TRUE

#get personalized priors
priorAlphas = regressedGames * preWinPerc
priorBetas = regressedGames * (1-preWinPerc)

#Method of Moments - using regressedGames is an estimator for this method
estParms = [estimateBetaParams(preWinPerc[i], talentVar[i]) for i in range(len(preWinPerc))]
priorAlphas2 = pd.Series([x['alpha'] for x in estParms])
priorBetas2 = pd.Series([x['beta'] for x in estParms])

print(np.mean(regressedGames)) #38.8
print(np.mean(priorAlphas - priorAlphas2)) #0.5
print(np.mean(priorBetas - priorBetas2)) #0.5 Small difference, but not negligible

nba18Pre["PriorAlpha"] = priorAlphas2
nba18Pre["PriorBeta"] = priorBetas2

##########################################################################

#init lists
winPercBeta = []
ci80Low = []
ci80High = []
ci90Low = []
ci90High = []
ci95Low = []
ci95High = []
ci99Low = []
ci99High = []

#reset seed, loop through each team, create beta distribution, get samples
#get stats and quantiles from samples.
np.random.seed(seed=12345)
for team in nba18Pre.Abbr.values:
    priorA = nba18Pre[nba18Pre.Abbr == team]["PriorAlpha"].values[0]
    priorB = nba18Pre[nba18Pre.Abbr == team]["PriorBeta"].values[0]
    
    r = beta.rvs(priorA, priorB, size=100000)
    winPercBeta.append(np.mean(r))
    ci80Low.append(np.percentile(r, 10))
    ci80High.append(np.percentile(r, 90))
    ci90Low.append(np.percentile(r, 5))
    ci90High.append(np.percentile(r, 95))
    ci95Low.append(np.percentile(r, 2.5))
    ci95High.append(np.percentile(r, 97.5))
    ci99Low.append(np.percentile(r, 0.5))
    ci99High.append(np.percentile(r, 99.5))

#Throw lists into the dataframe
nba18Pre["Beta_Estimate"] = winPercBeta
nba18Pre["80CI_Low"] = ci80Low
nba18Pre["80CI_High"] = ci80High
nba18Pre["90CI_Low"] = ci90Low
nba18Pre["90CI_High"] = ci90High
nba18Pre["95CI_Low"] = ci95Low
nba18Pre["95CI_High"] = ci95High
nba18Pre["99CI_Low"] = ci99Low
nba18Pre["99CI_High"] = ci99High

#turn win percentages into regular season win estimates
nba18Pre["Beta_Wins"] = np.round(nba18Pre.Beta_Estimate * totalGames,1)

nba18Pre["80CI_Low_Wins"] = np.round(nba18Pre["80CI_Low"] * totalGames,1)
nba18Pre["80CI_High_Wins"] = np.round(nba18Pre["80CI_High"] * totalGames,1)
nba18Pre["90CI_Low_Wins"] = np.round(nba18Pre["90CI_Low"] * totalGames,1)
nba18Pre["90CI_High_Wins"] = np.round(nba18Pre["90CI_High"] * totalGames,1)
nba18Pre["95CI_Low_Wins"] = np.round(nba18Pre["95CI_Low"] * totalGames,1)
nba18Pre["95CI_High_Wins"] = np.round(nba18Pre["95CI_High"] * totalGames,1)
nba18Pre["99CI_Low_Wins"] = np.round(nba18Pre["99CI_Low"] * totalGames,1)
nba18Pre["99CI_High_Wins"] = np.round(nba18Pre["99CI_High"] * totalGames,1)
         
#nba18Pre.to_csv("nba2018PreSeasonBetaEstimates.csv", index=False)

##############################################################################

#2018 Playoff Odds
    
import heapq
from collections import Counter

#read data downloaded from xmlStats API
nba18Pre = pd.read_csv("nba2018PreSeasonBetaEstimates.csv")
#nba18Results = pd.read_csv("nba2018SeasonResults.csv")

#Name Conferences
Eastern = ["TOR", "BOS", "PHI", "CLE", "IND", "MIA", "MIL", "WAS", "DET", "CHA", "NYK", "BRO", "CHI", "ORL", "ATL"]
Western = ["HOU", "GSW", "POR", "OKC", "UTH", "NOP", "SAN", "MIN", "DEN", "LAC", "LAK", "SAC", "DAL", "MEM", "PHO"]
Conferences = [Western, Eastern]

#init Odds arrays
resultsDF = pd.DataFrame()
teams = []
confOdds = []
expectedWins = []

ntrials=100000

np.random.seed(seed=54321)
for conference in Conferences:
    #Init playoff counters per league
    results = Counter({0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0
                     , 10: 0, 11: 0, 12: 0, 13: 0, 14: 0})
    tempResults = []
    for team in conference:
        alphaEst = nba18Pre[nba18Pre.Abbr == team]["PriorAlpha"].values[0]
        betaEst = nba18Pre[nba18Pre.Abbr == team]["PriorBeta"].values[0]
        sample = beta.rvs(alphaEst, betaEst, size=ntrials)
        tempResults.append(np.round(sample*82,0))
        expectedWins.append(np.round(np.mean(sample*82),0))
        teams.append(team)
    #find playoff teams   
    tempResults = np.array(tempResults)
    argMaxesIndx = [heapq.nlargest(8, range(len(tempResults[:,i])), 
                    key=tempResults[:,i].__getitem__) 
                    for i in range(np.size(tempResults,1))]
    results.update(np.array(argMaxesIndx).flatten())
    confOdds.extend(np.array(list(results.values()))/float(ntrials))
          
resultsDF["Teams"] = teams
resultsDF["PlayoffOdds20181015"] = confOdds
resultsDF["ExpectedWins20181015"] = expectedWins

#resultsDF.to_csv("nba2018PlayoffPreds.csv", index=False)

#######################################################################

#Playoff Odds

resultsDF = pd.read_csv("nba2018PlayoffPreds.csv")

#import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
import datetime

dates = []
start_date = date(2018, 10, 15)
end_date = date(2018, 10, 16)
for single_date in daterange(start_date, end_date):
    dates.append(single_date)
    
def to_unix_time(dt):
    epoch =  datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000

#https://teamcolorcodes.com/nba-team-color-codes/
teamColors = dict([('ATL', 'rgb(225,68,52)'), ('IND', 'rgb(253,187,48)'), ('ORL', 'rgb(196,25,34)'),
                   ('BOS', 'rgb(0,122,51)'), ('LAC', 'rgb(200,16,46)'), ('PHI', 'rgb(0,107,182)'),
                   ('BRO', 'rgb(0,0,0)'), ('LAK', 'rgb(85,37,130)'), ('PHO', 'rgb(29,17,96)'),
                   ('CHA', 'rgb(29,17,96)'), ('MEM', 'rgb(93,118,169)'), ('POR', 'rgb(224,58,62)'),
                   ('CHI', 'rgb(206,17,65)'), ('MIA', 'rgb(152,0,46)'), ('SAC', 'rgb(91,43,130)'),
                   ('CLE', 'rgb(111,38,61)'), ('MIL', 'rgb(0,71,27)'), ('SAN', 'rgb(196,206,211)'),
                   ('DAL', 'rgb(0,83,188)'), ('MIN', 'rgb(120,190,32)'), ('TOR', 'rgb(206,17,65)'),
                   ('DET', 'rgb(29,66,138)'), ('NOP', 'rgb(180,151,90)'), ('UTH', 'rgb(0,43,92)'),
                   ('GSW', 'rgb(253,185,39)'), ('NYK', 'rgb(245,132,38)'), ('WAS', 'rgb(0,43,92)'),
                   ('HOU', 'rgb(206,17,65)'), ('OKC', 'rgb(0,125,195)'), ('DEN', 'rgb(13,34,64)')])

dataTypes = ['Playoff', 'ExpectedWins']

#League Aggregate - 4 plots
leagueNames = ['Western_Conference', 'Eastern_Conference']
i=0
for league in Conferences:
    for dataType in dataTypes:
        dataToPlot = resultsDF[resultsDF.Teams.isin(league)]
        teamHeaders = dataToPlot.Teams.values
        cols = dataToPlot.columns[dataToPlot.columns.str.startswith(dataType)]
        dataToPlot = dataToPlot[cols]
        dataToPlot = pd.DataFrame(np.transpose(dataToPlot.values))
        dataToPlot.columns = teamHeaders
        
        leagueName = leagueNames[i]
        
        if 'Western' in leagueName:
            fileNamePrefix = '/HTML/Conference/Western/'
        else:
            fileNamePrefix = '/HTML/Conference/Eastern/'
            
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
            yStart = 0
            yEnd = 75
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
                           range = [to_unix_time(datetime.datetime(2018, 10, 15)),
                                    to_unix_time(datetime.datetime(2018, 10, 16))]))
        
        fig = go.Figure(data = data, layout = layout)
        offline.plot(fig, filename = fileName + '.html')
    i += 1

#Level Aggregate - 2 plots
levNames = ['NBA']
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
        yStart = 0
        yEnd = 75
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
                       range = [to_unix_time(datetime.datetime(2018, 10, 15)),
                                to_unix_time(datetime.datetime(2018, 10, 16))]))
    
    fig = go.Figure(data = data, layout = layout)
    offline.plot(fig, filename = fileName + '.html')

#Fin