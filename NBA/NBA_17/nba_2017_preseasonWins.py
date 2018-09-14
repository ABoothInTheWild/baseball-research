# -*- coding: utf-8 -*-
"""
Created on Thu Sep 06 23:53:05 2018

@author: Alexander
"""

#Imports
import pandas as pd
import os
import numpy as np

#Load Data
nba17Pre = pd.read_csv('nba_2017_preseasonWins.csv')

#Get columns
cols = nba17Pre.columns
allEstimatesCols = list(cols[2:10])
#allEstimatesCols.extend(cols[15:20]) #Turns out the 5Yr rolling average is not good
allEstimatesCols.extend(cols[16:18])

#Wisdom of the crowd with all win estimates
maeErrors = []
rmseErrors = []
for i in allEstimatesCols:
    maeError = np.mean(abs(nba17Pre[i] - nba17Pre["2017_Wins"]))
    rmseError = np.sqrt(((nba17Pre[i] - nba17Pre["2017_Wins"]) ** 2).mean(axis=None))    
    maeErrors.append(round(maeError,3))
    rmseErrors.append(round(rmseError,3))
    
df = pd.DataFrame(list(zip(allEstimatesCols, maeErrors, rmseErrors)), columns=["Source", "MAE", "RMSE"])
print(df.sort_values("MAE").reset_index(drop=True))
print("")
print(df.sort_values("RMSE").reset_index(drop=True))
print("")

##########################################################################

#Reference:
#https://stats.stackexchange.com/questions/12232/calculating-the-parameters-of-a-beta-distribution-using-the-mean-and-variance
def estimateBetaParams(mu, var):
  alpha = ((1 - mu) / var - 1 / mu) * mu ** 2 
  beta = alpha * (1 / mu - 1)
  return({'alpha':alpha, 'beta':beta})

##########################################################################

totalGames = 82

#Get personal games to regress by
preWinPerc = nba17Pre["Expert_Avg"]/totalGames
luckSD = np.sqrt((preWinPerc * (1-preWinPerc))/totalGames)
med5YrSD = np.median(pd.DataFrame(nba17Pre[cols[10:15]]/totalGames).std(axis=1))

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

nba17Pre["PriorAlpha"] = priorAlphas2
nba17Pre["PriorBeta"] = priorBetas2

print(np.mean(regressedGames)) #32
print(np.mean(priorAlphas - priorAlphas2)) #0.5
print(np.mean(priorBetas - priorBetas2)) #0.5 Small difference, but not negligible

##########################################################################

#Graphing Beta Distribution Example

#Reference:
#https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.stats.beta.html

from scipy.stats import beta
import matplotlib.pyplot as plt

#GS Warriors
#Set seed, init plots, get beta parameters
np.random.seed(seed=12345)
priorA = nba17Pre[nba17Pre.Abbr == "GSW"]["PriorAlpha"].values[0]
priorB = nba17Pre[nba17Pre.Abbr == "GSW"]["PriorBeta"].values[0]

#Summary stats of distribution
mean, var, skew, kurt = beta.stats(priorA, priorB, moments='mvsk')

#Plot pdf
x = np.linspace(beta.ppf(0.001, priorA, priorB),
              beta.ppf(0.999, priorA, priorB), 1000)

#Check pdf vs cdf
vals = beta.ppf([0.001, 0.5, 0.999], priorA, priorB)
print(np.allclose([0.001, 0.5, 0.999], beta.cdf(vals, priorA, priorB))) #True

#Make plot pretty
fig, ax = plt.subplots(1, 1)
ax.plot(x, beta.pdf(x, priorA, priorB),
         'r-', lw=5, alpha=0.6, label='beta pdf')
ax.legend(loc='best', frameon=False)
ax.set_xlim([0, 1])
ax.set_ylim([0, 8])
plt.title('GSW 2017 Preseason WP% Beta Estimate')
plt.ylabel('Density')
plt.xlabel('Winning Percentage')
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()

