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

access_token = 'a02014c0-9f69-4bf7-b9ac-4d804dfe58a3'
user_agent = 'adbooth01@gmail.com'
    
def MLBWinProbability(homeTeamAbbr, awayTeamAbbr, standingsOnDate, lastYearStandingsOnDate, override=False, inpDate = datetime(2018, 3, 29), homeAdditionalHomeWins=0, homeAdditionalHomeLosses=0, homeAdditionalTotalWins=0, homeAdditionalTotalLosses=0, awayAdditionalAwayWins=0, awayAdditionalAwayLosses=0, awayAdditionalTotalWins=0, awayAdditionalTotalLosses=0):
    #MLB Home Field Single Game Neutral Site
    betterTeamWinPercConstant = 0.56
    
    #TeamAbbrToXMLSTATSId
    teamAbbrsToId = {'CLE':'cleveland-indians',
     'MIN':'minnesota-twins',
     'DET':'detroit-tigers',
     'CHW':'chicago-white-sox',
     'KCR':'kansas-city-royals',
     'BOS': 'boston-red-sox',
     'NYY':'new-york-yankees',
     'TBR':'tampa-bay-rays',
     'TBD':'tampa-bay-rays',
     'TOR':'toronto-blue-jays',
     'BAL':'baltimore-orioles',
     'HOU':'houston-astros',
     'OAK':'oakland-athletics',
     'SEA': 'seattle-mariners',
     'LAA':'los-angeles-angels',
     'ANA':'los-angeles-angels',
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
     'FLA':'miami-marlins',
     'LAD':'los-angeles-dodgers',
     'COL':'colorado-rockies',
     'ARI':'arizona-diamondbacks',
     'SFG':'san-francisco-giants',
     'SDP':'san-diego-padres'}
    
    #read data
    beta18Pre = pd.read_csv("https://raw.githubusercontent.com/ABoothInTheWild/baseball-research/master/Playoff%20Odds/mlbPlayoffOdds2018/mlb2018PreSeasonBetaEstimates.csv")
    
    if override:
        stats = xmlstats.Xmlstats(access_token, user_agent)
        date_format = inpDate.strftime("%Y%m%d")    
        standingsOnDate = stats.standings(date=date_format, sport="mlb")
    
    #Get Home Team Stats
    homeTeam = teamAbbrsToId[homeTeamAbbr]
    homeStanding = [standing for standing in standingsOnDate.standing if standing.team_id == homeTeam][0]
    homeTeamHomeWins = homeStanding.home_won + homeAdditionalHomeWins
    homeTeamHomeLosses = homeStanding.home_lost + homeAdditionalHomeLosses
    homeTeamTotalWins = homeStanding.won + homeAdditionalTotalWins
    homeTeamTotalLosses = homeStanding.lost + homeAdditionalTotalLosses
    
    #Get Away Team Stats
    awayTeam = teamAbbrsToId[awayTeamAbbr]
    awayStanding = [standing for standing in standingsOnDate.standing if standing.team_id == awayTeam][0]
    awayTeamAwayWins = awayStanding.away_won + awayAdditionalAwayWins
    awayTeamAwayLosses = awayStanding.away_lost + awayAdditionalAwayLosses
    awayTeamTotalWins = awayStanding.won + awayAdditionalTotalWins
    awayTeamTotalLosses = awayStanding.lost + awayAdditionalTotalLosses
    
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
    minHomeGames = np.round((beta18Pre[beta18Pre.Team_Abbr == homeTeamAbbr1]["PriorAlpha"].values[0] + beta18Pre[beta18Pre.Team_Abbr == homeTeamAbbr1]["PriorBeta"].values[0])/2, 0)
    minAwayGames = np.round((beta18Pre[beta18Pre.Team_Abbr == awayTeamAbbr1]["PriorAlpha"].values[0] + beta18Pre[beta18Pre.Team_Abbr == awayTeamAbbr1]["PriorBeta"].values[0])/2, 0)
    
    #Determine Probability of Better Team
    ntrials=100000
    np.random.seed(seed=54321)
    homeSample = beta.rvs(homePostA, homePostB, size=ntrials)
    awaySample = beta.rvs(awayPostA, awayPostB, size=ntrials)    
    homeBetter = np.sum(homeSample > awaySample)/ntrials
    awayBetter = 1 - homeBetter
    
    #home field advantage
    #Get 2017 stats if not played enough in 2018
    if (homeTeamHomeWins + homeTeamHomeLosses <= minHomeGames):
        #Get Home Team Stats
        homeStanding = [standing for standing in lastYearStandingsOnDate.standing if standing.team_id == homeTeam][0]
        homeTeamHomeWins = homeStanding.home_won + homeAdditionalHomeWins
        homeTeamHomeLosses = homeStanding.home_lost + homeAdditionalHomeLosses
        homeTeamTotalWins = homeStanding.won + homeAdditionalTotalWins
        homeTeamTotalLosses = homeStanding.lost + homeAdditionalTotalLosses
    if (awayTeamAwayWins + awayTeamAwayLosses <= minAwayGames):
        #Get Away Team Stats
        awayStanding = [standing for standing in lastYearStandingsOnDate.standing if standing.team_id == awayTeam][0]
        awayTeamAwayWins = awayStanding.away_won + awayAdditionalAwayWins
        awayTeamAwayLosses = awayStanding.away_lost + awayAdditionalAwayLosses
        awayTeamTotalWins = awayStanding.won + awayAdditionalTotalWins
        awayTeamTotalLosses = awayStanding.lost + awayAdditionalTotalLosses
        
    #homeTeam
    homeTeamHomeWP = homeTeamHomeWins / (homeTeamHomeWins + homeTeamHomeLosses)
    homeTeamAwayWP = (homeTeamTotalWins - homeTeamHomeWins) / (homeTeamTotalWins + homeTeamTotalLosses - homeTeamHomeWins - homeTeamHomeLosses)
    homeTeamAdv = (homeTeamHomeWP - (homeTeamHomeWP+homeTeamAwayWP)/2) / ((homeTeamHomeWP+homeTeamAwayWP)/2)
    
    #AwayTeam
    awayTeamAwayWP = awayTeamAwayWins / (awayTeamAwayWins + awayTeamAwayLosses)
    awayTeamHomeWP = (awayTeamTotalWins - awayTeamAwayWins) / (awayTeamTotalWins + awayTeamTotalLosses - awayTeamAwayWins - awayTeamAwayLosses)
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


#MLBWinProbability('NYY', 'OAK', np.NAN, np.NAN, True, datetime.today())
