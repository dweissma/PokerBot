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



        # raise NotImplementedError()

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
            if len(cards[i][0]) == 1:
                print("    |" + cards[i][0] + "     |", end="")
            else:
                print("    |" + cards[i][0] + "    |", end="")
        print()
        for i in range(0, l):
            print("    |      |", end="")
        print()
        for i in range(0, l):
            print("    |      |", end="")
        print()
        for i in range(0, l):
            print("    |     " + cards[i][1] + "|", end="")
        print()
        for i in range(0, l):
            print("     ------ ", end="")
        print()
        for i in range(0, l):
            print("       " + str(i + 1) + "    ", end="")

    """
    The following methods are used to decide which rank are the 5 selected cards in
    """

    def is_royal_flush(self, cards):

        raise NotImplementedError()

    def is_straight_flush(self, cards):
        raise NotImplementedError()

    def is_four_of_a_kind(self, cards):
        raise NotImplementedError()

    def is_full_house(self, cards):
        raise NotImplementedError()

    def is_flush(self, cards):
        raise NotImplementedError()

    def is_straight(self, cards):
        raise NotImplementedError()

    def is_three_of_a_kind(self, cards):
        raise NotImplementedError()

    def is_two_pairs(self, cards):
        raise NotImplementedError()

    def is_pair(self, cards):
        raise NotImplementedError()
