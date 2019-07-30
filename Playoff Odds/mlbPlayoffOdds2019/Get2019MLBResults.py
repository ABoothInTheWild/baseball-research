# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 12:23:04 2019

@author: ABooth
"""

from xmlstats import xmlstats
import numpy as np
import pandas as pd
import os

access_token = '0aabe405-8ec2-4c0c-8e8b-39e164d7e7ca'
user_agent = 'adbooth01@gmail.com'

os.chdir('C:/Users/abooth/Documents/Python Scripts/PastPreds/mlbPlayoffOdds2019')

stats = xmlstats.Xmlstats(access_token, user_agent)

datetest = "20190320"
standingsOnDate = stats.standings(date=datetest, sport="mlb")

print(sum([standing.won for standing in standingsOnDate.standing])) #1

teamIds = np.sort(np.array([standing.team_id for standing in standingsOnDate.standing]))

teamWins = []
teamLosses = []
for teamId in teamIds:
    teamWins.extend([standing.won for standing in standingsOnDate.standing if standing.team_id == teamId])
    teamLosses.extend([standing.lost for standing in standingsOnDate.standing if standing.team_id == teamId])

df = pd.DataFrame(np.column_stack([teamIds,teamWins, teamLosses]),
                  columns = ['xmlstatsTeamId','Wins'+datetest, 'Losses'+datetest])


from datetime import timedelta, date
import time

#https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

seasonResults = pd.DataFrame({'xmlstatsTeamId':teamIds})
start_date = date(2019, 3, 20)
end_date = date(2019, 7, 11)
for single_date in daterange(start_date, end_date):
    date_format = single_date.strftime("%Y%m%d")
    standingsOnDate = stats.standings(date=date_format, sport="mlb")
    teamWins = []
    teamLosses = []
    for teamId in teamIds:
        teamWins.extend([standing.won for standing in standingsOnDate.standing if standing.team_id == teamId])
        teamLosses.extend([standing.lost for standing in standingsOnDate.standing if standing.team_id == teamId])
    seasonResults["Wins_"+date_format] = teamWins
    seasonResults["Losses_"+date_format] = teamLosses
    print(date_format)
    time.sleep(12) #6 requests a minute

seasonResults.to_csv("mlb2019SeasonResults.csv", index=False)

#####################################################################################

#Update For yesterday

seasonResults = pd.read_csv("mlb2019SeasonResults.csv")
start_date = date(2019, 7, 22)
end_date = date(2019, 7, 29)
for single_date in daterange(start_date, end_date):
    date_format = single_date.strftime("%Y%m%d")
    standingsOnDate = stats.standings(date=date_format, sport="mlb")
    teamWins = []
    teamLosses = []
    for teamId in teamIds:
        teamWins.extend([standing.won for standing in standingsOnDate.standing if standing.team_id == teamId])
        teamLosses.extend([standing.lost for standing in standingsOnDate.standing if standing.team_id == teamId])
    seasonResults["Wins_"+date_format] = teamWins
    seasonResults["Losses_"+date_format] = teamLosses
    print(date_format)
    time.sleep(12) #6 requests a minute
seasonResults.to_csv("mlb2019SeasonResults.csv", index=False)