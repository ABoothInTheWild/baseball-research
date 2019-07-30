# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 22:46:57 2018

@author: ABooth
"""

import numpy as np
import pandas as pd

def ImportRunsScoredAllowedDF(fileLoc):
    #define data
    df = pd.read_csv(fileLoc)
    df["Home/Away"] = pd.get_dummies(df['Unnamed: 4'])
    df["Won"] = df["R"] > df["RA"]
    dfSub = df[["R", "RA", "Home/Away", "Won"]].astype("float")
    return dfSub


#define simulator
def RunsSimulator(team1_df, team2_df, useHomeFieldAdv, niterations, negative_binom_size, length_of_series = 1):  
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
        for j in range(0, 1 * 2, 2):        
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
    
    results = pd.DataFrame(rtnScores, columns = ["Team1Score", "Team2Score"])
    results["WinningTeam"] = np.where(results['Team1Score'] > results["Team2Score"], 'Team1', 'Team2')
    return len(results[results.WinningTeam == "Team1"])/float(niterations)
    #return results

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
    