#point estimate and 95% CI for end-of-season wins for GSW
r = beta.rvs(priorA, priorB, size=10000)
print(np.mean(r) * totalGames) #66.5
print(np.percentile(r, 2.5) * totalGames) #49
print(np.percentile(r, 97.5) * totalGames) #78

##############################################################################

#Get win estimate and CIs for all teams
nba17Pre["2017_Actual_WP"] = nba17Pre["2017_Wins"] / totalGames

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
for team in nba17Pre.Abbr.values:
    priorA = nba17Pre[nba17Pre.Abbr == team]["PriorAlpha"].values[0]
    priorB = nba17Pre[nba17Pre.Abbr == team]["PriorBeta"].values[0]
    
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
nba17Pre["Beta_Estimate"] = winPercBeta
nba17Pre["80CI_Low"] = ci80Low
nba17Pre["80CI_High"] = ci80High
nba17Pre["90CI_Low"] = ci90Low
nba17Pre["90CI_High"] = ci90High
nba17Pre["95CI_Low"] = ci95Low
nba17Pre["95CI_High"] = ci95High
nba17Pre["99CI_Low"] = ci99Low
nba17Pre["99CI_High"] = ci99High

#turn win percentages into regular season win estimates
nba17Pre["Beta_Wins"] = np.round(nba17Pre.Beta_Estimate * totalGames,1)

nba17Pre["80CI_Low_Wins"] = np.round(nba17Pre["80CI_Low"] * totalGames,1)
nba17Pre["80CI_High_Wins"] = np.round(nba17Pre["80CI_High"] * totalGames,1)
nba17Pre["90CI_Low_Wins"] = np.round(nba17Pre["90CI_Low"] * totalGames,1)
nba17Pre["90CI_High_Wins"] = np.round(nba17Pre["90CI_High"] * totalGames,1)
nba17Pre["95CI_Low_Wins"] = np.round(nba17Pre["95CI_Low"] * totalGames,1)
nba17Pre["95CI_High_Wins"] = np.round(nba17Pre["95CI_High"] * totalGames,1)
nba17Pre["99CI_Low_Wins"] = np.round(nba17Pre["99CI_Low"] * totalGames,1)
nba17Pre["99CI_High_Wins"] = np.round(nba17Pre["99CI_High"] * totalGames,1)

#check if actual 2017 wins fell in preseason confidence intervals
nba17Pre["FinalIn80CI"] = np.where(np.logical_and(np.greater_equal(nba17Pre["2017_Actual_WP"], nba17Pre["80CI_Low"]),
         np.less_equal(nba17Pre["2017_Actual_WP"], nba17Pre["80CI_High"])), 1, 0)
nba17Pre["FinalIn90CI"] = np.where(np.logical_and(np.greater_equal(nba17Pre["2017_Actual_WP"], nba17Pre["90CI_Low"]),
         np.less_equal(nba17Pre["2017_Actual_WP"], nba17Pre["90CI_High"])), 1, 0)
nba17Pre["FinalIn95CI"] = np.where(np.logical_and(np.greater_equal(nba17Pre["2017_Actual_WP"], nba17Pre["95CI_Low"]),
         np.less_equal(nba17Pre["2017_Actual_WP"], nba17Pre["95CI_High"])), 1, 0)
nba17Pre["FinalIn99CI"] = np.where(np.logical_and(np.greater_equal(nba17Pre["2017_Actual_WP"], nba17Pre["99CI_Low"]),
         np.less_equal(nba17Pre["2017_Actual_WP"], nba17Pre["99CI_High"])), 1, 0)

print(sum(nba17Pre["FinalIn80CI"])/float(len(nba17Pre))) #.83 25/30
print(sum(nba17Pre["FinalIn90CI"])/float(len(nba17Pre))) #.87 26/30
print(sum(nba17Pre["FinalIn95CI"])/float(len(nba17Pre))) #.93 28/30
print(sum(nba17Pre["FinalIn99CI"])/float(len(nba17Pre))) #1.0 30/30
         
#nba17Pre.to_csv("nba2017PreSeasonBetaEstimates.csv", index=False)

