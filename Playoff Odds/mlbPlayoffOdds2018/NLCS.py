# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 16:50:53 2018

@author: ABooth
"""

import os

from MLBWinProbability import *
from MLB538WinProbability import *
from RunsScoredAllowedSimulator import *
import pandas as pd
import numpy as np

access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
user_agent = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

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
lad2018 = ImportRunsScoredAllowedDF("LAD_2018_RegularSeason.csv")
bos2018 = ImportRunsScoredAllowedDF("BOS_2018_RegularSeason.csv")
hou2018 = ImportRunsScoredAllowedDF("HOU_2018_RegularSeason.csv")
numSims = 100000

##################################################################################

def GetSeries7Prob00(homeProb, awayProb):
    totalProb = homeProb*homeProb*awayProb*awayProb    
    totalProb += homeProb*homeProb*awayProb*(1-awayProb)*awayProb
    totalProb += homeProb*homeProb*awayProb*(1-awayProb)*(1-awayProb)*homeProb
    totalProb += homeProb*homeProb*awayProb*(1-awayProb)*(1-awayProb)*(1-homeProb)*homeProb    
    totalProb += homeProb*homeProb*(1-awayProb)*awayProb*awayProb
    totalProb += homeProb*homeProb*(1-awayProb)*awayProb*(1-awayProb)*homeProb
    totalProb += homeProb*homeProb*(1-awayProb)*awayProb*(1-awayProb)*(1-homeProb)*homeProb
    totalProb += homeProb*homeProb*(1-awayProb)*(1-awayProb)*awayProb*homeProb
    totalProb += homeProb*homeProb*(1-awayProb)*(1-awayProb)*awayProb*(1-awayProb)*homeProb
    totalProb += homeProb*homeProb*(1-awayProb)*(1-awayProb)*(1-awayProb)*homeProb*homeProb    
    totalProb += homeProb*(1-homeProb)*awayProb*awayProb*awayProb
    totalProb += homeProb*(1-homeProb)*awayProb*awayProb*(1-awayProb)*homeProb
    totalProb += homeProb*(1-homeProb)*awayProb*awayProb*(1-awayProb)*(1-homeProb)*homeProb
    totalProb += homeProb*(1-homeProb)*awayProb*(1-awayProb)*awayProb*homeProb
    totalProb += homeProb*(1-homeProb)*awayProb*(1-awayProb)*awayProb*(1-awayProb)*homeProb
    totalProb += homeProb*(1-homeProb)*awayProb*(1-awayProb)*(1-awayProb)*homeProb*homeProb      
    totalProb += homeProb*(1-homeProb)*(1-awayProb)*awayProb*awayProb*homeProb
    totalProb += homeProb*(1-homeProb)*(1-awayProb)*awayProb*awayProb*(1-homeProb)*homeProb
    totalProb += homeProb*(1-homeProb)*(1-awayProb)*awayProb*(1-awayProb)*homeProb*homeProb
    totalProb += homeProb*(1-homeProb)*(1-awayProb)*(1-awayProb)*awayProb*homeProb*homeProb    
    totalProb += (1-homeProb)*homeProb*awayProb*awayProb*awayProb    
    totalProb += (1-homeProb)*homeProb*awayProb*awayProb*(1-awayProb)*homeProb
    totalProb += (1-homeProb)*homeProb*awayProb*awayProb*(1-awayProb)*(1-homeProb)*homeProb    
    totalProb += (1-homeProb)*homeProb*awayProb*(1-awayProb)*awayProb*homeProb
    totalProb += (1-homeProb)*homeProb*awayProb*(1-awayProb)*awayProb*(1-homeProb)*homeProb
    totalProb += (1-homeProb)*homeProb*awayProb*(1-awayProb)*(1-awayProb)*homeProb*homeProb        
    totalProb += (1-homeProb)*homeProb*(1-awayProb)*awayProb*awayProb*homeProb
    totalProb += (1-homeProb)*homeProb*(1-awayProb)*awayProb*awayProb*(1-homeProb)*homeProb
    totalProb += (1-homeProb)*homeProb*(1-awayProb)*awayProb*(1-awayProb)*homeProb*homeProb
    totalProb += (1-homeProb)*homeProb*(1-awayProb)*(1-awayProb)*awayProb*homeProb*homeProb    
    totalProb += (1-homeProb)*(1-homeProb)*awayProb*awayProb*awayProb*homeProb
    totalProb += (1-homeProb)*(1-homeProb)*awayProb*awayProb*awayProb*(1-homeProb)*homeProb
    totalProb += (1-homeProb)*(1-homeProb)*awayProb*awayProb*(1-awayProb)*homeProb*homeProb
    totalProb += (1-homeProb)*(1-homeProb)*awayProb*(1-awayProb)*awayProb*homeProb*homeProb    
    totalProb += (1-homeProb)*(1-homeProb)*(1-awayProb)*awayProb*awayProb*homeProb*homeProb

    return totalProb

def GetSeries7Prob10(homeProb, awayProb):
    totalProb = homeProb*awayProb*awayProb    
    totalProb += homeProb*awayProb*(1-awayProb)*awayProb
    totalProb += homeProb*awayProb*(1-awayProb)*(1-awayProb)*homeProb
    totalProb += homeProb*awayProb*(1-awayProb)*(1-awayProb)*(1-homeProb)*homeProb    
    totalProb += homeProb*(1-awayProb)*awayProb*awayProb
    totalProb += homeProb*(1-awayProb)*awayProb*(1-awayProb)*homeProb
    totalProb += homeProb*(1-awayProb)*awayProb*(1-awayProb)*(1-homeProb)*homeProb
    totalProb += homeProb*(1-awayProb)*(1-awayProb)*awayProb*homeProb
    totalProb += homeProb*(1-awayProb)*(1-awayProb)*awayProb*(1-awayProb)*homeProb
    totalProb += homeProb*(1-awayProb)*(1-awayProb)*(1-awayProb)*homeProb*homeProb    
    totalProb += (1-homeProb)*awayProb*awayProb*awayProb
    totalProb += (1-homeProb)*awayProb*awayProb*(1-awayProb)*homeProb
    totalProb += (1-homeProb)*awayProb*awayProb*(1-awayProb)*(1-homeProb)*homeProb
    totalProb += (1-homeProb)*awayProb*(1-awayProb)*awayProb*homeProb
    totalProb += (1-homeProb)*awayProb*(1-awayProb)*awayProb*(1-awayProb)*homeProb
    totalProb += (1-homeProb)*awayProb*(1-awayProb)*(1-awayProb)*homeProb*homeProb      
    totalProb += (1-homeProb)*(1-awayProb)*awayProb*awayProb*homeProb
    totalProb += (1-homeProb)*(1-awayProb)*awayProb*awayProb*(1-homeProb)*homeProb
    totalProb += (1-homeProb)*(1-awayProb)*awayProb*(1-awayProb)*homeProb*homeProb
    totalProb += (1-homeProb)*(1-awayProb)*(1-awayProb)*awayProb*homeProb*homeProb  
    return totalProb

def GetSeries7Prob01(homeProb, awayProb):
    totalProb = homeProb*awayProb*awayProb*awayProb    
    totalProb += homeProb*awayProb*awayProb*(1-awayProb)*homeProb
    totalProb += homeProb*awayProb*awayProb*(1-awayProb)*(1-homeProb)*homeProb    
    totalProb += homeProb*awayProb*(1-awayProb)*awayProb*homeProb
    totalProb += homeProb*awayProb*(1-awayProb)*awayProb*(1-homeProb)*homeProb
    totalProb += homeProb*awayProb*(1-awayProb)*(1-awayProb)*homeProb*homeProb        
    totalProb += homeProb*(1-awayProb)*awayProb*awayProb*homeProb
    totalProb += homeProb*(1-awayProb)*awayProb*awayProb*(1-homeProb)*homeProb
    totalProb += homeProb*(1-awayProb)*awayProb*(1-awayProb)*homeProb*homeProb
    totalProb += homeProb*(1-awayProb)*(1-awayProb)*awayProb*homeProb*homeProb    
    totalProb += (1-homeProb)*awayProb*awayProb*awayProb*homeProb
    totalProb += (1-homeProb)*awayProb*awayProb*awayProb*(1-homeProb)*homeProb
    totalProb += (1-homeProb)*awayProb*awayProb*(1-awayProb)*homeProb*homeProb
    totalProb += (1-homeProb)*awayProb*(1-awayProb)*awayProb*homeProb*homeProb    
    totalProb += (1-homeProb)*(1-awayProb)*awayProb*awayProb*homeProb*homeProb
    return totalProb

def GetSeries7Prob11(homeProb, awayProb):
    totalProb = awayProb*awayProb*awayProb
    totalProb += awayProb*awayProb*(1-awayProb)*homeProb
    totalProb += awayProb*awayProb*(1-awayProb)*(1-homeProb)*homeProb
    totalProb += awayProb*(1-awayProb)*awayProb*homeProb
    totalProb += awayProb*(1-awayProb)*awayProb*(1-awayProb)*homeProb
    totalProb += awayProb*(1-awayProb)*(1-awayProb)*homeProb*homeProb      
    totalProb += (1-awayProb)*awayProb*awayProb*homeProb
    totalProb += (1-awayProb)*awayProb*awayProb*(1-homeProb)*homeProb
    totalProb += (1-awayProb)*awayProb*(1-awayProb)*homeProb*homeProb
    totalProb += (1-awayProb)*(1-awayProb)*awayProb*homeProb*homeProb  
    return totalProb

def GetSeries7Prob21(homeProb, awayProb):
    totalProb = awayProb*awayProb
    totalProb += awayProb*(1-awayProb)*homeProb
    totalProb += awayProb*(1-awayProb)*(1-homeProb)*homeProb
    totalProb += (1-awayProb)*awayProb*homeProb
    totalProb += (1-awayProb)*awayProb*(1-awayProb)*homeProb
    totalProb += (1-awayProb)*(1-awayProb)*homeProb*homeProb      
    return totalProb

def GetSeries7Prob31(homeProb, awayProb):
    totalProb = awayProb
    totalProb += (1-awayProb)*homeProb
    totalProb += (1-awayProb)*(1-homeProb)*homeProb    
    return totalProb

def GetSeries7Prob22(homeProb, awayProb):
    totalProb = awayProb*homeProb
    totalProb += awayProb*(1-awayProb)*homeProb
    totalProb += (1-awayProb)*homeProb*homeProb      
    return totalProb

def GetSeries7Prob23(homeProb, awayProb):
    totalProb = homeProb*homeProb      
    return totalProb

def GetSeries7Prob33(homeProb, awayProb):
    totalProb = homeProb    
    return totalProb

##################################################################################
    
#HOUBOS
bosHome1 = MLBWinProbability('BOS', 'HOU', xmlStandingsOnDate, lastYearStandingsOnDate)
bosAway1 = 1 - MLBWinProbability('HOU', 'BOS', xmlStandingsOnDate, lastYearStandingsOnDate)
bosHome2 = RunsSimulator(bos2018, hou2018, True, numSims, 4)
bosAway2 = 1 - RunsSimulator(hou2018, bos2018, True, numSims, 4)
five381013 = MLB538WinProbability('BOS', 'HOU', datetime(2018, 10, 13), eloDF)
five381014 = MLB538WinProbability('BOS', 'HOU', datetime(2018, 10, 14), eloDF)
five381016 = 1 - MLB538WinProbability('HOU', 'BOS', datetime(2018, 10, 16), eloDF)
five381017 = 1 - MLB538WinProbability('HOU', 'BOS', datetime(2018, 10, 17), eloDF)
five381018 = 1 - MLB538WinProbability('HOU', 'BOS', datetime(2018, 10, 18), eloDF)
print(bosAway1)
print(bosAway2)
print(five381018)

print(GetSeries7Prob31(bosHome1,bosAway1))
print(GetSeries7Prob31(bosHome2,bosAway2))

#MILLAD
milHome1 = MLBWinProbability('MIL', 'LAD', xmlStandingsOnDate, lastYearStandingsOnDate)
milAway1 = 1 - MLBWinProbability('LAD', 'MIL', xmlStandingsOnDate, lastYearStandingsOnDate)
milHome2 = RunsSimulator(mil2018, lad2018, True, numSims, 4)
milAway2 = 1 - RunsSimulator(lad2018, mil2018, True, numSims, 4)
five381012 = MLB538WinProbability('MIL', 'LAD', datetime(2018, 10, 12), eloDF)
five381013 = MLB538WinProbability('MIL', 'LAD', datetime(2018, 10, 13), eloDF)
five381015 = 1-MLB538WinProbability('LAD', 'MIL', datetime(2018, 10, 15), eloDF)
five381016 = 1-MLB538WinProbability('LAD', 'MIL', datetime(2018, 10, 16), eloDF)
five381017 = 1-MLB538WinProbability('LAD', 'MIL', datetime(2018, 10, 17), eloDF)
five381019 = MLB538WinProbability('MIL', 'LAD', datetime(2018, 10, 19), eloDF)
five381020 = MLB538WinProbability('MIL', 'LAD', datetime(2018, 10, 20), eloDF)

print(milHome1)
print(milHome2)
print(five381020)

print(GetSeries7Prob33(milHome1,milAway1))
print(GetSeries7Prob33(milHome2,milAway2))
