# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 00:17:48 2017

@author: Alexander
"""
import pandas as pd
import numpy as np
import random

#Roulette Simulator
#Using Martingale betting strategy

#Alexander Booth
#January 25, 2017

#init probability variables
p_win = 18/38.0
p_lose = 20/38.0
niterations = 10000
#this is the intial bet put down
#It get's doubled after each loss
init_bet = 1
#maximum cash willing to lose
stop_loss = 130
#Goal to win
goal = 1

def simulator(p_win, p_lose, niterations, init_bet, stop_loss, goal):
  #Allow for reproduction
  random.seed(1234)
  #init variables
  results_bin = np.array(range(niterations))
  results_prof = np.array(range(niterations))
  total_profit = 0
  
  #figure out max losses in a row
  #Geometric sequence: ar^n
  a = init_bet
  sum = a
  max_losses = 1
  while(sum <= stop_loss):
    double = 2 ** max_losses
    a = init_bet * double
    sum = sum + a
    max_losses = max_losses + 1
  
  max_losses = max_losses - 1
  
  i = 0
  #Loop through iterations
  while(i < niterations):
    #Per turn, we play until we hit our goal
    #or hit our max_losses in a row
    current_profit = 0
    bet = init_bet
    win = False
    j = 0
    
    while(j < max_losses):
      
      #Random number from uniform distribution
      spin = random.random()
      
      #If win, add bet to the current profit
      #Check if current profit hits our goal
      #reset losses in a row
      #reset bet
      
      if(spin >= p_lose):
        current_profit = current_profit + bet
        if(current_profit >= goal):
          win = True
          break
        
        bet = init_bet
        j = 0
      
      #If lose, subtract bet from current profit
      #double our bet
      #add 1 to our losses in a row
      
      if(spin <= p_lose):
        current_profit = current_profit - bet
        bet = bet * 2
        j = j + 1
    
    #Set total profit for that game
    total_profit = current_profit
    
    #add profit and win boolean to arrays
    results_prof[i] = total_profit
    if(win == True):
      results_bin[i] = 1
    
    else:
      results_bin[i] = 0
    
    i = i + 1
  
  #return dataframe
  return(pd.DataFrame(data = {"Results" : results_bin, "Profit" : results_prof}))

results = simulator(p_win, p_lose, niterations, init_bet, stop_loss, goal)

#determine probability of reaching our goal
sum(results["Results"])/float(len(results["Results"]))