##############################################################################

#Create Gifs per day per prior per team

import errno
import imageio

#read data downloaded from xmlStats API
nba17Results = pd.read_csv("nba2017SeasonResults.csv")
nba17Pre = pd.read_csv("nba2017PreSeasonBetaEstimates.csv")

from datetime import timedelta, date
#https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

dates = []
start_date = date(2017, 10, 17)
end_date = date(2018, 4, 12)
for single_date in daterange(start_date, end_date):
    dates.append(single_date.strftime("%Y%m%d"))
    
teams = nba17Pre.Abbr.values

#Get Gifs    
for team_Abbr in teams:
    #Personalized Prior
    filename = "Teams/" + team_Abbr + "/personalizedPrior/"
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    os.chdir(filename)
    
    priorA = nba17Pre[nba17Pre.Abbr == team_Abbr]["PriorAlpha"].values[0]
    priorB = nba17Pre[nba17Pre.Abbr == team_Abbr]["PriorBeta"].values[0]
    
    team17Res = nba17Results[nba17Results.Abbr==team_Abbr].iloc[:,2:356]
    teamWins = team17Res.iloc[:,range(0,354,2)].values[0]
    teamLosses = team17Res.iloc[:,range(1,355,2)].values[0]
    
    #Plot pdf
    np.random.seed(seed=12345)
    fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
    x = np.linspace(beta.ppf(0.001, priorA, priorB),
                  beta.ppf(0.999, priorA, priorB), 1000)
    ax.plot(x, beta.pdf(x, priorA, priorB),
             'r-', lw=5, alpha=0.6, label='beta pdf')
    
    #Make plot pretty
    ax.legend(loc='best', frameon=False)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 10])
    plt.title(team_Abbr + ' 2017 Preseason WP% Prior Beta Estimate')
    plt.ylabel('Density')
    plt.xlabel('Winning Percentage')
    plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
    #plt.show()
    fig.savefig(team_Abbr + '20171016Prior.png', bbox_inches='tight')
    
    for i in range(len(dates)):
        posteriorAlpha = priorA + teamWins[i]
        posteriorBeta = priorB + teamLosses[i]    
        currDate = dates[i]
        
        #Plot pdf
        fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
        x = np.linspace(beta.ppf(0.001, posteriorAlpha, posteriorBeta),
                      beta.ppf(0.999, posteriorAlpha, posteriorBeta), 1000)
        ax.plot(x, beta.pdf(x, posteriorAlpha, posteriorBeta),
                 'r-', lw=5, alpha=0.6, label='beta pdf')
        
        #Make plot pretty
        ax.legend(loc='best', frameon=False)
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 10])
        plt.title(team_Abbr + " " + currDate + ' WP% Posterior Beta Estimate')
        plt.ylabel('Density')
        plt.xlabel('Winning Percentage')
        plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
        #plt.show()
        fig.savefig(team_Abbr+currDate + 'Posterior.png', bbox_inches='tight')
        plt.clf()
    
    images = []
    filenames = os.listdir(os.getcwd())
    for imgFilename in filenames:
        images.append(imageio.imread(imgFilename))
    
    # Save them as frames into a gif 
    exportname = team_Abbr + "2017WPBetaEstimates_Personalized.gif"
    imageio.mimsave(exportname, images, format='GIF', duration=0.1)
    print(team_Abbr) #track progress

##############################################################################

#2017 Playoff Odds
    
import heapq
from collections import Counter

#read data downloaded from xmlStats API
nba17Results = pd.read_csv("nba2017SeasonResults.csv")
nba17Pre = pd.read_csv("nba2017PreSeasonBetaEstimates.csv")

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
        alphaEst = nba17Pre[nba17Pre.Abbr == team]["PriorAlpha"].values[0]
        betaEst = nba17Pre[nba17Pre.Abbr == team]["PriorBeta"].values[0]
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
resultsDF["PlayoffOdds20171016"] = confOdds
resultsDF["ExpectedWins20171016"] = expectedWins

