# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 18:10:55 2018

@author: Alexander Booth
"""

##############################################################################################
#Riddler Express
#From Steven Pratt, an autumnal puzzle:
#
#The Major League Baseball playoffs are about to begin. Based on the current playoff format, what is the best possible winning percentage a team can have in the playoffs without winning the World Series? And what is the worst possible winning percentage a team can have in the playoffs and still win the World Series?
#
#Extra credit: How close to these extremes has any actual team come?

#https://fivethirtyeight.com/features/two-paths-diverged-in-a-city-and-i-i-took-the-block-less-traveled-by/
#https://www.baseball-reference.com/postseason/
##############################################################################################

import numpy as np

#What is the best possible winning percentage a team can have in the playoffs without winning the World Series?
minGamesPlayed = 0 + 3 + 4 + 4 #no wildcard and sweep
maxGamesPlayed = 1 + 5 + 7 + 7 #wildcard and max out all series
minGamesWon = 0 + 3 + 4 + 0 #Did not play wildcard and was swept in WS
maxGamesWon = 1 + 3 + 4 + 3 #Played wildcard and maxed out WS

gamesPlayed =[]
gamesWon = []
winPercentages = []
    
for x in range(minGamesPlayed, maxGamesPlayed + 1):
    for y in range(minGamesWon, maxGamesWon + 1):
        if (y == minGamesWon and x == maxGamesPlayed):
            continue #have to win the WildCard Game to play 20 games
        if (y+4 <= x): #Account for 4 wins in WS since we lost
            winPercentages.append(y/float(x))
            gamesPlayed.append(x)
            gamesWon.append(y)

argMax = np.argmax(winPercentages)
print("Best wp% without winning the World Series is winning " + str(gamesWon[argMax]) + " games while playing " + str(gamesPlayed[argMax]) + " games for a winning percentage of " + str(np.round(winPercentages[argMax], 3)))

##############################################################################################

#What is the worst possible winning percentage a team can have in the playoffs and still win the World Series?
minGamesPlayed = 0 + 3 + 4 + 4 #no wildcard and sweep
maxGamesPlayed = 1 + 5 + 7 + 7 #wildcard and max out all series

minGamesWon = 0 + 3 + 4 + 4 #Did not play wildcard
maxGamesWon = 1 + 3 + 4 + 4 #Won wildcard

gamesPlayed =[]
gamesWon = []
winPercentages = []
    
for x in range(minGamesPlayed, maxGamesPlayed + 1):
    for y in range(minGamesWon, maxGamesWon + 1):
        if (y == minGamesWon and x == maxGamesPlayed):
            continue #have to win the WildCard Game to play 20 games
        if (y <= x): #Can't win more than we play
            winPercentages.append(y/float(x))
            gamesPlayed.append(x)
            gamesWon.append(y)
argMin = np.argmin(winPercentages)
print("Worst wp% and still winning the World Series is winning " + str(gamesWon[argMin]) + " games while playing " + str(gamesPlayed[argMin]) + " games for a winning percentage of " + str(np.round(winPercentages[argMin], 3)))
