# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 16:50:53 2018

@author: ABooth
"""

import os
os.chdir('C:/Users/abooth/Documents/Python Scripts/PastPreds/mlbPlayoffOdds2019')

from MLBWinProbability_BAYES import *
from MLB538WinProbability import *
from RunsScoredAllowedSimulator import *
import pandas as pd
import numpy as np

access_token = '0aabe405-8ec2-4c0c-8e8b-39e164d7e7ca'
user_agent = 'adbooth01@gmail.com'

stats = xmlstats.Xmlstats(access_token, user_agent)
date_format = datetime.today().strftime("%Y%m%d")    
xmlStandingsOnDate = stats.standings(date=date_format, sport="mlb")
#last year data
endOfReg2018 = datetime(2018, 10, 1)  #2018 last day
stats1 = xmlstats.Xmlstats(access_token, user_agent)
date_format1 = endOfReg2018.strftime("%Y%m%d")    
lastYearStandingsOnDate = stats1.standings(date=date_format1, sport="mlb")

eloDF = pd.read_csv("https://projects.fivethirtyeight.com/mlb-api/mlb_elo.csv")
eloDF = eloDF[eloDF.season == 2019]
eloDF.date = pd.to_datetime(eloDF.date)
eloDF = eloDF.sort_values(["date"]).reset_index(drop=True)

home2019 = ImportRunsScoredAllowedDF("TEX_2019_RegularSeason.csv")
away2019 = ImportRunsScoredAllowedDF("HOU_2019_RegularSeason.csv")

homeAbbr = "TEX"
awayAbbr = "HOU"
numSims = 100000

##################################################################################
    
#HOUTEX
homeWin_Bayes = MLBWinProbability(homeAbbr, awayAbbr, xmlStandingsOnDate, lastYearStandingsOnDate)
#homeWinAway_Bayes = 1 - MLBWinProbability(awayAbbr, homeAbbr, xmlStandingsOnDate, lastYearStandingsOnDate)
homeWin_RSRA = RunsSimulator(home2019, away2019, True, numSims, 4)
#homeWinAway_RSRA = 1 - RunsSimulator(away2019, home2019, True, numSims, 4)
homeWin_Elo = MLB538WinProbability(homeAbbr, awayAbbr, datetime.today().strftime("%Y%m%d"), eloDF)

print("Bayes Home Win Prob: " + str(homeWin_Bayes))
print("RSRA Home Win Prob: " + str(homeWin_RSRA))
print("Elo Home Win Prob: " + str(homeWin_Elo))