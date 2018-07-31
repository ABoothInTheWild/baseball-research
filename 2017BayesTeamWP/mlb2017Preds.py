# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 20:15:56 2018

@author: Alexander
"""

#Imports
import pandas as pd
import os
import numpy as np

os.chdir('C:/Users/Alexander/Documents/baseball/Past Perf Playoffs')

#Load Data
mlb16 = pd.read_csv('Mlb_2016_SeasonStandings.csv')
mlb17Pre = pd.read_csv('Mlb_2017_PreseasonWins.csv')

#Get personal games to regress by
beta17Pre = mlb17Pre.copy(deep=True)
beta17Pre["luckSD"] = np.sqrt((beta17Pre.WinnPerc * (1-beta17Pre.WinnPerc))/
         beta17Pre.RegGames)
beta17Pre["Mlb2016SD"] = np.std(mlb16["W-L%"])
beta17Pre["TalentVar"] = beta17Pre.Mlb2016SD**2 - beta17Pre.luckSD**2
beta17Pre["RegrGames"] = (beta17Pre.WinnPerc * (1-beta17Pre.WinnPerc))/beta17Pre.TalentVar

print(all(np.sqrt((beta17Pre.WinnPerc * (1-beta17Pre.WinnPerc))/
                  beta17Pre.RegrGames) == np.sqrt(beta17Pre.TalentVar))) #TRUE

#get personalized priors
beta17Pre["PriorAlpha"] = beta17Pre.RegrGames * beta17Pre.WinnPerc
beta17Pre["PriorBeta"] = beta17Pre.RegrGames * (1-beta17Pre.WinnPerc)

print(np.mean(beta17Pre.RegrGames)) #91.6

###################################################################

#Graphing Beta Distribution Example

#Reference:
#https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.stats.beta.html

from scipy.stats import beta
import matplotlib.pyplot as plt

#SF Giants
#Set seed, init plots, get beta parameters
np.random.seed(seed=12345)
fig, ax = plt.subplots(1, 1)
priorA = beta17Pre[beta17Pre.Team_Abbr == "SFG"]["PriorAlpha"].values[0]
priorB = beta17Pre[beta17Pre.Team_Abbr == "SFG"]["PriorBeta"].values[0]

#Summary stats of distribution
mean, var, skew, kurt = beta.stats(priorA, priorB, moments='mvsk')

#Plot pdf
x = np.linspace(beta.ppf(0.001, priorA, priorB),
              beta.ppf(0.999, priorA, priorB), 1000)
ax.plot(x, beta.pdf(x, priorA, priorB),
         'r-', lw=5, alpha=0.6, label='beta pdf')

#Check pdf vs cdf
vals = beta.ppf([0.001, 0.5, 0.999], priorA, priorB)
print(np.allclose([0.001, 0.5, 0.999], beta.cdf(vals, priorA, priorB))) #True

#plot histogram of random samples from distribution
r = beta.rvs(priorA, priorB, size=10000)
binwidth = .025
ax.hist(r, normed=True, histtype='stepfilled', alpha=0.2,
        bins=np.arange(min(r), max(r) + binwidth, binwidth))

#Make plot pretty
ax.legend(loc='best', frameon=False)
ax.set_xlim([0.35, 0.75])
ax.set_ylim([0, 8])
plt.title('SFG 2017 Preseason WP% Beta Estimate')
plt.ylabel('Density')
plt.xlabel('Winning Percentage')
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()

#point estimate and 95% CI for end-of-season wins for SFG
print(np.mean(r) * 162) #88
print(np.percentile(r, 2.5) * 162) #71.5
print(np.percentile(r, 97.5) * 162) #104

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
for team in beta17Pre.Team_Abbr.values:
    priorA = beta17Pre[beta17Pre.Team_Abbr == team]["PriorAlpha"].values[0]
    priorB = beta17Pre[beta17Pre.Team_Abbr == team]["PriorBeta"].values[0]
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
beta17Pre["Beta_Estimate"] = winPercBeta
beta17Pre["80CI_Low"] = ci80Low
beta17Pre["80CI_High"] = ci80High
beta17Pre["90CI_Low"] = ci90Low
beta17Pre["90CI_High"] = ci90High
beta17Pre["95CI_Low"] = ci95Low
beta17Pre["95CI_High"] = ci95High
beta17Pre["99CI_Low"] = ci99Low
beta17Pre["99CI_High"] = ci99High

#turn win percentages into regular season win estimates
beta17Pre["Beta_Wins"] = np.round(beta17Pre.Beta_Estimate * beta17Pre.RegGames,1)

beta17Pre["80CI_Low_Wins"] = np.round(beta17Pre["80CI_Low"] * beta17Pre.RegGames,1)
beta17Pre["80CI_High_Wins"] = np.round(beta17Pre["80CI_High"] * beta17Pre.RegGames,1)
beta17Pre["90CI_Low_Wins"] = np.round(beta17Pre["90CI_Low"] * beta17Pre.RegGames,1)
beta17Pre["90CI_High_Wins"] = np.round(beta17Pre["90CI_High"] * beta17Pre.RegGames,1)
beta17Pre["95CI_Low_Wins"] = np.round(beta17Pre["95CI_Low"] * beta17Pre.RegGames,1)
beta17Pre["95CI_High_Wins"] = np.round(beta17Pre["95CI_High"] * beta17Pre.RegGames,1)
beta17Pre["99CI_Low_Wins"] = np.round(beta17Pre["99CI_Low"] * beta17Pre.RegGames,1)
beta17Pre["99CI_High_Wins"] = np.round(beta17Pre["99CI_High"] * beta17Pre.RegGames,1)

#check if actual 2017 wins fell in preseason confidence intervals
beta17Pre["FinalIn80CI"] = np.where(np.logical_and(np.greater_equal(beta17Pre["2017_Actual_WP"], beta17Pre["80CI_Low"]),
         np.less_equal(beta17Pre["2017_Actual_WP"], beta17Pre["80CI_High"])), 1, 0)
beta17Pre["FinalIn90CI"] = np.where(np.logical_and(np.greater_equal(beta17Pre["2017_Actual_WP"], beta17Pre["90CI_Low"]),
         np.less_equal(beta17Pre["2017_Actual_WP"], beta17Pre["90CI_High"])), 1, 0)
beta17Pre["FinalIn95CI"] = np.where(np.logical_and(np.greater_equal(beta17Pre["2017_Actual_WP"], beta17Pre["95CI_Low"]),
         np.less_equal(beta17Pre["2017_Actual_WP"], beta17Pre["95CI_High"])), 1, 0)
beta17Pre["FinalIn99CI"] = np.where(np.logical_and(np.greater_equal(beta17Pre["2017_Actual_WP"], beta17Pre["99CI_Low"]),
         np.less_equal(beta17Pre["2017_Actual_WP"], beta17Pre["99CI_High"])), 1, 0)

print(sum(beta17Pre["FinalIn80CI"])/float(len(beta17Pre))) #.77 23/30
print(sum(beta17Pre["FinalIn90CI"])/float(len(beta17Pre))) #.83 25/30
print(sum(beta17Pre["FinalIn95CI"])/float(len(beta17Pre))) #.90 27/30
print(sum(beta17Pre["FinalIn99CI"])/float(len(beta17Pre))) #.97 29/30
         
#beta17Pre.to_csv("mlb2017PreSeasonBetaEstimates.csv", index=False)

#########################################################################

#experimental priors

#Uninformed
np.random.seed(seed=12345)
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
priorA = 1
priorB = 1

#Plot pdf
x = np.linspace(beta.ppf(0.001, priorA, priorB),
              beta.ppf(0.999, priorA, priorB), 1000)
ax.plot(x, beta.pdf(x, priorA, priorB),
         'r-', lw=5, alpha=0.6, label='beta pdf')

#plot histogram of random samples from distribution
r = beta.rvs(priorA, priorB, size=10000)
binwidth = .025
ax.hist(r, normed=True, histtype='stepfilled', alpha=0.2,
        bins=np.arange(min(r), max(r) + binwidth, binwidth))

#Make plot pretty
ax.legend(loc='best', frameon=False)
ax.set_xlim([0.25, 0.75])
ax.set_ylim([0, 8])
plt.title('Uninformed Preseason WP% Beta Estimate')
plt.ylabel('Density')
plt.xlabel('Winning Percentage')
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
#fig.savefig('uninformed.png', bbox_inches='tight')

#point estimate and 95% CI
print(np.mean(r) * 162) #80.6
print(np.percentile(r, 2.5) * 162) #4
print(np.percentile(r, 97.5) * 162) #158

#informed
np.random.seed(seed=12345)
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)

avg2016WP = np.mean(mlb16["W-L%"])
avgRegrGames = (avg2016WP * (1-avg2016WP))/(np.std(mlb16["W-L%"])**2 
                    - np.sqrt((avg2016WP * (1-avg2016WP))/162)**2)

priorA = avgRegrGames * avg2016WP
priorB = avgRegrGames * (1-avg2016WP)
r = beta.rvs(priorA, priorB, size=100000)
print(
np.mean(r),
np.percentile(r, 10),
np.percentile(r, 90),
np.percentile(r, 5),
np.percentile(r, 95),
np.percentile(r, 2.5),
np.percentile(r, 97.5),
np.percentile(r, 0.5),
np.percentile(r, 99.5))

#Plot pdf
x = np.linspace(beta.ppf(0.001, priorA, priorB),
              beta.ppf(0.999, priorA, priorB), 1000)
ax.plot(x, beta.pdf(x, priorA, priorB),
         'r-', lw=5, alpha=0.6, label='beta pdf')

#plot histogram of random samples from distribution
r = beta.rvs(priorA, priorB, size=10000)
binwidth = .025
ax.hist(r, normed=True, histtype='stepfilled', alpha=0.2,
        bins=np.arange(min(r), max(r) + binwidth, binwidth))

#Make plot pretty
ax.legend(loc='best', frameon=False)
ax.set_xlim([0.25, 0.75])
ax.set_ylim([0, 8])
plt.title('Informed Preseason WP% Beta Estimate')
plt.ylabel('Density')
plt.xlabel('Winning Percentage')
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
plt.show()
#fig.savefig('informed.png', bbox_inches='tight')

#point estimate and 95% CI 
print(np.mean(r) * 162) #81
print(np.percentile(r, 2.5) * 162) #64.6
print(np.percentile(r, 97.5) * 162) #97

#Personalized Priors
for teamAbbr in beta17Pre.Team_Abbr.values:
    #Set seed, init plots, get beta parameters
    np.random.seed(seed=12345)
    fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
    priorA = beta17Pre[beta17Pre.Team_Abbr == teamAbbr]["PriorAlpha"].values[0]
    priorB = beta17Pre[beta17Pre.Team_Abbr == teamAbbr]["PriorBeta"].values[0]
    
    #Plot pdf
    x = np.linspace(beta.ppf(0.001, priorA, priorB),
                  beta.ppf(0.999, priorA, priorB), 1000)
    ax.plot(x, beta.pdf(x, priorA, priorB),
             'r-', lw=5, alpha=0.6, label='beta pdf')
    
    #plot histogram of random samples from distribution
    r = beta.rvs(priorA, priorB, size=10000)
    binwidth = .025
    ax.hist(r, normed=True, histtype='stepfilled', alpha=0.2,
            bins=np.arange(min(r), max(r) + binwidth, binwidth))
    
    #Make plot pretty
    ax.legend(loc='best', frameon=False)
    ax.set_xlim([0.25, 0.75])
    ax.set_ylim([0, 8])
    plt.title(teamAbbr + ' 2017 Preseason WP% Beta Estimate')
    plt.ylabel('Density')
    plt.xlabel('Winning Percentage')
    plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
    #plt.show()
    #fig.savefig(teamAbbr + 'prior.png', bbox_inches='tight')

###############################################################################

#Create Gifs per day per prior per team

import errno
import imageio

#read data downloaded from xmlStats API
mlb17Results = pd.read_csv("mlb2017SeasonResults.csv")

from datetime import timedelta, date
#https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

dates = []
start_date = date(2017, 4, 2)
end_date = date(2017, 10, 2)
for single_date in daterange(start_date, end_date):
    dates.append(single_date.strftime("%Y%m%d"))
    
teams = beta17Pre.Team_Abbr.values

#Get Gifs    
for team_Abbr in teams:
    #Personalized Prior
    filename = "C:/Users/Alexander/Documents/baseball/Past Perf Playoffs/Teams/" + team_Abbr + "/personalizedPrior/"
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    os.chdir(filename)
    
    priorA = beta17Pre[beta17Pre.Team_Abbr == team_Abbr]["PriorAlpha"].values[0]
    priorB = beta17Pre[beta17Pre.Team_Abbr == team_Abbr]["PriorBeta"].values[0]
    
    team17Res = mlb17Results[mlb17Results.Team_Abbr==team_Abbr].iloc[:,2:368]
    teamWins = team17Res.iloc[:,range(0,366,2)].values[0]
    teamLosses = team17Res.iloc[:,range(1,367,2)].values[0]
    
    #Plot pdf
    np.random.seed(seed=12345)
    fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
    x = np.linspace(beta.ppf(0.001, priorA, priorB),
                  beta.ppf(0.999, priorA, priorB), 1000)
    ax.plot(x, beta.pdf(x, priorA, priorB),
             'r-', lw=5, alpha=0.6, label='beta pdf')
    
    #Make plot pretty
    ax.legend(loc='best', frameon=False)
    ax.set_xlim([0.25, 0.75])
    ax.set_ylim([0, 13])
    plt.title(team_Abbr + ' 2017 Preseason WP% Prior Beta Estimate')
    plt.ylabel('Density')
    plt.xlabel('Winning Percentage')
    plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
    #plt.show()
    #fig.savefig(team_Abbr + '20170401Prior.png', bbox_inches='tight')
    
    for i in range(len(dates)):
        posteriorAlpha = priorA + teamWins[i]
        posteriorBeta = priorB + teamLosses[i]    
        currDate = dates[i]
        
        #Plot pdf
        fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
        x = np.linspace(beta.ppf(0.001, posteriorAlpha, posteriorBeta),
                      beta.ppf(0.999, posteriorAlpha, posteriorBeta), 1000)
        ax.plot(x, beta.pdf(x, posteriorAlpha, posteriorBeta),
                 'r-', lw=5, alpha=0.6, label='beta pdf')
        
        #Make plot pretty
        ax.legend(loc='best', frameon=False)
        ax.set_xlim([0.25, 0.75])
        ax.set_ylim([0, 13])
        plt.title(team_Abbr + " " + currDate + ' WP% Posterior Beta Estimate')
        plt.ylabel('Density')
        plt.xlabel('Winning Percentage')
        plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
        #plt.show()
        #fig.savefig(team_Abbr+currDate + 'Posterior.png', bbox_inches='tight')
        plt.clf()
    
    images = []
    filenames = os.listdir(os.getcwd())
    for imgFilename in filenames:
        images.append(imageio.imread(imgFilename))
    
    # Save them as frames into a gif 
    exportname = team_Abbr + "2017WPBetaEstimates_Personalized.gif"
    #imageio.mimsave(exportname, images, format='GIF', duration=0.1)
    print(team_Abbr)
    
    #InformedPrior
    filename = "C:/Users/Alexander/Documents/baseball/Past Perf Playoffs/Teams/" + team_Abbr + "/informedPrior/"
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    os.chdir(filename)
    
    priorA = avgRegrGames * avg2016WP
    priorB = avgRegrGames * (1-avg2016WP)

    team17Res = mlb17Results[mlb17Results.Team_Abbr==team_Abbr].iloc[:,2:368]
    teamWins = team17Res.iloc[:,range(0,366,2)].values[0]
    teamLosses = team17Res.iloc[:,range(1,367,2)].values[0]
    
    #Plot pdf
    np.random.seed(seed=12345)
    fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
    x = np.linspace(beta.ppf(0.001, priorA, priorB),
                  beta.ppf(0.999, priorA, priorB), 1000)
    ax.plot(x, beta.pdf(x, priorA, priorB),
             'r-', lw=5, alpha=0.6, label='beta pdf')
    
    #Make plot pretty
    ax.legend(loc='best', frameon=False)
    ax.set_xlim([0.25, 0.75])
    ax.set_ylim([0, 13])
    plt.title(team_Abbr + ' 2017 Preseason WP% Prior Beta Estimate')
    plt.ylabel('Density')
    plt.xlabel('Winning Percentage')
    plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
    #plt.show()
    #fig.savefig(team_Abbr + '20170401Prior.png', bbox_inches='tight')
    
    for i in range(len(dates)):
        posteriorAlpha = priorA + teamWins[i]
        posteriorBeta = priorB + teamLosses[i]    
        currDate = dates[i]
        
        #Plot pdf
        fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
        x = np.linspace(beta.ppf(0.001, posteriorAlpha, posteriorBeta),
                      beta.ppf(0.999, posteriorAlpha, posteriorBeta), 1000)
        ax.plot(x, beta.pdf(x, posteriorAlpha, posteriorBeta),
                 'r-', lw=5, alpha=0.6, label='beta pdf')
        
        #Make plot pretty
        ax.legend(loc='best', frameon=False)
        ax.set_xlim([0.25, 0.75])
        ax.set_ylim([0, 13])
        plt.title(team_Abbr + " " + currDate + ' WP% Posterior Beta Estimate')
        plt.ylabel('Density')
        plt.xlabel('Winning Percentage')
        plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
        #plt.show()
        #fig.savefig(team_Abbr+currDate + 'Posterior.png', bbox_inches='tight')
        plt.clf()
    
    images = []
    filenames = os.listdir(os.getcwd())
    for imgFilename in filenames:
        images.append(imageio.imread(imgFilename))
    
    # Save them as frames into a gif 
    exportname = team_Abbr + "2017WPBetaEstimates_Informed.gif"
    #imageio.mimsave(exportname, images, format='GIF', duration=0.1)
    print(team_Abbr)
    
    #UninformedPrior
    filename = "C:/Users/Alexander/Documents/baseball/Past Perf Playoffs/Teams/" + team_Abbr + "/uninformedPrior/"
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    os.chdir(filename)
    
    priorA = 1
    priorB = 1

    team17Res = mlb17Results[mlb17Results.Team_Abbr==team_Abbr].iloc[:,2:368]
    teamWins = team17Res.iloc[:,range(0,366,2)].values[0]
    teamLosses = team17Res.iloc[:,range(1,367,2)].values[0]
    
    #Plot pdf
    np.random.seed(seed=12345)
    fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
    x = np.linspace(beta.ppf(0.001, priorA, priorB),
                  beta.ppf(0.999, priorA, priorB), 1000)
    ax.plot(x, beta.pdf(x, priorA, priorB),
             'r-', lw=5, alpha=0.6, label='beta pdf')
    
    #Make plot pretty
    ax.legend(loc='best', frameon=False)
    ax.set_xlim([0.25, 0.75])
    ax.set_ylim([0, 13])
    plt.title(team_Abbr + ' 2017 Preseason WP% Prior Beta Estimate')
    plt.ylabel('Density')
    plt.xlabel('Winning Percentage')
    plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
    #plt.show()
    #fig.savefig(team_Abbr + '20170401Prior.png', bbox_inches='tight')
    
    for i in range(len(dates)):
        posteriorAlpha = priorA + teamWins[i]
        posteriorBeta = priorB + teamLosses[i]    
        currDate = dates[i]
        
        #Plot pdf
        fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
        x = np.linspace(beta.ppf(0.001, posteriorAlpha, posteriorBeta),
                      beta.ppf(0.999, posteriorAlpha, posteriorBeta), 1000)
        ax.plot(x, beta.pdf(x, posteriorAlpha, posteriorBeta),
                 'r-', lw=5, alpha=0.6, label='beta pdf')
        
        #Make plot pretty
        ax.legend(loc='best', frameon=False)
        ax.set_xlim([0.25, 0.75])
        ax.set_ylim([0, 13])
        plt.title(team_Abbr + " " + currDate + ' WP% Posterior Beta Estimate')
        plt.ylabel('Density')
        plt.xlabel('Winning Percentage')
        plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
        #plt.show()
        #fig.savefig(team_Abbr+currDate + 'Posterior.png', bbox_inches='tight')
        plt.clf()
    
    images = []
    filenames = os.listdir(os.getcwd())
    for imgFilename in filenames:
        images.append(imageio.imread(imgFilename))
    
    # Save them as frames into a gif 
    exportname = team_Abbr + "2017WPBetaEstimates_Uninformed.gif"
    #imageio.mimsave(exportname, images, format='GIF', duration=0.1)
    print(team_Abbr) #track progress

###########################################################################

#Compare when in season the actual wp% fell inside the 95% CI for informed
# vs Personalized prio

#Get date when 2017 actual wp% fell inside personalized prior 95% CI
np.random.seed(seed=12345)
successPers = []
for team_Abbr in teams:
    priorA = beta17Pre[beta17Pre.Team_Abbr == team_Abbr]["PriorAlpha"].values[0]
    priorB = beta17Pre[beta17Pre.Team_Abbr == team_Abbr]["PriorBeta"].values[0]
    #priorA = avgRegrGames * avg2016WP
    #priorB = avgRegrGames * (1-avg2016WP)
    
    actWP= beta17Pre[beta17Pre.Team_Abbr == team_Abbr]["2017_Actual_WP"].values[0]
    
    team17Res = mlb17Results[mlb17Results.Team_Abbr==team_Abbr].iloc[:,2:368]
    teamWins = team17Res.iloc[:,range(0,366,2)].values[0]
    teamLosses = team17Res.iloc[:,range(1,367,2)].values[0]
    
    for i in range(len(dates)):
        posteriorAlpha = priorA + teamWins[i]
        posteriorBeta = priorB + teamLosses[i]    
        currDate = dates[i]        
        
        #Summary stats of distribution
        r = beta.rvs(posteriorAlpha, posteriorBeta, size=10000)
        if (np.percentile(r,97.5) - np.percentile(r,2.5))*162 /2 < 150:
            if np.logical_and(np.greater_equal(actWP, np.percentile(r,2.5)),
             np.less_equal(actWP, np.percentile(r,97.5))):
                successPers.append(int(currDate))
                print(team_Abbr)
                print(currDate)
                print(np.mean(r)*162)
                print(actWP*162)
                print(np.sqrt(np.var(r))*162)
                break

#Get date when 2017 actual wp% fell inside informed prior 95% CI
np.random.seed(seed=12345)    
successIndp = []
for team_Abbr in teams:
    #priorA = beta17Pre[beta17Pre.Team_Abbr == team_Abbr]["PriorAlpha"].values[0]
    #priorB = beta17Pre[beta17Pre.Team_Abbr == team_Abbr]["PriorBeta"].values[0]
    priorA = avgRegrGames * avg2016WP
    priorB = avgRegrGames * (1-avg2016WP)
    
    actWP= beta17Pre[beta17Pre.Team_Abbr == team_Abbr]["2017_Actual_WP"].values[0]
    
    team17Res = mlb17Results[mlb17Results.Team_Abbr==team_Abbr].iloc[:,2:368]
    teamWins = team17Res.iloc[:,range(0,366,2)].values[0]
    teamLosses = team17Res.iloc[:,range(1,367,2)].values[0]
    
    for i in range(len(dates)):
        posteriorAlpha = priorA + teamWins[i]
        posteriorBeta = priorB + teamLosses[i]    
        currDate = dates[i]        
        
        #Summary stats of distribution
        r = beta.rvs(posteriorAlpha, posteriorBeta, size=10000)
        if (np.percentile(r,97.5) - np.percentile(r,2.5))*162 /2 <= 150:
            if np.logical_and(np.greater_equal(actWP, np.percentile(r,2.5)),
             np.less_equal(actWP, np.percentile(r,97.5))):
                successIndp.append(int(currDate))
                print(team_Abbr)
                print(currDate)
                print(np.mean(r)*162)
                print(actWP*162)
                print(np.sqrt(np.var(r))*162)
                break

#Compare
print(all(successPers[i] <= successIndp[i] for i in range(30)))
print(sum([successPers[i] <= successIndp[i] for i in range(30)]))
    
zip(teams, successPers, successIndp, np.array(successPers) - np.array(successIndp))
    
np.mean(np.array(successPers) - np.array(successIndp))

