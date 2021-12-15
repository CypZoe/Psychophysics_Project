#Adapted from the demo code used in class

#import libraries
import pandas as pd
import matplotlib.pyplot as plt

from statistics import mean
from os import listdir
from scipy.stats import norm
import numpy as np
from statsmodels.stats.anova import AnovaRM


#d' function
def dPrime(hitRate, FArate):
    stat = norm.ppf(hitRate) - norm.ppf(FArate)

    return stat

#criterion function
def criterion(hitRate, FArate):
    stat = -.5*(norm.ppf(hitRate) + norm.ppf(FArate))

    return stat

#data frame for mean SDTs
meanSDTs = pd.DataFrame({"participant" : [], "condition" : [], "hits" : [], "misses": [], "CRs": [], "FAs": [], "dPrime": [], "criterion": []})

#import raw data
dataPath = "data/"
fileList = listdir(dataPath)

#Count participants
counter = 0 #Initialize counter to 0
for dataFile in fileList:
    #New ID for each participant
    counter += 1
    pNum = "P-" + str(counter)
    rawData = pd.read_csv(dataPath + dataFile)


    #Create new data frame
    expData = pd.DataFrame(rawData, columns = ["Condition", "Trial", "key_resp_2.keys", "key_resp_2.rt"]) #Import raw data from specified columns

    #rename columns
    expData = expData.rename(columns = {"Condition" : "condition", "Trial" : "task", "key_resp_2.keys" : "resp", "key_resp_2.rt" : "RT"})


    #the data frame we'll be using
    accuracy = pd.DataFrame({"condition" : ["Still", "Move"], "hits" : [0,0], "misses" : [0,0], "CRs" : [0,0], "FAs" : [0,0]})



#updating the data frame for each entry
    for index, row in expData.iterrows():
        #condition: still
        if row["condition"] == "Still":
            rowInd = 0
            if row["task"] == "go" and row["resp"] == "space":
                accuracy.loc[rowInd,"hits"] += 1
            #Miss
            elif row["task"] == "go" and row["resp"] == "None":
                accuracy.loc[rowInd,"misses"] += 1
                #Correct rejection
            elif row["task"] == "no-go" and row["resp"] == "None":
                accuracy.loc[rowInd,"CRs"] += 1
            elif row["task"] == "no-go" and row["resp"] == "space":
                accuracy.loc[rowInd,"FAs"] += 1

        #condition: move
        elif row["condition"] == "Move":
                rowInd = 1
                #Hit
                if row["task"] == "go" and row["resp"] == "space":
                    accuracy.loc[rowInd,"hits"] += 1
                #Miss
                elif row["task"] == "go" and row["resp"] == "None":
                    accuracy.loc[rowInd,"misses"] += 1
                #Correct rejection
                elif row["task"] == "no-go" and row["resp"] == "None":
                    accuracy.loc[rowInd,"CRs"] += 1
                #False alarm
                elif row["task"] == "no-go" and row["resp"] == "space":
                    accuracy.loc[rowInd,"FAs"] += 1

    #Calculate hit rate for still condition
    hitRateStill = (accuracy.loc[0,"hits"]-1)/16
    #Calculate FA rate for stil condition
    FArateStill = (accuracy.loc[0,"FAs"]+1)/16
    #Calculate hit rate for move condition
    hitRateMove = (accuracy.loc[1,"hits"]-1)/16
    #Calculate FA rate for move condition
    FArateMove = (accuracy.loc[1,"FAs"]+1)/16

    #Data lists
    pNumList = [pNum, pNum]
    condList = ["Still", "Move"]
    hitList = [accuracy.loc[0, "hits"],accuracy.loc[1, "hits"]]
    missList = [accuracy.loc[0, "misses"],accuracy.loc[1, "misses"]]
    CRsList = [accuracy.loc[0, "CRs"],accuracy.loc[1, "CRs"]]
    FAsList = [accuracy.loc[0, "FAs"],accuracy.loc[1, "FAs"]]


    #calculate dPrime for each condition
    dPrimeList = [dPrime(hitRateStill, FArateStill), dPrime(hitRateMove, FArateMove)]
    #Calculate criterion for each condition
    criterionList = [criterion(hitRateStill, FArateStill), criterion(hitRateMove, FArateMove)]

    #new datsa --> data frame
    newLines = pd.DataFrame({"participant" : pNumList, "condition" : condList, "hits": hitList, "misses": missList, "CRs": CRsList, "FAs": FAsList, "dPrime": dPrimeList, "criterion": criterionList})
    #append new line to meanSDTs
    meanSDTs = meanSDTs.append(newLines, ignore_index=True)

#Print meanSDTd
print(meanSDTs)



#anova for dPrime
model = AnovaRM(data = meanSDTs, depvar = "dPrime", subject = "participant", within = ["condition"]).fit()
print(model)

#anova for criterion
model = AnovaRM(data = meanSDTs, depvar = "criterion", subject = "participant", within = ["condition"]).fit()
print(model)



#Condition bar graph

still_cond = [accuracy.loc[0, "hits"], accuracy.loc[0, "misses"], accuracy.loc[0, "CRs"], accuracy.loc[0, "FAs"]] #still condition accuracy
move_cond = [accuracy.loc[1, "hits"], accuracy.loc[1, "misses"], accuracy.loc[1, "CRs"], accuracy.loc[1, "FAs"]] #move condition accuracy

xLabels = ['hits', 'misses', 'CRs', 'FAs'] #Declare x tick labels
x = np.arange(len(xLabels))  # set x label locations
width = 0.35  # set the width of the bars

fig, ax = plt.subplots()
bar1 = ax.bar(x - width/2, still_cond, width, label='Still') #declare bar1
bar2 = ax.bar(x + width/2, move_cond, width, label='Move') #declare bar2

# Add labels
ax.set_ylabel('Trials') #y axis label
ax.set_title('Mean Response by Location of Stimuli') #graph title
ax.set_xticks(x) #call lacation of x label location
ax.set_xticklabels(xLabels) #call labels for the x-axis bars
ax.legend((bar1, bar2), ('Still','Move'))

plt.show()


#Box plot
fig, ax = plt.subplots()
box = ax.boxplot([dPrimeList, criterionList])
ax.set_ylabel('score')
ax.set_title('Reaction Time by Location of Stimuli')
ax.set_xticklabels(["dPrime", "Criterion"])
plt.show()
