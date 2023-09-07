import random

class Team:
    def __init__(self, name, wins,losses,RS,RA):
        self.name=name
        self.wins=wins
        self.losses=losses
        self.RS=RS
        self.RA=RA
        self.GR=162-wins-losses
        self.GP=wins+losses
    
    def findWinPer(self):
        self.pythWinPer=0.000693*(sum(self.RS)-sum(self.RA))+0.5
        self.trueWinPer=self.wins/self.GP
        self.denisWinPer = calcWinPer(self.RS,self.RA)

    def simulatePercentiles(self):
        trials=100000
        simulations = []
        for i in range(trials):
            team_ros_wins = self.wins
            for j in range(self.GR):
                game = random.random()
                if (self.pythWinPer>=game): 
                    team_ros_wins+=1
            simulations.append(team_ros_wins)
        return simulations
        
def calcWinPer(RS,RA):
    trials = len(RS) * len(RA)
    wins = 0
    for single_RS in RS:
        for single_RA in RA:
            if single_RS > single_RA:
                wins += 1
            elif single_RS == single_RA:
                wins += 0.5
    # for i in range(trials):
    #     [game_RS,game_RA] = simulateSingleGame(RS,RA)
    #     if game_RS > game_RA:
    #         wins += 1
    return wins/trials

def simulateSingleGame(RS,RA):
    game_RS = random.choice(RS)
    game_RA = random.choice(RA)
    if game_RS == game_RA:
        return simulateSingleGame(RS,RA)
    else:
        return (game_RS,game_RA)
    