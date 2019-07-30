# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 10:01:45 2019

@author: ABooth
"""

import pandas as pd
import numpy as np
from scipy.stats import beta
import os
from datetime import timedelta, date

#https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
#read data downloaded from xmlStats API
os.chdir('C:/Users/abooth/Documents/Python Scripts/PastPreds/mlbPlayoffOdds2019')
beta19Pre = pd.read_csv("mlb2019PreSeasonBetaEstimates.csv")
mlb19Results = pd.read_csv("mlb2019SeasonResults.csv")
        
dates = []
start_date = date(2019, 3, 20)
end_date = date(2019, 7, 11)
for single_date in daterange(start_date, end_date):
    dates.append(single_date.strftime("%Y%m%d"))

#TeamAbbrToXMLSTATSId
teamAbbrsToId = {'CLE':'cleveland-indians',
 'MIN':'minnesota-twins',
 'DET':'detroit-tigers',
 'CHW':'chicago-white-sox',
 'KCR':'kansas-city-royals',
 'BOS': 'boston-red-sox',
 'NYY':'new-york-yankees',
 'TBR':'tampa-bay-rays',
 'TOR':'toronto-blue-jays',
 'BAL':'baltimore-orioles',
 'HOU':'houston-astros',
 'OAK':'oakland-athletics',
 'SEA': 'seattle-mariners',
 'LAA':'los-angeles-angels',
 'TEX':'texas-rangers',
 'CHC':'chicago-cubs',
 'MIL':'milwaukee-brewers',
 'STL':'st-louis-cardinals',
 'PIT':'pittsburgh-pirates',
 'CIN':'cincinnati-reds',
 'ATL':'atlanta-braves',
 'PHI':'philadelphia-phillies',
 'WSN':'washington-nationals',
 'NYM':'new-york-mets',
 'MIA':'miami-marlins',
 'LAD':'los-angeles-dodgers',
 'COL':'colorado-rockies',
 'ARI':'arizona-diamondbacks',
 'SFG':'san-francisco-giants',
 'SDP':'san-diego-padres'}

ntrials=100000
np.random.seed(seed=54321)

dateLen = len(dates)
i = dateLen - 1

teams = []
winEstimates = []
lowWins = []
highWins = []
winPerc = []
lowWinPerc = []
highWinPerc = []

for team in teamAbbrsToId.keys():
    priorA = beta19Pre[beta19Pre.Team_Abbr == team]["PriorAlpha"].values[0]
    priorB = beta19Pre[beta19Pre.Team_Abbr == team]["PriorBeta"].values[0]
    #get posteriors
    team19Res = mlb19Results[mlb19Results.Team_Abbr==team].iloc[:,2:((2*dateLen)+2)]
    teamWins = team19Res.iloc[:,range(0,(2*dateLen),2)].values[0]
    teamLosses = team19Res.iloc[:,range(1,(2*dateLen)+1,2)].values[0]
    posteriorAlpha = priorA + teamWins[i]
    posteriorBeta = priorB + teamLosses[i]    
    
    #where the magic happens
    sample = beta.rvs(posteriorAlpha, posteriorBeta, size=ntrials)
    gamesLeft = 162 - teamWins[i] - teamLosses[i]
    winEstimate = np.round(teamWins[i] + sample*gamesLeft,0)
    
    teams.append(team)
    winEstimates.append(np.mean(winEstimate))
    lowWins.append(np.percentile(winEstimate, 2.5))
    highWins.append(np.percentile(winEstimate, 97.5))
    
    winPerc.append(np.mean(sample))
    lowWinPerc.append(np.percentile(sample, 2.5))
    highWinPerc.append(np.percentile(sample, 97.5))

df = pd.DataFrame()

df["Team"] = teams
df["WinEstimate"] = winEstimates
df["WinsLow"] = lowWins
df["WinsHigh"] = highWins
df["WinPercent"] = winPerc
df["LowWinPercent"] = lowWinPerc
df["HighWinPercent"] = highWinPerc

df.to_csv("teamWinEstimates_0711.csv", index=False)