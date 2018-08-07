# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 15:33:12 2018

@author: abooth
"""

#Imports
import pandas as pd
import os
import numpy as np
from scipy.stats import beta

os.chdir('C:/Users/abooth/Documents/Python Scripts/PastPreds/2018')

#Load Data
mlb17 = pd.read_csv('Mlb_2017_SeasonStandings.csv')
mlb18Pre = pd.read_csv('Mlb_2018_PreseasonWins.csv')

#Get personal games to regress by
beta18Pre = mlb18Pre.copy(deep=True)
beta18Pre["luckSD"] = np.sqrt((beta18Pre.WinnPerc * (1-beta18Pre.WinnPerc))/
         beta18Pre.RegGames)
beta18Pre["Mlb2017SD"] = np.std(mlb17["W-L%"])
beta18Pre["TalentVar"] = beta18Pre.Mlb2017SD**2 - beta18Pre.luckSD**2
beta18Pre["RegrGames"] = (beta18Pre.WinnPerc * (1-beta18Pre.WinnPerc))/beta18Pre.TalentVar

print(np.allclose(np.sqrt((beta18Pre.WinnPerc * (1-beta18Pre.WinnPerc))/
                  beta18Pre.RegrGames), np.sqrt(beta18Pre.TalentVar))) #TRUE

#get personalized priors
beta18Pre["PriorAlpha"] = beta18Pre.RegrGames * beta18Pre.WinnPerc
beta18Pre["PriorBeta"] = beta18Pre.RegrGames * (1-beta18Pre.WinnPerc)

print(np.mean(beta18Pre.RegrGames)) #72.9

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
for team in beta18Pre.Team_Abbr.values:
    priorA = beta18Pre[beta18Pre.Team_Abbr == team]["PriorAlpha"].values[0]
    priorB = beta18Pre[beta18Pre.Team_Abbr == team]["PriorBeta"].values[0]
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
beta18Pre["Beta_Estimate"] = winPercBeta
beta18Pre["80CI_Low"] = ci80Low
beta18Pre["80CI_High"] = ci80High
beta18Pre["90CI_Low"] = ci90Low
beta18Pre["90CI_High"] = ci90High
beta18Pre["95CI_Low"] = ci95Low
beta18Pre["95CI_High"] = ci95High
beta18Pre["99CI_Low"] = ci99Low
beta18Pre["99CI_High"] = ci99High

#turn win percentages into regular season win estimates
beta18Pre["Beta_Wins"] = np.round(beta18Pre.Beta_Estimate * beta18Pre.RegGames,1)

beta18Pre["80CI_Low_Wins"] = np.round(beta18Pre["80CI_Low"] * beta18Pre.RegGames,1)
beta18Pre["80CI_High_Wins"] = np.round(beta18Pre["80CI_High"] * beta18Pre.RegGames,1)
beta18Pre["90CI_Low_Wins"] = np.round(beta18Pre["90CI_Low"] * beta18Pre.RegGames,1)
beta18Pre["90CI_High_Wins"] = np.round(beta18Pre["90CI_High"] * beta18Pre.RegGames,1)
beta18Pre["95CI_Low_Wins"] = np.round(beta18Pre["95CI_Low"] * beta18Pre.RegGames,1)
beta18Pre["95CI_High_Wins"] = np.round(beta18Pre["95CI_High"] * beta18Pre.RegGames,1)
beta18Pre["99CI_Low_Wins"] = np.round(beta18Pre["99CI_Low"] * beta18Pre.RegGames,1)
beta18Pre["99CI_High_Wins"] = np.round(beta18Pre["99CI_High"] * beta18Pre.RegGames,1)

         
beta18Pre.to_csv("mlb2018PreSeasonBetaEstimates.csv", index=False)