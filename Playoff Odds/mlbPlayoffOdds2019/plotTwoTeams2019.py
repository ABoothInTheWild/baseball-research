# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 13:45:21 2019

@author: ABooth
"""

##########################################################################

#Graphing Beta Distribution Example

#Reference:
#https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.stats.beta.html

from scipy.stats import beta
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np
from xmlstats import xmlstats
import os

access_token = '0aabe405-8ec2-4c0c-8e8b-39e164d7e7ca'
user_agent = 'adbooth01@gmail.com'

#read data
os.chdir('C:/Users/abooth/Documents/Python Scripts/PastPreds/mlbPlayoffOdds2019')
beta19Pre = pd.read_csv("mlb2019PreSeasonBetaEstimates.csv")

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
    
stats = xmlstats.Xmlstats(access_token, user_agent)
date_format = datetime.today().strftime("%Y%m%d")    
standingsOnDate = stats.standings(date=date_format, sport="mlb")

#Teams
homeTeamAbbr = "TEX"
awayTeamAbbr = "HOU"

#Set seed, init plots, get beta parameters
np.random.seed(seed=12345)

#Get Home Team Stats
homeTeam = teamAbbrsToId[homeTeamAbbr]
homeStanding = [standing for standing in standingsOnDate.standing if standing.team_id == homeTeam][0]
homeTeamTotalWins = homeStanding.won
homeTeamTotalLosses = homeStanding.lost

homePostA = beta19Pre[beta19Pre.Team_Abbr == homeTeamAbbr]["PriorAlpha"].values[0] + homeTeamTotalWins
homePostB = beta19Pre[beta19Pre.Team_Abbr == homeTeamAbbr]["PriorBeta"].values[0] + homeTeamTotalLosses

#Get Away Team Stats
awayTeam = teamAbbrsToId[awayTeamAbbr]
awayStanding = [standing for standing in standingsOnDate.standing if standing.team_id == awayTeam][0]
awayTeamTotalWins = awayStanding.won
awayTeamTotalLosses = awayStanding.lost

awayPostA = beta19Pre[beta19Pre.Team_Abbr == awayTeamAbbr]["PriorAlpha"].values[0] + awayTeamTotalWins
awayPostB = beta19Pre[beta19Pre.Team_Abbr == awayTeamAbbr]["PriorBeta"].values[0] + awayTeamTotalLosses

#Plot pdf
x = np.linspace(beta.ppf(0.001, homePostA , homePostB),
              beta.ppf(0.999, homePostA , homePostB), 1000)
y = np.linspace(beta.ppf(0.001, awayPostA , awayPostB),
              beta.ppf(0.999, awayPostA , awayPostB), 1000)

#Check pdf vs cdf
vals = beta.ppf([0.001, 0.5, 0.999], homePostA , homePostB)
print(np.allclose([0.001, 0.5, 0.999], beta.cdf(vals, homePostA , homePostB))) #True
vals1 = beta.ppf([0.001, 0.5, 0.999], awayPostA , awayPostB)
print(np.allclose([0.001, 0.5, 0.999], beta.cdf(vals1, awayPostA , awayPostB))) #True

#Make plot pretty
fig, ax = plt.subplots(1, 1)
ax.plot(x, beta.pdf(x, homePostA , homePostB),
         'r-', lw=5, alpha=0.6, label= homeTeamAbbr + ' WP%')
ax.plot(y, beta.pdf(y, awayPostA , awayPostB),
         'b-', lw=5, alpha=0.6, label= awayTeamAbbr + ' WP%')
ax.legend(loc='best', frameon=False)
ax.set_xlim([0.4, 0.8])
ax.set_ylim([0, 14])
plt.title(homeTeamAbbr + ' vs ' + awayTeamAbbr + ' WP% Beta Estimate')
plt.ylabel('Density')
plt.xlabel('Winning Percentage')
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()