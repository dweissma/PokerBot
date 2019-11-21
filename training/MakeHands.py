"""
Makes hand objects from files
"""

import os

OUTPUT_DIR = './processed/'

OUTPUT = '.txt'

dirs = os.listdir('./data/')
dirs = [x for x in dirs if "holdem3" in x]
directs = [f"./data/{x}/holdem3" for x in dirs[dirs.index("holdem3.200002"):]]

def get_first(ls, key):
    for x in ls:
        if key(x):
            return x
    return None

def stringify(*args):
    sargs = [str(x) for x in args]
    return "\t".join(sargs)

def isCard(string):
    if string[-1] in ['s','c','h','d']:
        return True
    else:
        return False

for DATA_DIR in directs:
    player_list = []
    hand_list = []
    for x in os.listdir(DATA_DIR):
        player_list = []
        hand_list = []
        done = []
        with open(OUTPUT_DIR + x + OUTPUT, 'a+') as f:
            for y in os.listdir(DATA_DIR + '/' + x):
                if y == "pdb":
                    for player_file in os.listdir(DATA_DIR + '/' + x + '/' + y):
                        player_string = open(DATA_DIR + '/' + x + '/' + y + '/' + player_file).read()
                        hands = str(player_string)
                        hands = hands.split("\n")
                        hands = [x.split() for x in hands if x]
                        #print(hands)
                        player_list.append(hands)
                elif y == "hdb":
                    hand_string = open(DATA_DIR + '/' + x + '/' + y)
                    hands = list(hand_string)
                    #print(hands)
                    hand_list = [x.split() for x in hands]
            for i in range(len(player_list)):
                player = player_list[i]
                #print(player_list)
                for hand in player:
                    iden = hand[1]
                    if iden not in done:
                        this_hand = []
                        showdown = []
                        for p in player_list:
                            b = get_first(p, lambda x: x[1] == iden)
                            if b is not None:
                                this_hand.append(b)
                                if isCard(b[-1]):
                                    showdown.append(b)
                        if showdown:
                            hand_info = get_first(hand_list, lambda x: x[0] == iden)
                            this_hand = sorted(this_hand, key=lambda x: x[3])
                            decisions = [x[4:8] for x in this_hand]
                            for shows in showdown:
                                s_hand = shows[-2:]
                                s_pos = int(shows[3]) - 1
                                s_decisions = decisions[s_pos]
                                board = hand_info[-5:]
                                bet = shows[-4]
                                winnings = shows[-3]
                                net = int(winnings) - int(bet)
                                for d_i in range(len(s_decisions)):
                                    ds = s_decisions[d_i]
                                    for c_i in range(len(ds)):
                                        c = ds[c_i]
                                        bet_players = 0
                                        un_players = 0
                                        for p in decisions[:s_pos]:
                                            try:
                                                dp = p[d_i]
                                                if dp == "B":
                                                    un_players +=1
                                                elif dp == "-" or dp == "f":
                                                    pass
                                                else:
                                                    bet_players +=1
                                            except:
                                                pass
                                        if d_i == 0:
                                            this_board = []
                                            this_pot = 75
                                        elif d_i == 1:
                                            this_board = board[:-2]
                                            this_pot = hand_info[4]
                                            this_pot = this_pot[this_pot.index("/")+1:]
                                        elif d_i == 2:
                                            this_board = board[:-1]
                                            this_pot = hand_info[5]
                                            this_pot = this_pot[this_pot.index("/")+1:]
                                        else:
                                            this_board = board
                                            this_pot = hand_info[6]
                                            this_pot = this_pot[this_pot.index("/")+1:]
                                        un_players += len(decisions) - s_pos + 1
                                        s = stringify(s_hand, this_board, this_pot, bet_players, un_players, winnings, bet, net)
                                        s += "\n"
                                        f.write(s)
                        done.append(iden)
        f.close()
                    



