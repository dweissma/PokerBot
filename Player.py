"""
File for basic player class
"""

from Game import Game


class Player(object):
    def __init__(self, money):
        self.hand = [] #The player's hand
        self.money = money #How much money/chips the player has
        self.isPlaying = True # if fold, turn it to false

    def bet(self, action, amount): 
        """
        Decides whether the player would like to
        call fold or raise. Returns a tuple with 
        the first element being either 'c', 'f', or 'r'
        for call, fold, and raise respectively.
        The second element being the amount of the bet
        if applicable
        return -1 if not
        """

        if action == 'r':
            self.money -= amount
            self.pot += amount
        elif action == 'c':
            print("Hand: "+self.hand)
        else:
            self.isPlaying = False



        raise NotImplementedError() 




