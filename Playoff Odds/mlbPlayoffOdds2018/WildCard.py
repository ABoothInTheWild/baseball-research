# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 15:53:49 2018

@author: ABooth
"""

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

#Wild Card 2018 Simulator
#Using Negative Binomial Disribution


#Set Directory

from RunsScoredAllowedSimulator import *

#define data
rockies = pd.read_csv(r"COL_2018_RegularSeason.csv")
rockies["Home/Away"] = pd.get_dummies(rockies['Unnamed: 4'])

cubs = pd.read_csv(r"CHC_2018_RegularSeason.csv")
cubs["Home/Away"] = pd.get_dummies(cubs['Unnamed: 4'])

rockiesSub = rockies[["R", "RA", "Home/Away"]].astype("float")
cubsSub = cubs[["R", "RA", "Home/Away"]].astype("float")

#Stats
rockiesSub.corr()
cubsSub.corr()

print(np.mean(rockiesSub[rockiesSub["Home/Away"] == 0]["R"]))
print(np.mean(rockiesSub[rockiesSub["Home/Away"] == 1]["R"]))
print(np.mean(rockiesSub[rockiesSub["Home/Away"] == 0]["RA"]))
print(np.mean(rockiesSub[rockiesSub["Home/Away"] == 1]["RA"]))

print(np.mean(cubsSub[cubsSub["Home/Away"] == 0]["R"]))
print(np.mean(cubsSub[cubsSub["Home/Away"] == 1]["R"]))
print(np.mean(cubsSub[cubsSub["Home/Away"] == 0]["RA"]))
print(np.mean(cubsSub[cubsSub["Home/Away"] == 1]["RA"]))

##################################################
#Histograms
# the histogram of the data
fig, ax = plt.subplots(1, 1)
n, bins, patches = ax.hist(cubsSub.R, 10, density=1, facecolor='blue', alpha=0.75)
mu = np.mean(cubsSub.R)
sigma = np.std(cubsSub.R)

# add a 'best fit' line
y = mlab.normpdf( bins, mu, sigma)
l = ax.plot(bins, y, 'r--', linewidth=1)

plt.xlabel('Runs Scored')
plt.ylabel('Frequency')
plt.xlim([0,20])
plt.ylim([0,.2])
plt.title(r'Cubs Runs Scored')
plt.grid(False)

plt.show()

size = 4
np.random.seed(123)
test = np.random.negative_binomial(size, size/(size+mu), 1000)

# the histogram of the data
fig, ax = plt.subplots(1, 1)
n, bins, patches = ax.hist(test, 10, density=1, facecolor='blue', alpha=0.75)
mu2 = np.mean(test)
sigma = np.std(test)

# add a 'best fit' line
y = mlab.normpdf( bins, mu2, sigma)
l = ax.plot(bins, y, 'r--', linewidth=1)

plt.xlabel('Runs Scored')
plt.ylabel('Frequency')
plt.xlim([0,20])
plt.ylim([0,.2])
plt.title(r'Simulated Cubs Runs Scored')
plt.grid(False)

plt.show()

##################################################
#Histograms
# the histogram of the data
fig, ax = plt.subplots(1, 1)
n, bins, patches = ax.hist(rockiesSub.R, 10, density=1, facecolor='blue', alpha=0.75)
mu = np.mean(rockiesSub.R)
sigma = np.std(rockiesSub.R)

# add a 'best fit' line
y = mlab.normpdf( bins, mu, sigma)
l = ax.plot(bins, y, 'r--', linewidth=1)

plt.xlabel('Runs Scored')
plt.ylabel('Frequency')
plt.xlim([0,20])
plt.ylim([0,.2])
plt.title(r'Rockies Runs Scored')
plt.grid(False)

plt.show()

size = 4
np.random.seed(123)
test = np.random.negative_binomial(size, size/(size+mu), 1000)

# the histogram of the data
fig, ax = plt.subplots(1, 1)
n, bins, patches = ax.hist(test, 10, density=1, facecolor='blue', alpha=0.75)
mu2 = np.mean(test)
sigma = np.std(test)

# add a 'best fit' line
y = mlab.normpdf( bins, mu2, sigma)
l = ax.plot(bins, y, 'r--', linewidth=1)

plt.xlabel('Runs Scored')
plt.ylabel('Frequency')
plt.xlim([0,20])
plt.ylim([0,.2])
plt.title(r'Simulated Rockies Runs Scored')
plt.grid(False)

plt.show()

##############################################################################
numSims = 100000
wildCardAL = RunsSimulator(cubsSub, rockiesSub, True, 1, numSims, 4)

df = pd.DataFrame(wildCardAL, columns = ["cubsScore", "rockiesScore"])
df["WinningTeam"] = np.where(df['cubsScore'] > df["rockiesScore"], 'cubs', 'rockies')

print("Rockies Win Percentage: " , len(df[df.WinningTeam == "rockies"])/float(numSims))
print("Cubs Win Percentage: " , len(df[df.WinningTeam == "cubs"])/float(numSims))

#df.to_csv("HOUvsLAD_Simulation_Results_100000.csv", index=False)

#####################################################################################

#define data
oakland = pd.read_csv(r"OAK_2018_RegularSeason.csv")
oakland["Home/Away"] = pd.get_dummies(oakland['Unnamed: 4'])

yankees = pd.read_csv(r"NYY_2018_RegularSeason.csv")
yankees["Home/Away"] = pd.get_dummies(yankees['Unnamed: 4'])

oaklandSub = oakland[["R", "RA", "Home/Away"]].astype("float")
yankeesSub = yankees[["R", "RA", "Home/Away"]].astype("float")

#Stats
oaklandSub.corr()
yankeesSub.corr()

print(np.mean(oaklandSub[oaklandSub["Home/Away"] == 0]["R"]))
print(np.mean(oaklandSub[oaklandSub["Home/Away"] == 1]["R"]))
print(np.mean(oaklandSub[oaklandSub["Home/Away"] == 0]["RA"]))
print(np.mean(oaklandSub[oaklandSub["Home/Away"] == 1]["RA"]))

print(np.mean(yankeesSub[yankeesSub["Home/Away"] == 0]["R"]))
print(np.mean(yankeesSub[yankeesSub["Home/Away"] == 1]["R"]))
print(np.mean(yankeesSub[yankeesSub["Home/Away"] == 0]["RA"]))
print(np.mean(yankeesSub[yankeesSub["Home/Away"] == 1]["RA"]))

##################################################
#Histograms
# the histogram of the data
fig, ax = plt.subplots(1, 1)
n, bins, patches = ax.hist(yankeesSub.R, 10, density=1, facecolor='blue', alpha=0.75, label="")
mu = np.mean(yankeesSub.R)
sigma = np.std(yankeesSub.R)

# add a 'best fit' line
y = mlab.normpdf( bins, mu, sigma)
l = ax.plot(bins, y, 'r--', linewidth=1, label="NegBin Approx")
ax.legend(loc='best', frameon=False)
plt.xlabel('Runs Scored')
plt.ylabel('Frequency')
plt.xlim([0,20])
plt.ylim([0,.2])
plt.title(r'Yankees Runs Scored')
plt.grid(False)

plt.show()

size = 4
np.random.seed(123)
test = np.random.negative_binomial(size, size/(size+mu), 1000)

# the histogram of the data
fig, ax = plt.subplots(1, 1)
n, bins, patches = ax.hist(test, 10, density=1, facecolor='blue', alpha=0.75, label="")
mu2 = np.mean(test)
sigma = np.std(test)

# add a 'best fit' line
y = mlab.normpdf( bins, mu2, sigma)
l = ax.plot(bins, y, 'r--', linewidth=1, label="NegBin Approx")
ax.legend(loc='best', frameon=False)
plt.xlabel('Runs Scored')
plt.ylabel('Frequency')
plt.xlim([0,20])
plt.ylim([0,.2])
plt.title(r'Simulated Yankees Runs Scored')
plt.grid(False)

plt.show()

##################################################
#Histograms
# the histogram of the data
fig, ax = plt.subplots(1, 1)
n, bins, patches = ax.hist(oaklandSub.R, 10, density=1, facecolor='blue', alpha=0.75, label="")
mu = np.mean(oaklandSub.R)
sigma = np.std(oaklandSub.R)

# add a 'best fit' line
y = mlab.normpdf( bins, mu, sigma)
l = ax.plot(bins, y, 'r--', linewidth=1, label="NegBin Approx")
ax.legend(loc='best', frameon=False)
plt.xlabel('Runs Scored')
plt.ylabel('Frequency')
plt.xlim([0,20])
plt.ylim([0,.2])
plt.title(r'Oakland Runs Scored')
plt.grid(False)

plt.show()

size = 4
np.random.seed(123)
test = np.random.negative_binomial(size, size/(size+mu), 1000)

# the histogram of the data
fig, ax = plt.subplots(1, 1)
n, bins, patches = ax.hist(test, 10, density=1, facecolor='blue', alpha=0.75, label="")
mu2 = np.mean(test)
sigma = np.std(test)

# add a 'best fit' line
y = mlab.normpdf( bins, mu2, sigma)
l = ax.plot(bins, y, 'r--', linewidth=1, label="NegBin Approx")
ax.legend(loc='best', frameon=False)
plt.xlabel('Runs Scored')
plt.ylabel('Frequency')
plt.xlim([0,20])
plt.ylim([0,.2])
plt.title(r'Simulated Oakland Runs Scored')
plt.grid(False)

plt.show()

numSims = 100000
wildCardAL = RunsSimulator(yankeesSub, oaklandSub, True, 1, numSims, 4)

df2 = pd.DataFrame(wildCardAL, columns = ["yankeesScore", "oaklandScore"])
df2["WinningTeam"] = np.where(df2['yankeesScore'] > df2["oaklandScore"], 'yankees', 'oakland')

print("Oakland Win Percentage: " , len(df2[df2.WinningTeam == "oakland"])/float(numSims))
print("Yankees Win Percentage: " , len(df2[df2.WinningTeam == "yankees"])/float(numSims))

#df.to_csv("HOUvsLAD_Simulation_Results_100000.csv", index=False)

#####################################################################################
