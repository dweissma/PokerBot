"""
Trains the neural network using the data in /training/processed/with_probs/
"""

import torch.optim as optim
import torch
from Game import Game
from AI import AI
from random import shuffle
from math import cos, pi
import os
import ast
DATADIR = "./training/processed/with_probs/"
PARAMDIR = './params/test.pkl'
BATCHSIZE = 100

getNext = True

def learning_rate(n, cycleLen = 20, max_max = 0.01, min_max = 0.00001, abs_min = 0.00001, batch_num = 10000):
    #Use a cyclic learning rate https://arxiv.org/abs/1506.01186
    return abs(cos(n*(pi/cycleLen))) * ((max_max-abs_min) + ((min_max-max_max)/batch_num)) + abs_min

def make_node(row):
    row = row.split('\t')
    hand = ast.literal_eval(row[0])
    hand = [Game.serialize_card(x) for x in hand]
    board = ast.literal_eval(row[1])
    board = [Game.serialize_card(x) for x in board]
    while len(board) < 5:
        board.append(0)
    pot = int(row[2])
    bet_players = int(row[3])
    und_players = int(row[4])
    b_out = float(row[-1])
    return hand + board + [pot, bet_players, und_players, b_out]

def make_output_info(row):
    row = row.split('\t')
    net = int(row[-2])
    bet = int(row[-3])
    return (net, bet)

def pop_batch_size(ls, n):
    toReturn = []
    while n > 0:
        try:
            add = ls.pop()
            if len(add) > 0:
                toReturn.append(add)
                n -= 1
        except IndexError:
            global getNext
            getNext = True
            return toReturn 
    return toReturn

def set_lr(lr, o):
    for param_group in o.param_groups:
        param_group['lr'] = lr

batchCount = 0
net = AI(0)
optimizer = optim.SGD(net.parameters(), lr=0.01)
datasets = os.listdir(DATADIR) 
shuffle(datasets)#Do training in a random order
for ds in datasets:
    print(f"starting {ds}")
    f = str(open(DATADIR + ds).read())
    f = f.split("\n")
    getNext = False
    while not getNext:
        batch = pop_batch_size(f, BATCHSIZE)
        if batch:
            batchIn = [make_node(x) for x in batch]
            batchIn = torch.FloatTensor(batchIn)
            batchInfo = [make_output_info(x) for x in batch]
            lr = learning_rate(batchCount)
            set_lr(lr, optimizer)
            optimizer.zero_grad()
            output = net(batchIn)
            loss = net.calc_loss(batchInfo, output)
            loss.backward()
            optimizer.step()
            batchCount += 1

torch.save(net.state_dict(), PARAMDIR)
