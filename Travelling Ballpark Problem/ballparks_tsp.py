# -*- coding: utf-8 -*-
"""
Created on Tue May 15 13:36:32 2018

@author: Alexander
"""

#Imports
import pandas as pd
from collections import Counter
import geopy.distance
import itertools
import gurobipy as g

#Load Data
#https://www.seamheads.com/ballparks/index.php
parks = pd.read_csv(r"C:\Users\Alexander\Documents\baseball\TSP\Seamheads_Ballparks_Database_2017\Parks.csv")
teams = pd.read_csv(r"C:\Users\Alexander\Documents\baseball\TSP\Seamheads_Ballparks_Database_2017\Teams.csv")
park_teams = pd.read_csv(r"C:\Users\Alexander\Documents\baseball\TSP\Seamheads_Ballparks_Database_2017\Home Main Data With Parks Breakout.csv")

#Get info from csvs
teamID = []
teamName = []
seasonsPlayed = []

for i in range(len(parks)):
    parkID = parks.iloc[i]["PARKID"]
    parksForTeam = park_teams[park_teams.Park_ID == parkID].TeamID
    teamID.append(Counter(parksForTeam).most_common(1)[0][0]) #Get team that played at home in the stadium the most
    teamName.append(teams[teams.TeamID == teamID[i]].City.values[0] + " " + teams[teams.TeamID == teamID[i]].Nickname.values[0])
    seasonsPlayed.append(sum(Counter(parksForTeam).values()))

#Combine into one dataframe
df = parks.copy(deep=True)
df['TeamID'] = teamID
df['TeamName'] = teamName
df['SeasonsPlayed'] = seasonsPlayed

df.START = pd.to_datetime(parks.START, format='%Y%m%d', errors='ignore').dt.date
df.END = pd.to_datetime(parks.END, format='%Y%m%d', errors='ignore').dt.date
df['Active'] = df.END.isnull() & df.START.notnull()

#Sanity Check
#Apparently the California Angels has played more seasons than LAA at Angel Stadium
#Same for the Devil Rays vs Rays at Tropicana
df_active = df[df.Active == True]
for i in range(len(df_active)):
    teamName = df_active.iloc[i].TeamName
    parkName = df_active.iloc[i].NAME
    lat = df_active.iloc[i].Latitude
    long = df_active.iloc[i].Longitude
    print("The " + teamName + " play in " + parkName + " located at (" + str(lat) + ", " + str(long) + ")")

#Test distance
#http://www.meridianoutpost.com/resources/etools/calculators/calculator-latitude-longitude-distance.php

coords_1 = (38.872987, -77.007435)
coords_2 = (43.641256, -79.389054)

print(geopy.distance.geodesic(coords_1, coords_2).mi) #351.61 miles

####################################################################################

# Copyright 2018, Gurobi Optimization, LLC
# Modified by Alexander Booth, 2018
# Thanks Gurobi!

# Solve a traveling salesman problem on a randomly generated set of
# points using lazy constraints.   The base MIP model only includes
# 'degree-2' constraints, requiring each node to have exactly
# two incident edges.  Solutions to this model may contain subtours -
# tours that don't visit every city.  The lazy constraint callback
# adds new constraints to cut them off.

# Callback - use lazy constraints to eliminate sub-tours

def subtourelim(model, where):
    if where == g.GRB.Callback.MIPSOL:
        # make a list of edges selected in the solution
        vals = model.cbGetSolution(model._vars)
        selected = g.tuplelist((i,j) for i,j in model._vars.keys() if vals[i,j] > 0.5)
        # find the shortest cycle in the selected edge list
        tour = subtour(selected)
        if len(tour) < n:
            # add subtour elimination constraint for every pair of cities in tour
            model.cbLazy(g.quicksum(model._vars[i,j]
                                  for i,j in itertools.combinations(tour, 2))
                         <= len(tour)-1)


# Given a tuplelist of edges, find the shortest subtour

def subtour(edges):
    unvisited = list(range(n))
    cycle = range(n+1) # initial length has 1 more city
    while unvisited: # true if list is non-empty
        thiscycle = []
        neighbors = unvisited
        while neighbors:
            current = neighbors[0]
            thiscycle.append(current)
            unvisited.remove(current)
            neighbors = [j for i,j in edges.select(current,'*') if j in unvisited]
        if len(cycle) > len(thiscycle):
            cycle = thiscycle
    return cycle

###################################################################################

#All Current
    
n = len(df_active)
points = [(df_active.iloc[i].Latitude, df_active.iloc[i].Longitude) for i in range(n)]
    
dist = {(i,j) :
    geopy.distance.geodesic((points[i][0],points[i][1]), (points[j][0],points[j][1])).mi
    for i in range(n) for j in range(i)}

m = g.Model()

# Create variables
vars = m.addVars(dist.keys(), obj=dist, vtype=g.GRB.BINARY, name='e')
for i,j in vars.keys():
    vars[j,i] = vars[i,j] # edge in opposite direction

# Add degree-2 constraint
m.addConstrs(vars.sum(i,'*') == 2 for i in range(n))
m.update()

# Optimize model
m._vars = vars
m.Params.lazyConstraints = 1
m.optimize(subtourelim)

vals = m.getAttr('x', vars)
selected = g.tuplelist((i,j) for i,j in vals.keys() if vals[i,j] > 0.5)

tour = subtour(selected)
assert len(tour) == n

print('')
print('Optimal tour: %s' % str(tour))
print('Optimal cost: %g' % m.objVal)
print('')

for cityIndx in tour:
    print(df_active.iloc[cityIndx].NAME + ", " + df_active.iloc[cityIndx].CITY)

#Heck yeah it worked
#################################################################################
    
#All Historical
    
n = len(df)
points = [(df.iloc[i].Latitude, df.iloc[i].Longitude) for i in range(n)]
    
dist = {(i,j) :
    geopy.distance.geodesic((points[i][0],points[i][1]), (points[j][0],points[j][1])).mi
    for i in range(n) for j in range(i)}

m = g.Model()
m.setParam('TimeLimit', 10*60) #set time limit

# Create variables
vars = m.addVars(dist.keys(), obj=dist, vtype=g.GRB.BINARY, name='e')
for i,j in vars.keys():
    vars[j,i] = vars[i,j] # edge in opposite direction

# Add degree-2 constraint
m.addConstrs(vars.sum(i,'*') == 2 for i in range(n))
m.update()

# Optimize model
m._vars = vars
m.Params.lazyConstraints = 1
m.optimize(subtourelim)

vals = m.getAttr('x', vars)
selected = g.tuplelist((i,j) for i,j in vals.keys() if vals[i,j] > 0.5)

tour = subtour(selected)
assert len(tour) == n

print('')
print('Optimal tour: %s' % str(tour))
print('Optimal cost: %g' % m.objVal)
print('')

for cityIndx in tour:
    print(df.iloc[cityIndx].NAME + ", " + df.iloc[cityIndx].CITY)