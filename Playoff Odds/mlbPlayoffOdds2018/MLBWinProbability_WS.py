# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 16:29:59 2018

@author: ABooth
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 16:46:47 2018

@author: ABooth
"""

import pandas as pd
from datetime import datetime
from scipy.stats import beta
import numpy as np
from xmlstats import xmlstats

access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
user_agent = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

def MLBWinProbability(homeTeamAbbr, awayTeamAbbr, home2018DF, away2018DF):
    #MLB Home Field Single Game Neutral Site
    betterTeamWinPercConstant = 0.56
    
    #read data
    beta18Pre = pd.read_csv("https://raw.githubusercontent.com/ABoothInTheWild/baseball-research/master/Playoff%20Odds/mlbPlayoffOdds2018/mlb2018PreSeasonBetaEstimates.csv")

    #Get Home Team Stats
    homeTeamHomeWins = len(home2018DF[(home2018DF["Home/Away"] == 0) & (home2018DF["Won"] == 1)]["Won"])
    homeTeamHomeLosses = len(home2018DF[(home2018DF["Home/Away"] == 0) & (home2018DF["Won"] == 0)]["Won"])
    homeTeamTotalWins = len(home2018DF[(home2018DF["Won"] == 1)]["Won"])
    homeTeamTotalLosses = len(home2018DF[(home2018DF["Won"] == 0)]["Won"])
    
    #Get Away Team Stats
    awayTeamAwayWins = len(away2018DF[(away2018DF["Home/Away"] == 1) & (away2018DF["Won"] == 1)]["Won"])
    awayTeamAwayLosses = len(away2018DF[(away2018DF["Home/Away"] == 1) & (away2018DF["Won"] == 0)]["Won"])
    awayTeamTotalWins = len(away2018DF[(away2018DF["Won"] == 1)]["Won"])
    awayTeamTotalLosses = len(away2018DF[(away2018DF["Won"] == 0)]["Won"])
    
    #mappings
    homeTeamAbbr1 = homeTeamAbbr
    awayTeamAbbr1 = awayTeamAbbr
    if homeTeamAbbr == "FLA":
        homeTeamAbbr1 = "MIA"
    if homeTeamAbbr == "ANA":
        homeTeamAbbr1 = "LAA"
    if homeTeamAbbr == "TBD":
        homeTeamAbbr1 = "TBR"
    if awayTeamAbbr == "FLA":
        awayTeamAbbr1 = "MIA"
    if awayTeamAbbr == "ANA":
        awayTeamAbbr1 = "LAA"
    if awayTeamAbbr == "TBD":
        awayTeamAbbr1 = "TBR"
    
    #get posteriors
    homePostA = beta18Pre[beta18Pre.Team_Abbr == homeTeamAbbr1]["PriorAlpha"].values[0] + homeTeamTotalWins
    homePostB = beta18Pre[beta18Pre.Team_Abbr == homeTeamAbbr1]["PriorBeta"].values[0] + homeTeamTotalLosses
    awayPostA = beta18Pre[beta18Pre.Team_Abbr == awayTeamAbbr1]["PriorAlpha"].values[0] + awayTeamTotalWins
    awayPostB = beta18Pre[beta18Pre.Team_Abbr == awayTeamAbbr1]["PriorBeta"].values[0] + awayTeamTotalLosses

    #Determine Probability of Better Team
    ntrials=100000
    np.random.seed(seed=54321)
    homeSample = beta.rvs(homePostA, homePostB, size=ntrials)
    awaySample = beta.rvs(awayPostA, awayPostB, size=ntrials)    
    homeBetter = np.sum(homeSample > awaySample)/ntrials
    awayBetter = 1 - homeBetter
    
    #home field advantage        
    #homeTeam
    #homeTeamHomeWP = homeTeamHomeWins / (homeTeamHomeWins + homeTeamHomeLosses)
    #homeTeamAwayWP = (homeTeamTotalWins - homeTeamHomeWins) / (homeTeamTotalWins + homeTeamTotalLosses - homeTeamHomeWins - homeTeamHomeLosses)
    homeTeamHomeWP = ((sum(home2018DF[(home2018DF["Home/Away"] == 0)]["R"])**2)/((sum(home2018DF[(home2018DF["Home/Away"] == 0)]["R"])**2) + (sum(home2018DF[(home2018DF["Home/Away"] == 0)]["RA"])**2)))
    homeTeamAwayWP = ((sum(home2018DF[(home2018DF["Home/Away"] == 1)]["R"])**2)/((sum(home2018DF[(home2018DF["Home/Away"] == 1)]["R"])**2) + (sum(home2018DF[(home2018DF["Home/Away"] == 1)]["RA"])**2)))
    homeTeamAdv = (homeTeamHomeWP - (homeTeamHomeWP+homeTeamAwayWP)/2) / ((homeTeamHomeWP+homeTeamAwayWP)/2)
    
    #AwayTeam
    #awayTeamAwayWP = awayTeamAwayWins / (awayTeamAwayWins + awayTeamAwayLosses)
    #awayTeamHomeWP = (awayTeamTotalWins - awayTeamAwayWins) / (awayTeamTotalWins + awayTeamTotalLosses - awayTeamAwayWins - awayTeamAwayLosses)
    awayTeamHomeWP = ((sum(away2018DF[(away2018DF["Home/Away"] == 0)]["R"])**2)/((sum(away2018DF[(away2018DF["Home/Away"] == 0)]["R"])**2) + (sum(away2018DF[(away2018DF["Home/Away"] == 0)]["RA"])**2)))
    awayTeamAwayWP = ((sum(away2018DF[(away2018DF["Home/Away"] == 1)]["R"])**2)/((sum(away2018DF[(away2018DF["Home/Away"] == 1)]["R"])**2) + (sum(away2018DF[(away2018DF["Home/Away"] == 1)]["RA"])**2)))
    awayTeamAdv = (awayTeamAwayWP - (awayTeamAwayWP+awayTeamHomeWP)/2) / ((awayTeamAwayWP+awayTeamHomeWP)/2)
    
    #Advantage
    #advantage = 1 + (homeTeamAdv - awayTeamAdv)/2 #average
    #advantage = 1 + (homeTeamAdv - awayTeamAdv) #sum
    homeAdvantage = 1 + homeTeamAdv
    awayAdvantage = 1 + awayTeamAdv
    
    #Win Probability
    winProbabilityHomeWins = (homeBetter*betterTeamWinPercConstant + awayBetter*(1-betterTeamWinPercConstant)) * homeAdvantage
    winProbabilityAwayLoses = 1 - (awayBetter*betterTeamWinPercConstant + homeBetter*(1-betterTeamWinPercConstant)) * awayAdvantage
    winProbabilityHome = .5*winProbabilityHomeWins + .5*winProbabilityAwayLoses
    
    return winProbabilityHome
