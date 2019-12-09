"""
Self play script which iteratively eliminates the AI doing the worst
until only one survivor remains
"""

from Game import Game
from AI import AI
from numpy.random import normal
from random import randint
from math import sqrt
import torch

GAMES = 250
HANDS = 100 #HANDS PER GAME
OUTPUT = "./params/selfcons.pkl"
LROUT = "./params/LRLogCons.txt"
startingSD = 0.1


def get_lr(n):
    k = normal(winning_lr, startingSD/sqrt(n))
    if k < 1 and k > 0:
        return k
    else:
        return get_lr(n)

winning_lr = 0.0161309382673114 
winning_dict = torch.load("./params/self750.pkl")
with open(LROUT, "a+") as f:
    for i in range(GAMES):
        n = i + 1
        startingPlayers = randint(2, 10)
        print(f"starting game with {startingPlayers} players")
        players = []
        for x in range(startingPlayers):
            p = AI(5000, learnRate=get_lr(n))
            p.load_model_from_dict(winning_dict)
            players.append(p)
        while len(players) > 1:
            g = Game(players)
            loans = {}
            for p in players:
                loans[p.id] = 0
            for h in range(HANDS):
                g.play_hand_train()
                for p in players:
                    if p.money <= 0:#Give bankrupt players a loan
                        p.money = 5000
                        loans[p.id] += 5000
            #Determine the winner
            for p in players:
                p.money -= loans[p.id]
            loser = min(players, key=lambda x: x.money)
            print(f"Loser lost {5000-loser.money} dollars")
            players.pop(players.index(loser)) #Remove the loserS
            for p in players:
                p.money = 5000
        winner = max(players, key=lambda x: x.money)
        winning_lr = winner.learnRate
        winning_dict = winner.state_dict()
        print(f"After {n} rounds the best learning rate is {winning_lr}")
        f.write(str(winning_lr) + "\n")

torch.save(winning_dict, OUTPUT)