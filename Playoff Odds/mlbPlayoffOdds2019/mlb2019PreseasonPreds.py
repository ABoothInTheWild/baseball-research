# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 11:59:04 2019

@author: ABooth
"""

# -*- coding: utf-8 -*-
"""
Created on Thurs July 11 2019

@author: abooth
"""

#Imports
import pandas as pd
import os
import numpy as np
from scipy.stats import beta

os.chdir('C:/Users/abooth/Documents/Python Scripts/PastPreds/mlbPlayoffOdds2019')

#Load Data
mlb18 = pd.read_csv('Mlb_2018_SeasonStandings.csv')
mlb19Pre = pd.read_csv('Mlb_2019_PreseasonWins.csv')

#Get personal games to regress by
beta19Pre = mlb19Pre.copy(deep=True)
beta19Pre["luckSD"] = np.sqrt((beta19Pre.WinnPerc * (1-beta19Pre.WinnPerc))/
         beta19Pre.RegGames)
beta19Pre["Mlb2018SD"] = np.std(mlb18["W-L%"])
beta19Pre["TalentVar"] = beta19Pre.Mlb2018SD**2 - beta19Pre.luckSD**2
beta19Pre["RegrGames"] = (beta19Pre.WinnPerc * (1-beta19Pre.WinnPerc))/beta19Pre.TalentVar

print(np.allclose(np.sqrt((beta19Pre.WinnPerc * (1-beta19Pre.WinnPerc))/
                  beta19Pre.RegrGames), np.sqrt(beta19Pre.TalentVar))) #TRUE

#get personalized priors
beta19Pre["PriorAlpha"] = beta19Pre.RegrGames * beta19Pre.WinnPerc
beta19Pre["PriorBeta"] = beta19Pre.RegrGames * (1-beta19Pre.WinnPerc)

print(np.mean(beta19Pre.RegrGames)) #38.6

##############################################################################

#Get win estimate and CIs for all teams

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
for team in beta19Pre.Team_Abbr.values:
    priorA = beta19Pre[beta19Pre.Team_Abbr == team]["PriorAlpha"].values[0]
    priorB = beta19Pre[beta19Pre.Team_Abbr == team]["PriorBeta"].values[0]
    #priorA = avgRegrGames * avg2016WP
    #priorB = avgRegrGames * (1-avg2016WP)
    
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
beta19Pre["Beta_Estimate"] = winPercBeta
beta19Pre["80CI_Low"] = ci80Low
beta19Pre["80CI_High"] = ci80High
beta19Pre["90CI_Low"] = ci90Low
beta19Pre["90CI_High"] = ci90High
beta19Pre["95CI_Low"] = ci95Low
beta19Pre["95CI_High"] = ci95High
beta19Pre["99CI_Low"] = ci99Low
beta19Pre["99CI_High"] = ci99High

#turn win percentages into regular season win estimates
beta19Pre["Beta_Wins"] = np.round(beta19Pre.Beta_Estimate * beta19Pre.RegGames,1)

beta19Pre["80CI_Low_Wins"] = np.round(beta19Pre["80CI_Low"] * beta19Pre.RegGames,1)
beta19Pre["80CI_High_Wins"] = np.round(beta19Pre["80CI_High"] * beta19Pre.RegGames,1)
beta19Pre["90CI_Low_Wins"] = np.round(beta19Pre["90CI_Low"] * beta19Pre.RegGames,1)
beta19Pre["90CI_High_Wins"] = np.round(beta19Pre["90CI_High"] * beta19Pre.RegGames,1)
beta19Pre["95CI_Low_Wins"] = np.round(beta19Pre["95CI_Low"] * beta19Pre.RegGames,1)
beta19Pre["95CI_High_Wins"] = np.round(beta19Pre["95CI_High"] * beta19Pre.RegGames,1)
beta19Pre["99CI_Low_Wins"] = np.round(beta19Pre["99CI_Low"] * beta19Pre.RegGames,1)
beta19Pre["99CI_High_Wins"] = np.round(beta19Pre["99CI_High"] * beta19Pre.RegGames,1)

         
beta19Pre.to_csv("mlb2019PreSeasonBetaEstimates.csv", index=False)