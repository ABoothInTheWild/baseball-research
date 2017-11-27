# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 19:51:08 2017

@author: Alexander
"""

# Twitter Bot

# Imports
# prepare for Python version 3x features and functions
from __future__ import division, print_function
import random
import pandas as pd
from twitterBot import *

class BaseballTrivia(TwitterBot):
    
    #inits
    screen_name = "baseball_trivya"
    retweetTags = ["mlb", "#mlbnhotstove", "#mlbnow", "#cfbplayoff", "mls", "nfl", "nba", "nhl", "ncaa"]
    favoriteTags = ["mlb", "#mlbnhotstove", "#mlbnow", "#cfbplayoff", "mls", "nfl", "nba", "nhl", "ncaa"]
    followTags = ["mlb", "#mlbnhotstove", "#mlbnow", "#cfbplayoff", "mls", "nfl", "nba", "nhl", "ncaa"]
    
    #define data
    master = pd.read_csv(r"https://raw.githubusercontent.com/ABoothInTheWild/baseball-research/master/TwitterBot/Data/Master.csv")
    batting = pd.read_csv(r"https://raw.githubusercontent.com/ABoothInTheWild/baseball-research/master/TwitterBot/Data/Batting.csv")
    batting = batting.dropna(subset=["SO"]).fillna(0)
    pitching = pd.read_csv(r"https://raw.githubusercontent.com/ABoothInTheWild/baseball-research/master/TwitterBot/Data/Pitching.csv")
    teams = pd.read_csv(r"https://raw.githubusercontent.com/ABoothInTheWild/baseball-research/master/TwitterBot/Data/Teams.csv")
    batting["PA"] = batting.AB + batting.BB + batting.HBP + batting.SH + batting.SF
    pitching["IP"] = pitching.IPouts / 3.0
    pitching["WHIP"] = (pitching.H + pitching.BB) / pitching.IP
    uniquePlayers = master.playerID.unique()
    
    def getStatus(self):
        path = random.randint(1, 2)
        status = "I hope you have a great day!"
        if path == 1:
            status = self.getBattingLine(self.uniquePlayers, self.batting, self.teams, self.master)
        else:
            status = self.getPitchingLine(self.uniquePlayers, self.pitching, self.teams, self.master)
        
        return status
    
    #Get Batting Status
    def getBattingLine(self, uniquePlayers, batting, teams, master):
    
        batData = batting.iloc[[random.randint(0, len(batting)-1)]]
        
        if (not batData.playerID.values[0] in uniquePlayers) or (batData.PA.values[0] == 0):
            self.getBattingLine(uniquePlayers, batting, teams, master)
            
        else:
            name = master[master.playerID == batData.playerID.values[0]].nameFirst.values[0] + \
                    " " + master[master.playerID == batData.playerID.values[0]].nameLast.values[0]
        
            year = batData.yearID.values[0].astype(int)
            
            teamName = teams[(teams.teamID == batData.teamID.values[0]) &
                             (teams.yearID == batData.yearID.values[0])].name.values[0]
            
            games = batData.G.values[0].astype(int)
            plate = batData.PA.values[0].astype(int)
            
            hits = batData.H.values[0].astype(int)
            hrs = batData.HR.values[0].astype(int)
            sos = batData.SO.values[0].astype(int)
            
            line1 = name + " played for the " + teamName + " in the year " + str(year) + ". He had " + \
                    str(plate) + " plate appearances in " + str(games) + " games with " + str(hits) + " hits, " + \
                    str(hrs) + " homeruns, and " + str(sos) + " strikeouts. #MLB #facts"
                    
            line2 = "In the year " + str(year) + ", " + name + " played for the " + teamName +  ". He had " + \
                    str(plate) + " plate appearances in " + str(games) + " games with " + str(hits) + " hits, " + \
                    str(hrs) + " homeruns, and " + str(sos) + " strikeouts. #MLB #trivia"
                    
            line3 = name + " played for the " + teamName + " in the year " + str(year) + ". He had " + \
                    str(hits) + " hits, " + str(hrs) + " homeruns, and " + str(sos) + " strikeouts while recording " + \
                    str(plate) + " plate appearances in " + str(games) + " games! #MLB #trivia"  
                    
            line4 = "In the year " + str(year) + ", " + name + " played for the " + teamName +  ". He had " + \
                    str(hits) + " hits, " + str(hrs) + " homeruns, and " + str(sos) + " strikeouts while recording " + \
                    str(plate) + " plate appearances in " + str(games) + " games! #MLB #facts"
        
            lines = [line1, line2, line3, line4]
            
            finalLine = lines[random.randint(0, 3)]
            
            return finalLine
    
    #Get Pitching Status
    def getPitchingLine(self, uniquePlayers, pitching, teams, master):
    
        pitData = pitching.iloc[[random.randint(0, len(pitching)-1)]]
        
        if (not pitData.playerID.values[0] in uniquePlayers) or (pitData.IP.values[0] == 0):
            self.getPitchingLine(uniquePlayers, pitching, teams, master)
            
        else:
            name = master[master.playerID == pitData.playerID.values[0]].nameFirst.values[0] + \
                    " " + master[master.playerID == pitData.playerID.values[0]].nameLast.values[0]
        
            year = pitData.yearID.values[0].astype(int)
            
            teamName = teams[(teams.teamID == pitData.teamID.values[0]) &
                             (teams.yearID == pitData.yearID.values[0])].name.values[0]
            
            games = pitData.G.values[0].astype(int)
            era = pitData.ERA.values[0].astype(float)
            
            whip = round(pitData.WHIP.values[0].astype(float),2)
            ips = round(pitData.IP.values[0].astype(float), 2)
            wins = pitData.W.values[0].astype(int)
            loss = pitData.L.values[0].astype(int)
            
            line1 = name + " pitched for the " + teamName + " in the year " + str(year) + ". He pitched " + \
                    str(ips) + " innings over " + str(games) + " games with a " + str(era) + " ERA, " + \
                    str(whip) + " WHIP, and a " + str(wins) + "-" + str(loss) + " record. #MLB #trivia"
                    
            line2 = "In the year " + str(year) + ", " + name + " pitched for the " + teamName +  ". He pitched " + \
                    str(ips) + " innings over " + str(games) + " games with a " + str(era) + " ERA, " + \
                    str(whip) + " WHIP, and a " + str(wins) + "-" + str(loss) + " record. #MLB #facts"
                    
            line3 = name + " pitched for the " + teamName + " in the year " + str(year) + ". He had a " + \
                    str(era) + " ERA, " + str(whip) + " WHIP, and a " + str(wins) + "-" + str(loss) + " record while pitching " + \
                    str(ips) + " innings over " + str(games) + " games! #MLB #facts"  
                    
            line4 = "In the year " + str(year) + ", " + name + " pitched for the " + teamName +  ". He had a " + \
                    str(era) + " ERA, " + str(whip) + " WHIP, and a " + str(wins) + "-" + str(loss) + " record while pitching " + \
                    str(ips) + " innings over " + str(games) + " games. #MLB #trivia"  
        
            lines = [line1, line2, line3, line4]
            
            finalLine = lines[random.randint(0, 3)]
            
            return finalLine