# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 13:36:12 2018

@author: ABooth
"""

from scipy.stats import beta
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np

#read data
os.chdir('C:/Users/abooth/Documents/Python Scripts/PastPreds/mlbPlayoffOdds2018')
beta18Pre = pd.read_csv("mlb2018PreSeasonBetaEstimates.csv")
mlb18Results = pd.read_csv("mlb2018SeasonResults.csv")

teamAbbr = "MIA"

#Set seed, init plots, get beta parameters
np.random.seed(seed=12345)
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
priorA = beta18Pre[beta18Pre.Team_Abbr == teamAbbr]["PriorAlpha"].values[0]
priorB = beta18Pre[beta18Pre.Team_Abbr == teamAbbr]["PriorBeta"].values[0]

teamWins = mlb18Results[mlb18Results.Team_Abbr == teamAbbr].iloc[0]["Wins_20180830"]
teamLosses =  mlb18Results[mlb18Results.Team_Abbr == teamAbbr].iloc[0]["Losses_20180830"]

postA = teamWins + priorA
postB = teamLosses + priorB

#Plot pdf
x = np.linspace(beta.ppf(0.001, postA, postB),
              beta.ppf(0.999, postA, postB), 1000)
ax.plot(x, beta.pdf(x, postA, postB),
         'r-', lw=5, alpha=0.6, label='beta pdf')

#Make plot pretty
ax.legend(loc='best', frameon=False)
ax.set_xlim([0.25, 0.75])
ax.set_ylim([0, 13])
plt.title(teamAbbr + ' 8/30/2018 WP% Beta Estimate')
plt.ylabel('Density')
plt.xlabel('Winning Percentage')
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
#fig.savefig(teamAbbr + "826PosteriorWP.png", bbox_inches='tight')

#where the magic happens
np.random.seed(seed=12345)
sample = beta.rvs(postA, postB, size=100000)
gamesLeft = 162 - teamWins - teamLosses
winEstimate = np.round(teamWins + sample*gamesLeft,0)
print(np.mean(winEstimate))
print(np.percentile(winEstimate, 2.5))
print(np.percentile(winEstimate, 97.5))

print(np.mean(sample))
print(np.percentile(sample, 2.5))
print(np.percentile(sample, 97.5))


wins100 = 100 - teamWins
losses100 = 100 - teamLosses

#print(wins100/np.mean(sample))
#print(wins100/np.percentile(sample, 2.5))
#print(wins100/np.percentile(sample, 97.5))


print(losses100/(1-np.mean(sample)))
print(losses100/(1-np.percentile(sample, 2.5)))
print(losses100/(1-np.percentile(sample, 97.5)))

prob = len(winEstimate[winEstimate <= 62])/float(100000)
print(prob)

