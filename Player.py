"""
File for basic player class
"""

from random import randint


class Player(object):
    def __init__(self, money):
        self.hand = [] #The player's hand
        self.money = money #How much money/chips the player has
        self.isPlaying = True # if fold, turn it to false
        self.id = randint(1, 1000)

    def bet(self, game): 
        """
        Decides whether the player would like to
        call fold or raise. Returns a tuple with 
        the first element being either 'c', 'f', 'r', or 'a'
        for call, fold, raise, and all-in respectively.
        The second element being the amount of the bet
        if applicable
        return None if not applicable
        """
        pass

    def cardPrinter(self, cards):
        """
        Print a group of cards in a decent way
         ______
        |4     |
        |      |
        |      |
        |     D|
         ------
           1
        :param cards: a list of cards
        :return: None
        """
        l = len(cards)
        for i in range(0, l):
            print("     ______ ", end="")
        print()
        for i in range(0, l):
            if len(cards[i][1]) == 1:
                print("    |" + cards[i][1] + "     |", end="")
            else:
                print("    |" + cards[i][1] + "    |", end="")
        print()
        for i in range(0, l):
            print("    |      |", end="")
        print()
        for i in range(0, l):
            print("    |      |", end="")
        print()
        for i in range(0, l):
            print("    |     " + cards[i][0] + "|", end="")
        print()
        for i in range(0, l):
            print("     ------ ", end="")
        print()
        for i in range(0, l):
            print("       " + str(i + 1) + "    ", end="")
        print()