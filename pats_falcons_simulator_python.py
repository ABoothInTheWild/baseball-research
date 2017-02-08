# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 21:48:40 2017

@author: Alexander
"""

import pandas as pd
import numpy as np
import random

#Super Bowl Simulator
#Using Negative Binomial Disribution

#Alexander Booth
#January 31, 2017

#define data
pats_off = np.array([23, 31, 27, 0, 33, 35, 27, 41, 24, 30, 22, 26, 30, 16, 41, 35, 34, 36])
pats_def = np.array([21, 24, 0, 16, 13, 17, 16, 25, 31, 17, 17, 10, 23, 3, 3, 14, 16, 17])

falc_off = np.array([24, 35, 45, 48, 23, 24, 30, 33, 43, 15, 38, 28, 42, 41, 33, 38, 36, 44])
falc_def = np.array([31, 28, 32, 33, 16, 26, 33, 32, 28, 24, 19, 29, 14, 13, 16, 32, 20, 21])

scores_df = pd.DataFrame(data = { "Pats_Off" : pats_off, "Pats_Def" : pats_def, "Falc_Off" : falc_off, "Falc_Def" : falc_def})

#define simulator
def simulator(team1_off_mean, team1_def_mean, team2_off_mean, team2_def_mean, niterations):
    
  #set seed for duplicity
  random.seed(1234)
  
  #set game arrays
  team1_game_score = np.array(range(niterations))
  team2_game_score = np.array(range(niterations))
  
  team1_wins = np.array(range(niterations))
  team2_wins = np.array(range(niterations))
  
  size = 4
  
  i = 0
  
  while(i < niterations):
    
    #sample from negative binomial for each statistic
    team1_off = np.random.negative_binomial(size, size/(size+team1_off_mean), 1)
    team1_def = np.random.negative_binomial(size, size/(size+team1_def_mean), 1)
    
    team2_off = np.random.negative_binomial(size, size/(size+team2_off_mean), 1)
    team2_def = np.random.negative_binomial(size, size/(size+team2_def_mean), 1)
    
    #determine final game score
    team1_score = round(np.mean(np.array([team1_off, team2_def])))
    team2_score = round(np.mean(np.array([team2_off, team1_def])))
    
    #Check for ties
    if(team1_score == 1 or team2_score == 1):
      continue
    
    if(team1_score == team2_score):
      continue
    
    #record score
    team1_game_score[i] = team1_score
    team2_game_score[i] = team2_score
    
    #record wins
    if(team1_score > team2_score):
      team1_wins[i] = 1
      team2_wins[i] = 0
    
    if(team2_score > team1_score):
      team2_wins[i] = 1
      team1_wins[i] = 0
    
    i = i + 1
  
  #determine win sum
  team1_sum = sum(team1_wins)
  team2_sum = sum(team2_wins)
  
  #determine win percentage
  team1_win_pcnt = team1_sum/float(niterations)
  team2_win_pcnt = team2_sum/float(niterations)
  
  #return array of percentages, mean scores, and standard deviations
  return(np.array([team1_win_pcnt, team2_win_pcnt, np.mean(team1_game_score), np.mean(team2_game_score), np.std(team1_game_score), np.std(team2_game_score)]))

#simulate super bowl
pats_off_mean = np.mean(pats_off)
pats_def_mean = np.mean(pats_def)

falc_off_mean = np.mean(falc_off)
falc_def_mean = np.mean(falc_def)
niterations = 100000

final_scores = simulator(pats_off_mean, pats_def_mean, falc_off_mean, falc_def_mean, niterations)

print(final_scores)