# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 11:42:52 2018

@author: abooth
"""

#2018 RedSox Win Record
import pandas as pd
import numpy as np
from scipy.stats import beta
import os

#read data
os.chdir('C:/Users/abooth/Documents/Python Scripts/PastPreds/mlbPlayoffOdds2018')
beta18Pre = pd.read_csv("mlb2018PreSeasonBetaEstimates.csv")

#init contstants
team = "BOS"
ntrials=100000
beatMarinersRecordProb = []

#Get Preseason
np.random.seed(seed=54321)
priorA = beta18Pre[beta18Pre.Team_Abbr == team]["PriorAlpha"].values[0]
priorB = beta18Pre[beta18Pre.Team_Abbr == team]["PriorBeta"].values[0]
sample = beta.rvs(priorA, priorB, size=ntrials)
sampleWins = np.round(sample*162,0)
prob = len(sampleWins[sampleWins >= 116])/float(ntrials)
beatMarinersRecordProb.append(prob)

#read data downloaded from xmlStats API
mlb18Results = pd.read_csv("mlb2018SeasonResults.csv")

from datetime import timedelta, date
#https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

dates = []
start_date = date(2018, 3, 29)
end_date = date(2018, 8, 7)
for single_date in daterange(start_date, end_date):
    dates.append(single_date.strftime("%Y%m%d"))

dateLen = len(dates)
for i in range(len(dates)):
    currDate = dates[i]   
    
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
    beatMarinersRecordProb.append(prob)

#import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
import datetime

dates = []
start_date = date(2018, 3, 28)
end_date = date(2018, 8, 7)
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

    
x = dates
fileName = os.getcwd() + '/RedSox116WinProbability'
hoverFormat = '.3f'
data = []
trace = go.Scatter(
        x=x,
        y=beatMarinersRecordProb,
        mode='lines+markers',
        name = team,
        line = dict(
                color = teamColors[team],
                width = 4,
                shape='linear'))

data.append(trace)    
layout = go.Layout(
    title = 'Probability the Boston Red Sox Win at least 116 Games in 2018',
    yaxis = dict(title = 'Probability',
                 range = [0, 0.15],
                 hoverformat = hoverFormat),
    xaxis = dict(title = '',
               range = [to_unix_time(datetime.datetime(2018, 3, 28)),
                        to_unix_time(datetime.datetime(2018, 8, 7))]))

fig = go.Figure(data = data, layout = layout)
offline.plot(fig, filename = fileName + '.html')
    
