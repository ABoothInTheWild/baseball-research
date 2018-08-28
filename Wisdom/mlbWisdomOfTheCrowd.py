# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 21:47:15 2018

@author: Alexander
"""

#Imports
import pandas as pd
import os
import numpy as np

os.chdir('C:/Users/Alexander/Documents/baseball/Wisdom')

#Load Data
mlb17Pre = pd.read_csv('Mlb_2017_WisdomCrowd.csv')

cols = mlb17Pre.columns
allEstimatesCols = list(cols[2:16])
goodEstimatesCols = list(cols[2:9])
goodEstimatesCols.extend(cols[16:18])

#Wisdom of the crowd with all win estimates
maeErrors = []
rmseErrors = []
for i in allEstimatesCols:
    maeError = np.mean(abs(mlb17Pre[i] - mlb17Pre["2017_Actual_Wins"]))
    rmseError = np.sqrt(((mlb17Pre[i] - mlb17Pre["2017_Actual_Wins"]) ** 2).mean(axis=None))
    
    maeErrors.append(round(maeError,3))
    rmseErrors.append(round(rmseError,3))
    
df = pd.DataFrame(list(zip(allEstimatesCols, maeErrors, rmseErrors)), columns=["Source", "MAE", "RMSE"])
print(df.sort_values("MAE").reset_index(drop=True))
print("")
print(df.sort_values("RMSE").reset_index(drop=True))
print("")

#Wisdom of the crowd with expert win estimates
maeErrors1 = []
rmseErrors1 = []
for i in goodEstimatesCols:
    maeError = np.mean(abs(mlb17Pre[i] - mlb17Pre["2017_Actual_Wins"]))
    rmseError = np.sqrt(((mlb17Pre[i] - mlb17Pre["2017_Actual_Wins"]) ** 2).mean(axis=None))
    
    maeErrors1.append(round(maeError,3))
    rmseErrors1.append(round(rmseError,3))
    
df1 = pd.DataFrame(list(zip(goodEstimatesCols, maeErrors1, rmseErrors1)), columns=["Source", "MAE", "RMSE"])
print(df1.sort_values("MAE").reset_index(drop=True))
print("")
print(df1.sort_values("RMSE").reset_index(drop=True))
print("")

#Graphs

import matplotlib.pyplot as plt
import matplotlib.cm as cm
x = mlb17Pre["2017_Actual_Wins"]
#ys = [mlb17Pre[i] for i in pd.concat([mlb17Pre.iloc[:, 2:9], mlb17Pre.iloc[:, 16:18]],axis=1)]
#ys = [mlb17Pre[i] for i in mlb17Pre.iloc[:, 2:16]]
#ys = list([mlb17Pre["Median_Good"], mlb17Pre["Average_Good"]])
#ys = list([mlb17Pre["Fangraphs_Wins"], mlb17Pre["PECOTA_Wins"]])
ys = list([mlb17Pre["Fangraphs_Wins"], mlb17Pre["BleacherReport1_Wins"]])

#colors = iter(["blue", "red"])
colors = iter(cm.coolwarm(np.linspace(0, 1, len(ys))))
fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=80)
for y in ys:
    plt.scatter(x, y, color=next(colors))
plt.plot([0, 100], [0, 100], color = 'black', linewidth = 1, linestyle='--')
#ax.legend(loc='best', frameon=False) 
plt.title('2017 Actual vs Predicted Wins')
plt.ylabel('Predicted Wins')
plt.xlabel('Actual Wins')
plt.xlim(60, 100)
plt.ylim(60, 100)
plt.grid(b=True, which='major', color='gray', linestyle='--', alpha= 0.3)
fig.legend(loc=7)
fig.tight_layout()
fig.subplots_adjust(right=0.72)  
plt.show()
fig.savefig("PredictedActualFGBR.png", bbox_inches='tight')
