#Adapted from the demo code used in class

#import libraries
import pandas as pd
import matplotlib.pyplot as plt

from statistics import mean
from os import listdir
from statsmodels.stats.anova import AnovaRM

#import raw data
dataPath = "data/"
fileList = listdir(dataPath)

#data frame for mean RTs
meanRTs = pd.DataFrame({"participant" : [], "condition" : [], "mean RT" : []})

#Count participants
counter = 0 #initialize counter to 0
for dataFile in fileList:
    # Create a new ID for each participant
    counter += 1
    pNum = "P-" + str(counter)
    rawData = pd.read_csv(dataPath + dataFile)

    #Create new data frame
    expData = pd.DataFrame(rawData, columns = ["Condition", "Trial", "key_resp_2.rt", "key_resp_2.keys"]) #Import raw data from specified columns
    #Rename columns
    expData = expData.rename(columns = {"Condition" : "condition", "Trial" : "trial", "key_resp_2.rt" : "RT", "key_resp_2.keys" : "response"})
    #only include trials with a response
    expData = expData[expData.RT.notnull()]

    #only include trials with correct test responses for RT analysis
    rtData = expData[(expData.trial == "go") & (expData.response == "space")] #only correct attributions

    #Data frame for RTs for each condition
    stillRTs = rtData[(rtData.trial == "go") & (rtData.condition == "Still")].RT
    moveRTs = rtData[(rtData.trial == "go") & (rtData.condition == "Move")].RT

    #Data lists
    pNumList = [pNum, pNum]
    condList = ["Still", "Move"]
    meanRTsList = [mean(stillRTs), mean(moveRTs)]

    #new data --> data frame
    newLines = pd.DataFrame({"participant" : pNumList, "condition" : condList, "mean RT" : meanRTsList})
    #append new lines to RT
    meanRTs = meanRTs.append(newLines, ignore_index=True)

#print meanRTs
print(meanRTs)

#Group means for each condition
stillMeans = meanRTs[meanRTs.condition == "Still"]["mean RT"]
moveMeans = meanRTs[meanRTs.condition == "Move"]["mean RT"]

#Print group means for each condition
print("Still condition, go mean RT:", mean(stillMeans))
print("Move condition, go mean RT", mean(moveMeans))

#anova
model = AnovaRM(data = meanRTs, depvar = "mean RT", subject = "participant", within = ["condition"]).fit()
print(model)


#Box plot
fig, ax = plt.subplots()
box = ax.boxplot([stillMeans, moveMeans])
ax.set_ylabel('RT (s)')
ax.set_title('Reaction Time by Location of Stimuli')
ax.set_xticklabels(["Center (Still)", "Corners (Move)"])
plt.show()

quit()
#Bar graph
fig, ax = plt.subplots()
bars = ax.bar([.5,1], [mean(stillMeans), mean(moveMeans)], width=.4)
ax.set_ylabel('RT (s)')
ax.set_title('Mean Reaction Time by Location of Stimuli')
ax.set_xticks([.5,1])
ax.set_xticklabels(["Center (Still)", "Corners (Move)"])
plt.show()
