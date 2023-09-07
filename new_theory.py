import pandas as pd
import random
import numpy as np
import time
import matplotlib.pyplot as plt
import pybaseball.pybaseball as pyball
import sklearn.metrics as scikit
from pybaseball import cache
from new_classes import Team

#Given teams current wins,losses, and lists of each game's RS and RA,
#simulates the rest of the season 100000 times and returns the list of 
#end of season wins
def simulateROS(wins,losses,RS,RA):
    trials = 100000
    simulations = []
    GP = wins + losses
    GR = 162 - GP
    
    for i in range(trials):
        team_ros_wins = wins
        for j in range(GR):
            (game_RS,game_RA) = simulateSingleGame(RS,RA)
            if game_RS > game_RA:
                team_ros_wins += 1
        simulations.append(team_ros_wins)
    return simulations
    # plt.hist(simulations,25,(75,100),True)
    # plt.show()
    # np.histogram(simulations)
    # simulations.sort()
    # for k in range(5,100,5):
    #     print(str(k) + ":" + str(simulations[int(trials*(k/100))]))

#Given a list of RS and RA, simulates a single game and returns a tuple
# of that games RS and RA
def simulateSingleGame(RS,RA):
    game_RS = random.choice(RS)
    game_RA = random.choice(RA)
    if game_RS == game_RA:
        return simulateSingleGame(RS,RA)
    else:
        return (game_RS,game_RA)

#Plots both methods of simulating the season, using individual game results
#and individual game run totals
def plotBothMethods(team_wins,team_losses,runs_scored,runs_allowed,sel):
    x = 50
    if len(runs_allowed) > x:
        runs_allowed = getLastN(runs_allowed,x)
        runs_scored = getLastN(runs_scored,x)
    sim1 = simulateROS(team_wins,team_losses,runs_scored,runs_allowed)
    CIN = Team("CIN",team_wins,team_losses,sum(runs_scored),sum(runs_allowed))
    sim2 = CIN.simulatePercentiles()
    lower = min(min(sim1),min(sim2))
    upper = max(max(sim1),max(sim2))
    plt.clf()
    if sel == 1:
        plt.hist(sim1,int(upper-lower+1),(lower-0.5,upper+0.5),alpha = 0.5,label = "Individual Game Runs")
        plt.hist(sim2,int(upper-lower+1),(lower-0.5,upper+0.5),alpha = 0.5,label = "Total Season Runs")
        plt.legend(loc = "upper right")
        plt.show()
    else:
        plt.boxplot([sim1,sim2])
        
        plt.show()

#given a list of RS and RA, plots a histogram of them overlaid
def plotRunsScoredVsRunsAllowed(runs_scored,runs_allowed):
    lower = min(min(runs_scored),min(runs_allowed))
    upper = max(max(runs_scored),max(runs_allowed))

    plt.hist(runs_scored,int(upper-lower+1),(lower-0.5,upper+0.5),alpha = 0.5,label="RS")
    plt.hist(runs_allowed,int(upper-lower+1),(lower-0.5,upper+0.5),alpha = 0.5,label="RA")
    plt.legend(loc = "upper right")
    plt.show()

#given a list of scores, returns the latest x, assuming they were given
# in order
def getLastN(scores,x):
    new = []
    reversedList = scores[::-1]
    for i in range(x):
        new.append(reversedList[i])
    return new

#Prunes a list of scores, only returning run totals
def pruneList(list):
    new = []
    for i in list:
        if i >= 0:
            new.append(i)
    return new

# given a list of RS and RA, returns that teams hypothetical win %
# by using MonteCarlo and simulating 100000 times
def calcWinPer(RS,RA):
    trials = 1000000
    wins = 0
    for i in range(trials):
        [game_RS,game_RA] = simulateSingleGame(RS,RA)
        if game_RS > game_RA:
            wins += 1
    return wins/trials

#Reads and returns alot of the reds data for 2023
def InitializeRedsShit():
    data = pd.read_excel("reds year over year.xlsx","2023")
    runs_scored = data["Reds Runs"].values.tolist()
    runs_allowed = data["Opp Runs"].values.tolist()
    runs_scored = pruneList(runs_scored)
    runs_allowed = pruneList(runs_allowed)
    team_wins = data["Result"].value_counts()["W"]
    team_losses = data["Result"].value_counts()["L"]
    return (runs_scored,runs_allowed,team_wins,team_losses)

#Eh this is boring
def ReadBrefPage(year,name):
    data = pyball.schedule_and_record(year,name)
    RS = data["R"].values.tolist()
    RA = data["RA"].values.tolist()
    RS,RA = pruneList(RS),pruneList(RA)
    # W_L = data["W/L"].values.tolist()
    W = data["W/L"].value_counts()["W"]
    W_wo = data["W/L"].value_counts()["W-wo"]
    L = data["W/L"].value_counts()["L"]
    L_wo = data["W/L"].value_counts()["L-wo"]
    return (RS,RA,W+W_wo,L+L_wo)
              


def compareMethods(W,L,RS,RA):
    sim1 = simulateROS(W,L,RS,RA)
    CIN = Team("CIN",W,L,RS,RA)
    CIN.findWinPer()
    sim2 = CIN.simulatePercentiles()
    lower = min(min(sim1),min(sim2))
    upper = max(max(sim1),max(sim2))
    plt.clf()
    plt.hist(sim1,int(upper-lower+1),(lower-0.5,upper+0.5),alpha = 0.5,label = "My Method")
    plt.hist(sim2,int(upper-lower+1),(lower-0.5,upper+0.5),alpha = 0.5,label = "Their Method")
    plt.legend(loc = "upper right")
    plt.show()

def lastFiveYears():
    cache.enable()

    league = ["NYY","BOS","TBR","BAL","TOR",
              "MIN","DET","CHW","KCR","CLE",
              "OAK","LAA","HOU","TEX","SEA",
              "LAD","SFG","ARI","SDP","COL",
              "CIN","STL","MIL","CHC","PIT",
              "WSN","PHI","ATL","NYM","MIA"]
    years = [2017,2018,2019,2021,2022]
    trueWinPer = []
    denisWinPer = []
    pythWinPer = []
    league_of_objects = []
    # league = ["CIN"]
    for year in years:
        for team in league:
            RS,RA,W,L = ReadBrefPage(year,team)
            invTeam = Team(team,W,L,RS,RA)
            league_of_objects.append(invTeam)
    for team in league_of_objects:
        team.findWinPer()
        trueWinPer.append(team.trueWinPer)
        pythWinPer.append(team.pythWinPer)
        denisWinPer.append(team.denisWinPer)

    x = [0.25,0.4,0.5,0.6,0.75]
    print("My Way: " + str(scikit.r2_score(trueWinPer,denisWinPer)))
    print("Their Way: " + str(scikit.r2_score(trueWinPer,pythWinPer)))
    plt.clf()
    plt.plot(denisWinPer,trueWinPer,"bo",label="My Way")
    plt.plot(pythWinPer,trueWinPer,"ro",label = "Pyth Way")
    plt.legend(loc = "upper right")
    plt.plot(x,x,"-")
    plt.show()

def singleTeamPrediction(team,year):
    cache.purge()
    RS,RA,W,L = ReadBrefPage(year,team)
    compareMethods(W,L,RS,RA)

def calcAbove500(team,year):
    RS,RA,W,L = ReadBrefPage(year,team)
    sim1 = simulateROS(W,L,RS,RA)
    wins = 0
    for game in sim1:
        if game > 81:
            wins += 1
    print(wins/len(sim1))

def main():
    calcAbove500("NYY",2023)


main()