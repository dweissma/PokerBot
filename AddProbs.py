"""
Makes hand objects from files
"""

import os
import ast
import AI
import Game

OUTPUT_DIR = './training/processed/with_probs/'

def convert_card(card):
    rank = card[0]
    suit = card[1]
    suit = suit.upper()
    return (suit, rank)

a = AI.AI(0)
g = Game.Game(0)

dirs = os.listdir('./training/processed/no_probs/')

for files in dirs:
    content = open('./training/processed/no_probs/' + files).read()
    content = str(content)
    content = content.split("\n")
    if not content[-1]:
        content = content[:-1]
    with open(OUTPUT_DIR + files, "a+") as out:
        for decisions in content:
            d = decisions.split('\t')
            hand = ast.literal_eval(d[0])
            hand = [convert_card(x) for x in hand]
            b = ast.literal_eval(d[1])
            g.board = [convert_card(x) for x in b]
            a.hand = hand
            pot = int(d[2])
            bet_players = int(d[3])
            und_players = int(d[4])
            g.players = [None for x in range(bet_players + und_players)]
            prob = a.training_prob_bh(g, bet_players, und_players, pot)
            decisions += "\t" + str(prob) + "\n"
            out.write(decisions)


