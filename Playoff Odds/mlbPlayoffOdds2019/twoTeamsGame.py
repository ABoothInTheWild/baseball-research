# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 13:50:14 2019

@author: ABooth
"""

# Imports
# prepare for Python version 3x features and functions
from __future__ import division, print_function

import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
from scipy.stats import norm
import matplotlib.pyplot as plt
import os

#World Series 2017 Simulator
#Using Negative Binomial Disribution

#Alexander Booth
#October 24, 2017

#Set Directory
os.chdir('C:/Users/abooth/Documents/Python Scripts/PastPreds/mlbPlayoffOdds2019')

from RunsScoredAllowedSimulator import *

#define data
texas = pd.read_csv(r"TEX_2019_RegularSeason.csv")
texas["Home/Away"] = pd.get_dummies(texas['Unnamed: 4'])

houston = pd.read_csv(r"HOU_2019_RegularSeason.csv")
houston["Home/Away"] = pd.get_dummies(houston['Unnamed: 4'])

texasSub = texas[["R", "RA", "Home/Away"]].astype("float")
houstonSub = houston[["R", "RA", "Home/Away"]].astype("float")

#Stats
texasSub.corr()
houstonSub.corr()

print(np.mean(texasSub[texasSub["Home/Away"] == 0]["R"]))
print(np.mean(texasSub[texasSub["Home/Away"] == 1]["R"]))
print(np.mean(texasSub[texasSub["Home/Away"] == 0]["RA"]))
print(np.mean(texasSub[texasSub["Home/Away"] == 1]["RA"]))

print(np.mean(houstonSub[houstonSub["Home/Away"] == 0]["R"]))
print(np.mean(houstonSub[houstonSub["Home/Away"] == 1]["R"]))
print(np.mean(houstonSub[houstonSub["Home/Away"] == 0]["RA"]))
print(np.mean(houstonSub[houstonSub["Home/Away"] == 1]["RA"]))

##################################################
#Histograms
# the histogram of the data
fig, ax = plt.subplots(1, 1)
n, bins, patches = ax.hist(houstonSub.R, 10, density=1, facecolor='blue', alpha=0.75, label="")
mu = np.mean(houstonSub.R)
sigma = np.std(houstonSub.R)

# add a 'best fit' line
y = norm.pdf(bins, mu, sigma)
l = ax.plot(bins, y, 'r--', linewidth=1, label="NegBin Approx")
ax.legend(loc='best', frameon=False)
plt.xlabel('Runs Scored')
plt.ylabel('Frequency')
plt.xlim([0,20])
plt.ylim([0,.2])
plt.title(r'Houston Runs Scored')
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
y = norm.pdf(bins, mu2, sigma)
l = ax.plot(bins, y, 'r--', linewidth=1, label="NegBin Approx")
ax.legend(loc='best', frameon=False)
plt.xlabel('Runs Scored')
plt.ylabel('Frequency')
plt.xlim([0,20])
plt.ylim([0,.2])
plt.title(r'Simulated Houston Runs Scored')
plt.grid(False)

plt.show()

##################################################
#Histograms
# the histogram of the data
fig, ax = plt.subplots(1, 1)
n, bins, patches = ax.hist(texasSub.R, 10, density=1, facecolor='blue', alpha=0.75, label="")
mu = np.mean(texasSub.R)
sigma = np.std(texasSub.R)

# add a 'best fit' line
y = norm.pdf(bins, mu, sigma)
l = ax.plot(bins, y, 'r--', linewidth=1, label="NegBin Approx")
ax.legend(loc='best', frameon=False)
plt.xlabel('Runs Scored')
plt.ylabel('Frequency')
plt.xlim([0,20])
plt.ylim([0,.2])
plt.title(r'Texas Runs Scored')
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
y = norm.pdf(bins, mu2, sigma)
l = ax.plot(bins, y, 'r--', linewidth=1, label="NegBin Approx")
ax.legend(loc='best', frameon=False)
plt.xlabel('Runs Scored')
plt.ylabel('Frequency')
plt.xlim([0,20])
plt.ylim([0,.2])
plt.title(r'Simulated Texas Runs Scored')
plt.grid(False)

plt.show()

numSims = 100000
df2 = RunsSimulator(texasSub, houstonSub, True, numSims, 4, 1)

print("Houston Win Percentage: " , len(df2[df2.WinningTeam == "Team2"])/float(numSims))
print("Texas Win Percentage: " , len(df2[df2.WinningTeam == "Team1"])/float(numSims))

#df.to_csv("HOUvsLAD_Simulation_Results_100000.csv", index=False)

#####################################################################################