"""
Runs a game of texas holdem
"""

from itertools import product
from random import shuffle

class Game(object):
    STAGES = {
        'begin':'B',
        'flop':'F',
        'turn':'T',
        'river':'R',
    }    
    RANKS = ['2', '3',' 4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    SUITS = ['H', 'D', 'S', 'C'] # Heart-H, Diamond-D, Spade-S, Club-C

    #A card is represented as a suit rank tuple given as (suit, rank)
    #For example a Jack of hearts would be ('H', 'J')

    DECK = list(product(RANKS, SUITS))

    def __init__(self, players, money):
        self.players = []
        self.initialMoney = money
        self.publicCards = []
        self.stage = Game.STAGES['begin']
        self.pot = 0
        self.min = 0 # every time you bet, should greater than this number
        self.deck = self.DECK[:]
        shuffle(self.deck)
        raise NotImplementedError()

    def play_hand(self):
        """
        Plays through a single hand of texas holdem
        using the current amounts of money each player has
        """
        raise NotImplementedError()

    def play_game(self):
        """
        Plays hands of texas holdem until either
        all players but 1 are bankrupt or the user
        want's the game to stop
        """
        raise NotImplementedError()
        
    
    