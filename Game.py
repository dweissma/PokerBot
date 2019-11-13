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
        self.board = [] ## 5 cards on board
        self.round = 1
        self.initialMoney = money
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
        Resets variables after game is finished
        """
        bankrupt = False
        while(not bankrupt):
            for player in self.players:
                if((player.money == 0) or (player.money < self.min)):
                    bankrupt = True
            if bankrupt: 
                break
            else:
                self.playRound
                if(self.round > 5):
                    self.round = 1
                    self.pot = 0
                    self.board = []
                    self.deck = self.DECK[:]

        

    def shuffleDeck(self):
        """
        Shuffles Deck does not return anything
        """
        random.shuffle(self.deck)

    def assignCards(self):
        """
        Assigns 2 cards to each player for round 1
        Gives 3 cards to board for round 2
        Gives 1 card to board for round 3
        Gives 1 card to board for round 4
        Gives 1 card to board for round 5
        """
        self.shuffleDeck()
        if(self.round == 1):
            for player in self.players:
                player.hand.append(self.deck.pop())
                player.hand.append(self.deck.pop())
        elif(self.round == 2):
            board.append(self.deck.pop())
            board.append(self.deck.pop())
            board.append(self.deck.pop())
        elif(self.round == 3):
            board.append(self.deck.pop())
        elif(self.round == 4):
            board.append(self.deck.pop())
        elif(self.round == 5):
            board.append(self.deck.pop())
        else:
            print("Game has Finished")
    def playRound(self):
        """
        Does not change the order of players playing the game // We can change this later, but might be easier for Neural net if bot always goes second or first
        //Shuffles Deck
        //Assigns cards to player
        //Collect bets
        //Increasess round
        """
        self.shuffleDeck()
        if((self.round >= 1) and (self.round <=5)):
            self.assignCards

            for player in self.players:
                player.bet()
            self.round+=1
        else:
            print("Game Class playRound Error")
    
     

        
    
    