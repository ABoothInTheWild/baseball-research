# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 23:00:02 2018

@author: ABooth
"""

import os
os.chdir("C:/Users/abooth/Documents/Python Scripts/PastPreds/mlbPlayoffOdds2018")

from MLBWinProbability import *
from MLB538WinProbability import *
from RunsScoredAllowedSimulator import *
import pandas as pd
import numpy as np

access_token = 'a02014c0-9f69-4bf7-b9ac-4d804dfe58a3'
user_agent = 'adbooth01@gmail.com'

stats = xmlstats.Xmlstats(access_token, user_agent)
date_format = datetime.today().strftime("%Y%m%d")    
xmlStandingsOnDate = stats.standings(date=date_format, sport="mlb")
#last year data
endOfReg2017 = datetime(2017, 10, 2)  #2017 last day
stats1 = xmlstats.Xmlstats(access_token, user_agent)
date_format1 = endOfReg2017.strftime("%Y%m%d")    
lastYearStandingsOnDate = stats1.standings(date=date_format1, sport="mlb")

eloDF = pd.read_csv("https://projects.fivethirtyeight.com/mlb-api/mlb_elo.csv")
eloDF = eloDF[eloDF.season == 2018]
eloDF.date = pd.to_datetime(eloDF.date)
eloDF = eloDF.sort_values(["date"]).reset_index(drop=True)

mil2018 = ImportRunsScoredAllowedDF("MIL_2018_RegularSeason.csv")
col2018 = ImportRunsScoredAllowedDF("COL_2018_RegularSeason.csv")
atl2018 = ImportRunsScoredAllowedDF("ATL_2018_RegularSeason.csv")
lad2018 = ImportRunsScoredAllowedDF("LAD_2018_RegularSeason.csv")
bos2018 = ImportRunsScoredAllowedDF("BOS_2018_RegularSeason.csv")
nyy2018 = ImportRunsScoredAllowedDF("NYY_2018_RegularSeason.csv")
hou2018 = ImportRunsScoredAllowedDF("HOU_2018_RegularSeason.csv")
cle2018 = ImportRunsScoredAllowedDF("CLE_2018_RegularSeason.csv")
oak2018 = ImportRunsScoredAllowedDF("OAK_2018_RegularSeason.csv")
chc2018 = ImportRunsScoredAllowedDF("CHC_2018_RegularSeason.csv")
numSims = 100000

##################################################################################

print(MLBWinProbability('MIL', 'COL', xmlStandingsOnDate, lastYearStandingsOnDate))
print(MLB538WinProbability('MIL', 'COL', datetime(2018, 10, 4), eloDF))
print(RunsSimulator(mil2018, col2018, True, numSims, 4))

print(MLBWinProbability('LAD', 'ATL', xmlStandingsOnDate, lastYearStandingsOnDate))
print(MLB538WinProbability('LAD', 'ATL', datetime(2018, 10, 4), eloDF))
print(RunsSimulator(lad2018, atl2018, True, numSims, 4))
##################################################################################

def GetSeriesProb(homeProb, awayProb):
    totalProb = homeProb*homeProb*awayProb
    totalProb += homeProb*homeProb*(1-awayProb)*awayProb
    totalProb += homeProb*homeProb*(1-awayProb)*(1-awayProb)*homeProb
    totalProb += homeProb*(1-homeProb)*awayProb*awayProb
    totalProb += homeProb*(1-homeProb)*awayProb*(1-awayProb)*homeProb
    totalProb += homeProb*(1-homeProb)*(1-awayProb)*awayProb*homeProb
    totalProb += (1-homeProb)*homeProb*awayProb*awayProb
    totalProb += (1-homeProb)*homeProb*awayProb*(1-awayProb)*homeProb
    totalProb += (1-homeProb)*homeProb*(1-awayProb)*awayProb*homeProb
    totalProb += (1-homeProb)*(1-homeProb)*awayProb*awayProb*homeProb
    return totalProb

def GetSeriesProb2(homeProb, awayProb):
    totalProb = homeProb*awayProb
    totalProb += homeProb*(1-awayProb)*awayProb
    totalProb += homeProb*(1-awayProb)*(1-awayProb)*homeProb
    totalProb += (1-homeProb)*awayProb*awayProb
    totalProb += (1-homeProb)*awayProb*(1-awayProb)*homeProb
    totalProb += (1-homeProb)*(1-awayProb)*awayProb*homeProb
    return totalProb


def GetSeriesProb3(homeProb, awayProb):
    totalProb = awayProb
    totalProb += (1-awayProb)*awayProb
    totalProb += (1-awayProb)*(1-awayProb)*homeProb
    return totalProb

def GetSeriesProb31(homeProb, awayProb):
    totalProb = awayProb
    totalProb += (1-awayProb)*homeProb
    return totalProb

def GetSeriesProb21(homeProb, awayProb):
    totalProb = awayProb*awayProb
    totalProb += awayProb*(1-awayProb)*homeProb
    totalProb += (1-awayProb)*awayProb*homeProb
    return totalProb

print(GetSeriesProb(MLBWinProbability('MIL', 'COL', xmlStandingsOnDate, lastYearStandingsOnDate), (1-MLBWinProbability('COL', 'MIL', xmlStandingsOnDate, lastYearStandingsOnDate))))
print(GetSeriesProb(RunsSimulator(mil2018, col2018, True, numSims, 4), (1-RunsSimulator(col2018, mil2018, True, numSims, 4))))

print(GetSeriesProb(MLBWinProbability('LAD', 'ATL', xmlStandingsOnDate, lastYearStandingsOnDate), (1-MLBWinProbability('LAD', 'ATL', xmlStandingsOnDate, lastYearStandingsOnDate))))
print(GetSeriesProb(RunsSimulator(lad2018, atl2018, True, numSims, 4), (1-RunsSimulator(atl2018, lad2018, True, numSims, 4))))

##################################################################################

#MILCOL
print(MLBWinProbability('MIL', 'COL', xmlStandingsOnDate, lastYearStandingsOnDate))
print(MLB538WinProbability('MIL', 'COL', datetime(2018, 10, 5), eloDF))
print(RunsSimulator(mil2018, col2018, True, numSims, 4))

print(GetSeriesProb3(MLBWinProbability('MIL', 'COL', xmlStandingsOnDate, lastYearStandingsOnDate), (1-MLBWinProbability('COL', 'MIL', xmlStandingsOnDate, lastYearStandingsOnDate))))
print(GetSeriesProb3(RunsSimulator(mil2018, col2018, True, numSims, 4), (1-RunsSimulator(col2018, mil2018, True, numSims, 4))))

print(MLBWinProbability('COL', 'MIL', xmlStandingsOnDate, lastYearStandingsOnDate))
print(MLB538WinProbability('COL', 'MIL', datetime(2018, 10, 7), eloDF))
print(RunsSimulator(col2018, mil2018, True, numSims, 4))

#LADATL
print(MLBWinProbability('LAD', 'ATL', xmlStandingsOnDate, lastYearStandingsOnDate))
print(MLB538WinProbability('LAD', 'ATL', datetime(2018, 10, 5), eloDF))
print(RunsSimulator(lad2018, atl2018, True, numSims, 4))

print(GetSeriesProb31(MLBWinProbability('LAD', 'ATL', xmlStandingsOnDate, lastYearStandingsOnDate), (1-MLBWinProbability('LAD', 'ATL', xmlStandingsOnDate, lastYearStandingsOnDate))))
print(GetSeriesProb31(RunsSimulator(lad2018, atl2018, True, numSims, 4), (1-RunsSimulator(atl2018, lad2018, True, numSims, 4))))

print(MLBWinProbability('ATL', 'LAD', xmlStandingsOnDate, lastYearStandingsOnDate))
print(MLB538WinProbability('ATL', 'LAD', datetime(2018, 10, 8), eloDF))
print(RunsSimulator(atl2018, lad2018, True, numSims, 4))


#NYYBOS
print(MLBWinProbability('BOS', 'NYY', xmlStandingsOnDate, lastYearStandingsOnDate))
print(MLB538WinProbability('BOS', 'NYY', datetime(2018, 10, 5), eloDF))
print(RunsSimulator(bos2018, nyy2018, True, numSims, 4))

print(GetSeriesProb21(MLBWinProbability('BOS', 'NYY', xmlStandingsOnDate, lastYearStandingsOnDate), (1-MLBWinProbability('NYY', 'BOS', xmlStandingsOnDate, lastYearStandingsOnDate))))
print(GetSeriesProb21(RunsSimulator(bos2018, nyy2018, True, numSims, 4), (1-RunsSimulator(nyy2018, bos2018, True, numSims, 4))))

print(MLBWinProbability('NYY', 'BOS', xmlStandingsOnDate, lastYearStandingsOnDate))
print(MLB538WinProbability('NYY', 'BOS', datetime(2018, 10, 9), eloDF))
print(RunsSimulator(nyy2018, bos2018, True, numSims, 4))

#CLEHOU
print(MLBWinProbability('HOU', 'CLE', xmlStandingsOnDate, lastYearStandingsOnDate))
print(MLB538WinProbability('HOU', 'CLE', datetime(2018, 10, 6), eloDF))
print(RunsSimulator(hou2018, cle2018, True, numSims, 4))

print(GetSeriesProb3(MLBWinProbability('HOU', 'CLE', xmlStandingsOnDate, lastYearStandingsOnDate), (1-MLBWinProbability('CLE', 'HOU', xmlStandingsOnDate, lastYearStandingsOnDate))))
print(GetSeriesProb3(RunsSimulator(hou2018, cle2018, True, numSims, 4), (1-RunsSimulator(cle2018, hou2018, True, numSims, 4))))

print(MLBWinProbability('CLE', 'HOU', xmlStandingsOnDate, lastYearStandingsOnDate))
print(MLB538WinProbability('CLE', 'HOU', datetime(2018, 10, 8), eloDF))
print(RunsSimulator(cle2018, hou2018, True, numSims, 4))

##################################################################################

#NYYBOS
print(MLBWinProbability('BOS', 'NYY', xmlStandingsOnDate, lastYearStandingsOnDate))
print(MLB538WinProbability('BOS', 'NYY', datetime(2018, 10, 6), eloDF))
print(RunsSimulator(bos2018, nyy2018, True, numSims, 4))

print(GetSeriesProb2(MLBWinProbability('BOS', 'NYY', xmlStandingsOnDate, lastYearStandingsOnDate), (1-MLBWinProbability('NYY', 'BOS', xmlStandingsOnDate, lastYearStandingsOnDate))))
print(GetSeriesProb2(RunsSimulator(bos2018, nyy2018, True, numSims, 4), (1-RunsSimulator(nyy2018, bos2018, True, numSims, 4))))

#CLEHOU
print(MLBWinProbability('HOU', 'CLE', xmlStandingsOnDate, lastYearStandingsOnDate))
print(MLB538WinProbability('HOU', 'CLE', datetime(2018, 10, 6), eloDF))
print(RunsSimulator(hou2018, cle2018, True, numSims, 4))

print(GetSeriesProb2(MLBWinProbability('HOU', 'CLE', xmlStandingsOnDate, lastYearStandingsOnDate), (1-MLBWinProbability('CLE', 'HOU', xmlStandingsOnDate, lastYearStandingsOnDate))))
print(GetSeriesProb2(RunsSimulator(hou2018, cle2018, True, numSims, 4), (1-RunsSimulator(cle2018, hou2018, True, numSims, 4))))


##################################################################################

#HOUBOS
print(MLBWinProbability('BOS', 'HOU', xmlStandingsOnDate, lastYearStandingsOnDate))
print(MLB538WinProbability('BOS', 'HOU', datetime(2018, 10, 13), eloDF))
print(RunsSimulator(bos2018, hou2018, True, numSims, 4))

#MILCOL
print(MLBWinProbability('MIL', 'LAD', xmlStandingsOnDate, lastYearStandingsOnDate))
print(MLB538WinProbability('MIL', 'LAD', datetime(2018, 10, 12), eloDF))
print(RunsSimulator(mil2018, lad2018, True, numSims, 4))
