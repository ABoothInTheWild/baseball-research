# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 22:45:16 2018

@author: ABooth
"""    

def getGameScore(prob, homeWon):
    #https://fivethirtyeight.com/features/how-to-play-our-nfl-predictions-game/
    return 25 - ((prob*100 - 100)**2/100)*homeWon - (((1-prob)*100 - 100)**2/100)*(1-homeWon)

def getBrierScore(prob, homeWon):
    #https://en.wikipedia.org/wiki/Brier_score
    return ((prob - homeWon)**2)*homeWon + ((1-prob-1-homeWon)**2)*(1-homeWon)
    
def getMLBGamesFromDate(inpDate, df):
    games = df[(df.date == inpDate)]
    return list(zip(games.team1.values, games.team2.values))

def getMLBResultsFromTeamsAndDate(homeTeamAbbr, awayTeamAbbr, inpDate, df):
    game = df[(df.date == inpDate) & (df.team1 == homeTeamAbbr) & (df.team2 == awayTeamAbbr)]
    return [1,0] if game.score1.values[0] > game.score2.values[0] else [0,1]
    
def MLB538WinProbability(homeTeamAbbr, awayTeamAbbr, inpDate, df):    
    if homeTeamAbbr == "MIA":
        homeTeamAbbr = "FLA"
    if homeTeamAbbr == "LAA":
        homeTeamAbbr = "ANA"
    if homeTeamAbbr == "TBR":
        homeTeamAbbr = "TBD"
    if awayTeamAbbr == "MIA":
        awayTeamAbbr = "FLA"
    if awayTeamAbbr == "LAA":
        awayTeamAbbr = "ANA"
    if awayTeamAbbr == "TBR":
        awayTeamAbbr = "TBD"
    
    game = df[(df.date == inpDate) & (df.team1 == homeTeamAbbr) & (df.team2 == awayTeamAbbr)]
    
    return game.rating_prob1.values[0]