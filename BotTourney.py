"""
Pits the various bots against each other
"""

from Game import Game
from AI import AI
from numpy.random import normal
from random import randint
from math import sqrt
import torch


OUTPUT = "./params/best.pkl"
HANDS = 1000

players = []

bots = ["./params/100_epochs.pkl", "./params/self750.pkl", "./params/selfcons.pkl"]

for x in bots:
    for y in range(1, 4):
        lr = 0.1 * y
        p = AI(5000, lr)
        p.load_model_from_path(x)
        players.append(p)

g = Game(players)
loans = {}
for p in players:
    loans[p.id] = 0
for x in range(HANDS):
    print(x)
    g.play_hand_train()
    for p in players:
        if p.money <= 0:#Give bankrupt players a loan
            p.money = 5000
            loans[p.id] += 5000
for p in players:
    p.money -= loans[p.id]
winner = max(players, key=lambda x: x.money)
winning_lr = winner.learnRate
winning_dict = winner.state_dict()
print(f"The best learning rate is {winning_lr}")
print(f"The winner won {winner.money} dollars")
torch.save(winning_dict, OUTPUT)
pids = [p.id for p in players]
winI = pids.index(winner.id)
if winI < 3:
    print("100 epochs won")
elif winI < 6:
    print("self play won")
else:
    print("survivor won")