###############################################################################

#Create playoff odds per day per prior per team

from datetime import date
#https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

dates = []
start_date = date(2017, 10, 17)
end_date = date(2018, 4, 12)
for single_date in daterange(start_date, end_date):
    dates.append(single_date.strftime("%Y%m%d"))
    
dateLen = len(dates)
 
#resultsDF = pd.DataFrame()
for i in range(len(dates)):
    currDate = dates[i]
    
    #init Odds arrays
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
            #get priors
            priorA = nba17Pre[nba17Pre.Abbr == team]["PriorAlpha"].values[0]
            priorB = nba17Pre[nba17Pre.Abbr == team]["PriorBeta"].values[0]
            #get posteriors
            team17Res = nba17Results[nba17Results.Abbr==team].iloc[:,2:((2*dateLen)+2)]
            teamWins = team17Res.iloc[:,range(0,(2*dateLen),2)].values[0]
            teamLosses = team17Res.iloc[:,range(1,(2*dateLen)+1,2)].values[0]
            posteriorAlpha = priorA + teamWins[i]
            posteriorBeta = priorB + teamLosses[i]    
            #where the magic happens
            sample = beta.rvs(posteriorAlpha, posteriorBeta, size=ntrials)
            gamesLeft = 82 - teamWins[i] - teamLosses[i]
            winEstimate = np.round(teamWins[i] + sample*gamesLeft,0)
            tempResults.append(winEstimate)
            expectedWins.append(np.round(np.mean(teamWins[i] + sample*gamesLeft),0))
            teams.append(team)
        #find playoff teams   
        tempResults = np.array(tempResults)
        argMaxesIndx = [heapq.nlargest(8, range(len(tempResults[:,j])), 
                        key=tempResults[:,j].__getitem__) 
                        for j in range(np.size(tempResults,1))]
        results.update(np.array(argMaxesIndx).flatten())
        confOdds.extend(np.array(list(results.values()))/float(ntrials))
              
    resultsDF["Teams"] = teams
    resultsDF["PlayoffOdds" + currDate] = confOdds
    resultsDF["ExpectedWins" + currDate] = expectedWins
    
resultsDF.to_csv("nba2017PlayoffPreds.csv", index=False)

#######################################################################

#Playoff Odds

resultsDF = pd.read_csv("nba2017PlayoffPreds.csv")

#import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
import datetime

dates = []
start_date = date(2017, 10, 16)
end_date = date(2018, 4, 12)
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
            plotTitle = leagueName + ' 2017 Bayesian ' + dataType + ' Probabilities'
            yLabel = dataType + ' Probability'
            fileName = os.getcwd() + fileNamePrefix + leagueName + '_2017_' + dataType + '_Probs'
            yStart = 0
            yEnd = 1.05
            hoverFormat = '.2f'
        else:
            plotTitle = leagueName + ' 2017 Bayesian Expected Wins'
            yLabel = "Expected Wins"
            fileName = os.getcwd() + fileNamePrefix + leagueName + '_2017_' + dataType
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
                           range = [to_unix_time(datetime.datetime(2017, 10, 16)),
                                    to_unix_time(datetime.datetime(2018, 4, 12))]))
        
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
        plotTitle = levName + ' 2017 Bayesian ' + dataType + ' Probabilities'
        yLabel = dataType + ' Probability'
        fileName = os.getcwd() + fileNamePrefix + levName + '_2017_' + dataType + '_Probs'
        yStart = 0
        yEnd = 1.05
        hoverFormat = '.2f'
    else:
        plotTitle = levName + ' 2017 Bayesian Expected Wins'
        yLabel = "Expected Wins"
        fileName = os.getcwd() + fileNamePrefix + levName + '_2017_' + dataType
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
                       range = [to_unix_time(datetime.datetime(2017, 10, 16)),
                                to_unix_time(datetime.datetime(2018, 4, 12))]))
    
    fig = go.Figure(data = data, layout = layout)
    offline.plot(fig, filename = fileName + '.html')

#Fin
