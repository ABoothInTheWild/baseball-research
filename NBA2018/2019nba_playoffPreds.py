# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 18:49:41 2019

@author: ABooth
"""

#Imports
import pandas as pd
import os
import numpy as np
import heapq
from collections import Counter
from scipy.stats import beta
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType

#2018 Playoff Odds
    
#Load Data
os.chdir('C:/Users/abooth/Documents/Python Scripts/NBA/NBA_18/')
nba18Pre = pd.read_csv("nba2018PreSeasonBetaEstimates.csv")

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

###############################################################################

#2018-2019 NBA Season Results
from datetime import timedelta, date, datetime

client.season_schedule(season_end_year=2019, output_type=OutputType.CSV, output_file_path="C:/Users/abooth/Documents/Data/NBA2018/2019nba_scores.csv")
nba18Results = pd.read_csv("C:/Users/abooth/Documents/Data/NBA2018/2019nba_scores.csv")
nba18Results.away_team = [team.replace(" ", "_") for team in nba18Results.away_team.values]
nba18Results.home_team = [team.replace(" ", "_") for team in nba18Results.home_team.values]
nba18Results.start_time = [(datetime.strptime(start[0:16], '%Y-%m-%d %H:%M') - timedelta(hours=6)) for start in nba18Results.start_time.values]

teamMap = pd.read_csv("C:/Users/abooth/Documents/Data/NBA2018/teamMap.csv")
teamMapDict = dict(teamMap.values)

#https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

dates = []
start_date = date(2019, 1, 8)
end_date = date(2019, 1, 12)
for single_date in daterange(start_date, end_date):
    dates.append(single_date.strftime("%Y%m%d"))
    
dateLen = len(dates)

def getTeamWinsForAbbr(abbr, date):
    bbRefID = teamMapDict[abbr]  
    nba18ResultsSub = nba18Results[nba18Results.start_time < date]
    awayScores = nba18ResultsSub[nba18ResultsSub.away_team == bbRefID]
    awayWins = sum(awayScores.away_team_score > awayScores.home_team_score)
    homeScores = nba18ResultsSub[nba18ResultsSub.home_team == bbRefID]
    homeWins = sum(homeScores.home_team_score > homeScores.away_team_score)    
    return(awayWins + homeWins)
    
def getTeamLossesForAbbr(abbr, date):
    bbRefID = teamMapDict[abbr]  
    nba18ResultsSub = nba18Results[nba18Results.start_time < date]
    awayScores = nba18ResultsSub[nba18ResultsSub.away_team == bbRefID]
    awayLosses = sum(awayScores.away_team_score < awayScores.home_team_score)
    homeScores = nba18ResultsSub[nba18ResultsSub.home_team == bbRefID]
    homeLosses = sum(homeScores.home_team_score < homeScores.away_team_score)    
    return(awayLosses + homeLosses)
    
def getTeamPythagWinsLossesForAbbr(abbr, date):
    bbRefID = teamMapDict[abbr]  
    nba18ResultsSub = nba18Results[nba18Results.start_time < date]
    
    awayGames = nba18ResultsSub[nba18ResultsSub.away_team == bbRefID]
    awayPointsScored = sum(awayGames.away_team_score.values)
    awayPointsAllowed = sum(awayGames.home_team_score.values)
    
    homeGames = nba18ResultsSub[nba18ResultsSub.home_team == bbRefID]
    homePointsScored = sum(homeGames.home_team_score.values)
    homePointsAllowed = sum(homeGames.away_team_score.values)

    totalPointsScored = awayPointsScored + homePointsScored
    totalPointsAllowed = awayPointsAllowed + homePointsAllowed
    totalGames = len(homeGames) + len(awayGames)
    
    if totalPointsAllowed == 0 or totalPointsScored == 0:
        return([0, 0])
    else:
        pythagWL = totalPointsScored**16.5 / (totalPointsScored**16.5 + totalPointsAllowed**16.5)
        pythagWins = pythagWL * totalGames
        pythagLosses = (1-pythagWL) * totalGames
        
        return([pythagWins, pythagLosses])

###############################################################################
#os.chdir('C:/Users/abooth/Documents/Data/NBA2018/Pythag/')
#resultsDF = pd.read_csv("nba2019PlayoffPreds_Pythag.csv")
os.chdir('C:/Users/abooth/Documents/Data/NBA2018/')
resultsDF = pd.read_csv("nba2019PlayoffPreds.csv")

#Get Posterior Wins for Dates
for i in range(len(dates)):
    currDate = dates[i]

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
            priorA = nba18Pre[nba18Pre.Abbr == team]["PriorAlpha"].values[0]
            priorB = nba18Pre[nba18Pre.Abbr == team]["PriorBeta"].values[0]            
            teamWins = getTeamWinsForAbbr(team, currDate)
            teamLosses = getTeamLossesForAbbr(team, currDate)
#            pythagWL = getTeamPythagWinsLossesForAbbr(team, currDate)
#            
#            pythagWins = pythagWL[0]
#            pythagLosses = pythagWL[1]           
#            
#            posteriorAlpha = priorA + pythagWins
#            posteriorBeta = priorB + pythagLosses
            
            posteriorAlpha = priorA + teamWins
            posteriorBeta = priorB + teamLosses
            
            sample = beta.rvs(posteriorAlpha, posteriorBeta, size=ntrials)
            gamesLeft = 82 - teamWins - teamLosses
            winEstimate = np.round(teamWins + sample*gamesLeft,0)
            tempResults.append(winEstimate)
            expectedWins.append(np.round(np.mean(teamWins + sample*gamesLeft),0))
            teams.append(team)
        #find playoff teams   
        tempResults = np.array(tempResults)
        argMaxesIndx = [heapq.nlargest(8, range(len(tempResults[:,i])), 
                        key=tempResults[:,i].__getitem__) 
                        for i in range(np.size(tempResults,1))]
        results.update(np.array(argMaxesIndx).flatten())
        confOdds.extend(np.array(list(results.values()))/float(ntrials))
        
    resultsDF["Teams"] = teams
    resultsDF["PlayoffOdds" + currDate] = confOdds
    resultsDF["ExpectedWins" + currDate] = expectedWins

resultsDF.to_csv("nba2019PlayoffPreds.csv", index=False)
#resultsDF.to_csv("nba2019PlayoffPreds_Pythag.csv", index=False)

#######################################################################

#Playoff Odds
#os.chdir('C:/Users/abooth/Documents/Data/NBA2018/Pythag/')
#resultsDF = pd.read_csv("nba2019PlayoffPreds_Pythag.csv")
os.chdir('C:/Users/abooth/Documents/Data/NBA2018/')
resultsDF = pd.read_csv("nba2019PlayoffPreds.csv")

#import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
import datetime

dates = []
start_date = date(2018, 10, 15)
end_date = date(2019, 1, 12)
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
            plotTitle = leagueName + ' 2018-2019 Bayesian ' + dataType + ' Probabilities'
            yLabel = dataType + ' Probability'
            fileName = os.getcwd() + fileNamePrefix + leagueName + '_2018-2019_' + dataType + '_Probs'
            yStart = 0
            yEnd = 1.05
            hoverFormat = '.2f'
        else:
            plotTitle = leagueName + ' 2018-2019 Bayesian Expected Wins'
            yLabel = "Expected Wins"
            fileName = os.getcwd() + fileNamePrefix + leagueName + '_2018-2019_' + dataType
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
                                    to_unix_time(datetime.datetime(2019, 1, 12))]))
        
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
        plotTitle = levName + ' 2018-2019 Bayesian ' + dataType + ' Probabilities'
        yLabel = dataType + ' Probability'
        fileName = os.getcwd() + fileNamePrefix + levName + '_2018-2019_' + dataType + '_Probs'
        yStart = 0
        yEnd = 1.05
        hoverFormat = '.2f'
    else:
        plotTitle = levName + ' 2018-2019 Bayesian Expected Wins'
        yLabel = "Expected Wins"
        fileName = os.getcwd() + fileNamePrefix + levName + '_2018-2019_' + dataType
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
                                to_unix_time(datetime.datetime(2019, 1, 12))]))
    
    fig = go.Figure(data = data, layout = layout)
    offline.plot(fig, filename = fileName + '.html')

#Fin