"""
File for basic player class
"""

class Player(object):
    def __init__(self):
        self.hand = None #The player's hand
        self.money = None #How much money/chips the player has
        raise NotImplementedError()

    def bet(self):
        """
        Decides whether the player would like to
        call fold or raise. Returns a tuple with 
        the first element being either 'c', 'f', or 'r'
        for call, fold, and raise repectively.
        The second element being the amount of the bet
        if applicable
        """
        raise NotImplementedError()


