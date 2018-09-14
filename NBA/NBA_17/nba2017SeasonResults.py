# -*- coding: utf-8 -*-
"""
Created on Fri Sep 07 14:28:16 2018

@author: Alexander
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 15:01:09 2018

@author: abooth
"""

from xmlstats import xmlstats
import numpy as np
import pandas as pd

access_token = '27ab1460-5a3b-47a5-bab8-7c0192f848d9'
user_agent = 'adbooth01@gmail.com'


stats = xmlstats.Xmlstats(access_token, user_agent)

datetest = "20171017"
standingsOnDate = stats.standings(date=datetest, sport="nba")

sum([standing.won for standing in standingsOnDate.standing]) #3

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
start_date = date(2017, 10, 17)
end_date = date(2018, 4, 12)
for single_date in daterange(start_date, end_date):
    date_format = single_date.strftime("%Y%m%d")
    standingsOnDate = stats.standings(date=date_format, sport="nba")
    teamWins = []
    teamLosses = []
    for teamId in teamIds:
        teamWins.extend([standing.won for standing in standingsOnDate.standing if standing.team_id == teamId])
        teamLosses.extend([standing.lost for standing in standingsOnDate.standing if standing.team_id == teamId])
    seasonResults["Wins_"+date_format] = teamWins
    seasonResults["Losses_"+date_format] = teamLosses
    print(date_format)
    time.sleep(12) #6 requests a minute

seasonResults.to_csv("nba2017SeasonResults.csv", index=False)