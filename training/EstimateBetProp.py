"""
Estimates the percentage of decisions which result in a bet (not folding)
Findings
Players bet ~70% of the time regardless of how many other players are present.
"""

import os


dirs = os.listdir('./data/')
dirs = [x for x in dirs if "holdem3" in x]
directs = [f"./data/{x}/holdem3" for x in dirs]

bets = {}
bet_codes = ['k', 'b', 'c', 'r', 'A']

for DATA_DIR in directs:
    for x in os.listdir(DATA_DIR):
        for y in os.listdir(DATA_DIR + "/" + x + "/" + "pdb"):
            content = str(open(DATA_DIR + "/" + x + "/" + "pdb" + "/" + y).read())
            content = content.split("\n")
            content = content[:-1]
            content = [x.split() for x in content]
            for r in content:
                p = r[3]
                decisions = ''.join(r[4:7])
                for c in decisions:
                    if c in bet_codes:
                        try:
                            b = bets[p]
                            b = (b[0] + 1, b[1] + 1)
                            bets[p] = b
                        except:
                            bets[p] = (1, 1)
                    elif c == "-" or c == "B":
                        pass
                    else:
                        try:
                            b = bets[p]
                            b = (b[0], b[1] + 1)
                            bets[p] = b
                        except:
                            bets[p] = (0, 1)
                    

    print(bets)        
                    



