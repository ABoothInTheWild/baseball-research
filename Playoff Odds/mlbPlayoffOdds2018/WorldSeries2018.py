# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 15:25:30 2018

@author: ABooth
"""

import os
os.chdir("C:/Users/abooth/Documents/Python Scripts/PastPreds/mlbPlayoffOdds2018")

from MLBWinProbability_WS import *
from MLB538WinProbability import *
from RunsScoredAllowedSimulator import *
import pandas as pd
import numpy as np

eloDF = pd.read_csv("https://projects.fivethirtyeight.com/mlb-api/mlb_elo.csv")
eloDF = eloDF[eloDF.season == 2018]
eloDF.date = pd.to_datetime(eloDF.date)
eloDF = eloDF.sort_values(["date"]).reset_index(drop=True)

lad2018 = ImportRunsScoredAllowedDF("LAD_2018_RegularSeason.csv")
bos2018 = ImportRunsScoredAllowedDF("BOS_2018_RegularSeason.csv")
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

##################################################################################
    
#LADBOS
bosHome1 = MLBWinProbability('BOS', 'LAD', bos2018, lad2018)
bosAway1 = 1 - MLBWinProbability('LAD', 'BOS', lad2018, bos2018)
bosHome2 = RunsSimulator(bos2018, lad2018, True, numSims, 4)
bosAway2 = 1 - RunsSimulator(lad2018, bos2018, True, numSims, 4)
five381023 = MLB538WinProbability('BOS', 'LAD', datetime(2018, 10, 23), eloDF)

print(bosHome1)
print(bosHome2)
print(five381023)

print(GetSeries7Prob00(bosHome1,bosAway1))
print(GetSeries7Prob00(bosHome2,bosAway2))