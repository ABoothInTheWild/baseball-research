# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 10:15:51 2017

@author: Alexander Booth
"""

# Imports
# prepare for Python version 3x features and functions
from __future__ import division, print_function

import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os

#World Series 2017 Simulator
#Using Negative Binomial Disribution

#Alexander Booth
#October 24, 2017

#Set Directory
os.chdir(r"C:\Users\Alexander\Documents\baseball\World Series")

#define data
astros = pd.read_csv(r"astros_regularSeason_2017.csv")
astros["Home/Away"] = pd.get_dummies(astros['Unnamed: 4'])

dodgers = pd.read_csv(r"dodgers_regularSeason_2017.csv")
dodgers["Home/Away"] = pd.get_dummies(dodgers['Unnamed: 4'])

astrosSub = astros[["R", "RA", "Home/Away"]]
dodgersSub = dodgers[["R", "RA", "Home/Away"]]

#Stats
astrosSub.corr()
dodgersSub.corr()

np.mean(astrosSub[astrosSub["Home/Away"] == 0]["R"])
np.mean(astrosSub[astrosSub["Home/Away"] == 1]["R"])
np.mean(astrosSub[astrosSub["Home/Away"] == 0]["RA"])
np.mean(astrosSub[astrosSub["Home/Away"] == 1]["RA"])

np.mean(dodgersSub[dodgersSub["Home/Away"] == 0]["R"])
np.mean(dodgersSub[dodgersSub["Home/Away"] == 1]["R"])
np.mean(dodgersSub[dodgersSub["Home/Away"] == 0]["RA"])
np.mean(dodgersSub[dodgersSub["Home/Away"] == 1]["RA"])

##################################################
#Histograms
# the histogram of the data
n, bins, patches = plt.hist(dodgers.R, 10, normed=1, facecolor='blue', alpha=0.75)
mu = np.mean(dodgers.R)
sigma = np.std(dodgers.R)

# add a 'best fit' line
y = mlab.normpdf( bins, mu, sigma)
l = plt.plot(bins, y, 'r--', linewidth=1)

plt.xlabel('Runs Scored')
plt.ylabel('Frequency')
plt.xlim([0,20])
plt.ylim([0,.16])
plt.title(r'Dodgers Runs Scored')
plt.grid(False)

plt.show()

size = 4
np.random.seed(123)
test = np.random.negative_binomial(size, size/(size+mu), 1000)

# the histogram of the data
n, bins, patches = plt.hist(test, 10, normed=1, facecolor='blue', alpha=0.75)
mu2 = np.mean(test)
sigma = np.std(test)

# add a 'best fit' line
y = mlab.normpdf( bins, mu2, sigma)
l = plt.plot(bins, y, 'r--', linewidth=1)

plt.xlabel('Runs Scored')
plt.ylabel('Frequency')
plt.xlim([0,20])
plt.ylim([0,.16])
plt.title(r'Simulated Dodgers Runs Scored')
plt.grid(False)

plt.show()

####################################################################
#define simulator
def simulator(team1_df, team2_df, useHomeFieldAdv, length_of_series, niterations, negative_binom_size):  
    #set seed for duplicity
    np.random.seed(1234)
        
    #set game arrays
    rtnScores = np.empty((niterations, length_of_series * 2))
    
    #Set home field games. Take the game number, subtract 1 and double it
    #for baseball, that's Games 1,2,6,7
    #make sure team with home field advantage is team1
    #team2 home advantage is Games 3,4,5
    team1_HOME = [0,2,10,12]
    team2_HOME = [4,6,8]
      
    #Get Means
    sampleMeans = getOffensiveAndDefensiveMeans(team1_df, team2_df, useHomeFieldAdv)
      
    for i in range(niterations):
        for j in range(0, length_of_series * 2, 2):        
            if not useHomeFieldAdv:                
                #Get game score
                sample_game_score = getSampleScores(sampleMeans[0], sampleMeans[1], sampleMeans[2], sampleMeans[3], 1, negative_binom_size)
            else:
                if j in team1_HOME:
                    sample_game_score = getSampleScores(sampleMeans[0], sampleMeans[2], sampleMeans[5], sampleMeans[7], 1, negative_binom_size)
                elif j in team2_HOME:
                    sample_game_score = getSampleScores(sampleMeans[1], sampleMeans[3], sampleMeans[4], sampleMeans[6], 1, negative_binom_size)
                else:
                    print("Something has gone terrible wrong")
                    break
            
            #record score
            rtnScores[i,j] = sample_game_score[0]
            rtnScores[i,j+1] = sample_game_score[1]
    
    return rtnScores

def getOffensiveAndDefensiveMeans(team1_df, team2_df, useHomeFieldAdv):
    rtnMeans = []
    
    if not useHomeFieldAdv:
        #Get Means
        team1_off_mean = np.mean(team1_df["R"])
        team1_def_mean = np.mean(team1_df["RA"])
        team2_off_mean = np.mean(team2_df["R"])
        team2_def_mean = np.mean(team2_df["RA"])
        
        rtnMeans = np.array([team1_off_mean, team1_def_mean, team2_off_mean, team2_def_mean])    
    else:
        #Get Means
        team1_off_mean_HOME = np.mean(team1_df[team1_df["Home/Away"] == 0]["R"])
        team1_off_mean_AWAY = np.mean(team1_df[team1_df["Home/Away"] == 1]["R"])
        team1_def_mean_HOME = np.mean(team1_df[team1_df["Home/Away"] == 0]["RA"])
        team1_def_mean_AWAY = np.mean(team1_df[team1_df["Home/Away"] == 1]["RA"])
        
        team2_off_mean_HOME = np.mean(team2_df[team2_df["Home/Away"] == 0]["R"])
        team2_off_mean_AWAY = np.mean(team2_df[team2_df["Home/Away"] == 1]["R"])
        team2_def_mean_HOME = np.mean(team2_df[team2_df["Home/Away"] == 0]["RA"])
        team2_def_mean_AWAY = np.mean(team2_df[team2_df["Home/Away"] == 1]["RA"])
        
        rtnMeans = np.array([team1_off_mean_HOME, team1_off_mean_AWAY, team1_def_mean_HOME, team1_def_mean_AWAY,
                             team2_off_mean_HOME, team2_off_mean_AWAY, team2_def_mean_HOME, team2_def_mean_AWAY])
  
    return rtnMeans
  
def getSampleScores(team1_off_mean, team1_def_mean, team2_off_mean, team2_def_mean, nScores, size):
    
    #sample from negative binomial for each statistic
    team1_off = np.random.negative_binomial(size, size/(size+team1_off_mean), nScores)
    team1_def = np.random.negative_binomial(size, size/(size+team1_def_mean), nScores)
    
    team2_off = np.random.negative_binomial(size, size/(size+team2_off_mean), nScores)
    team2_def = np.random.negative_binomial(size, size/(size+team2_def_mean), nScores)
    
    #determine final game score
    team1_score = round(np.mean(np.array([team1_off, team2_def])))
    team2_score = round(np.mean(np.array([team2_off, team1_def])))
    
    rtnScoreArray = np.array([team1_score, team2_score])
    
    #Check for ties
    if(team1_score == team2_score):
      rtnScoreArray = getSampleScores(team1_off_mean, team1_def_mean, team2_off_mean, team2_def_mean, nScores, size)
    
    return rtnScoreArray
    
##############################################################################
numSims = 10000
worldSeries = simulator(dodgersSub, astrosSub, True, 7, numSims, 4)

columns = ['WinningTeam','NumberOfGames', 'GameOneWinner']
df = pd.DataFrame(index = range(numSims), columns = columns)

for x in range(numSims):
    seriesScores = worldSeries[x,]
    astrosWins = 0
    dodgersWins = 0

    for y in range(0, len(seriesScores), 2):
        astrosScore = seriesScores[y+1]
        dodgersScore = seriesScores[y]
        
        if astrosScore > dodgersScore:
            astrosWins += 1
            if y == 0:
                df.GameOneWinner[x] = "Astros"
        if dodgersScore > astrosScore:
            dodgersWins += 1
            if y == 0:
                df.GameOneWinner[x] = "Dodgers"
                
        if astrosWins >= 4:
            df.WinningTeam[x] = "Astros"
            df.NumberOfGames[x] = astrosWins + dodgersWins
            break
        
        if dodgersWins >= 4:
            df.WinningTeam[x] = "Dodgers"
            df.NumberOfGames[x] = astrosWins + dodgersWins
            break
        
print("Astros Win Percentage: " , len(df[df.WinningTeam == "Astros"])/float(numSims))
print("Dodgers Win Percentage: " , len(df[df.WinningTeam == "Dodgers"])/float(numSims))


df[df.NumberOfGames == 7][["WinningTeam", "NumberOfGames"]].groupby("WinningTeam").count()
df[df.NumberOfGames == 4][["WinningTeam", "NumberOfGames"]].groupby("WinningTeam").count()


df[df.GameOneWinner == "Dodgers"][["WinningTeam", "NumberOfGames"]].groupby("WinningTeam").count()
df[df.GameOneWinner == "Astros"][["WinningTeam", "NumberOfGames"]].groupby("WinningTeam").count()

