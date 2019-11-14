"""
Runs a game of texas holdem
"""

from itertools import product
from random import shuffle
from AI import AI
from User import User
import heapq
# from copy import deepcopy

class Game(object):
    STAGES = {
        'prehand':'P', #Stage of the game before any players are actually dealt
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

    def __init__(self, money, players=2):
        self.players = []
        self.board = [] ## 5 cards on board
        self.round = 1
        self.initialMoney = money
        self.stage = Game.STAGES['begin']
        self.pot = 0
        self.min = 0 # every time you bet, should greater than this number
        self.deck = self.DECK[:]
        # shuffle(self.deck)
        # raise NotImplementedError()

    # def play_hand(self):
    #     """
    #     Plays through a single hand of texas holdem
    #     using the current amounts of money each player has
    #     """
    #     raise NotImplementedError()

    def play_game(self):
        """
        Plays hands of texas holdem until either
        all players but 1 are bankrupt or the user
        want's the game to stop
        Resets variables after game is finished
        """
        # a human and a computer
        self.players.append(User(self.initialMoney))
        self.players.append(AI(self.initialMoney))

        bankrupt = False
        while(not bankrupt):
            for player in self.players:
                if((player.money == 0) or (player.money < self.min)):
                    bankrupt = True
            if bankrupt:
                break
            else:
                self.playRound()
                if(self.round > 5):
                    self.showdown()
                    # self.round = 1
                    # self.pot = 0
                    # self.board = []
                    # self.deck = deepcopy(self.DECK)

        

    def shuffleDeck(self):
        """
        Shuffles Deck does not return anything
        """
        shuffle(self.deck)


    def assignCards(self):
        """
        Assigns 2 cards to each player for round 1
        Gives 3 cards to board for round 2
        Gives 1 card to board for round 3
        Gives 1 card to board for round 4
        Gives 1 card to board for round 5
        """
        self.shuffleDeck()
        if self.round == 1:
            for player in self.players:
                player.hand.append(self.deck.pop())
                player.hand.append(self.deck.pop())
        elif self.round == 2:
            self.board.append(self.deck.pop())
            self.board.append(self.deck.pop())
            self.board.append(self.deck.pop())
        elif self.round == 3:
            self.board.append(self.deck.pop())
        elif self.round == 4:
            self.board.append(self.deck.pop())
        elif self.round == 5:
            self.board.append(self.deck.pop())
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

        if((self.round > 1) and (self.round <=5)):
            self.assignCards()
            # we continue this round until no one bet
            currentPot = self.pot
            potAfterBet = self.pot+1
            while potAfterBet-currentPot != 0:
                for player in self.players:
                    # player.bet()
                    # if player doesnt fold
                    if player.isPlaying:
                        player.play()
                potAfterBet = self.pot

            self.round += 1
        else:
            print("Game Class playRound Error")

    def unique(self, iterable):
        """
        Give a iterable object, return the unique values in it
        and corresponding counters
        The method is given by Professor Saúl Blanco
        """
        items = list(iterable)
        unique_items = list(set(items))
        counts = [items.count(item) for item in unique_items]
        return unique_items, counts


    def showdown(self):
        """
        Decides who wins the pot
        """
        # {player's rank: index in self.players}
        # play's rank = (rank, a tuple which contains the numerical values of the cards)
        player_with_ranks= {}
        for i in range(0, len(self.players)):
            player = self.players[i]
            # if player doesn't fold
            if player.isPlaying:
                # tell him to select 5 cards among his hand and 5 community cards
                # find the rank of these cards
                rank = player.in_which_rank(player.select_five_cards())
                player_with_ranks[rank] = i

        # if only one player is still on the board
        # give him the money and initialize the game
        if len(player_with_ranks) == 1:
            self.players[player_with_ranks.values()[0]].money += self.pot
            self.round = 1
            self.pot = 0
            self.board = []
            self.deck = self.DECK[:]
            return

        # if we have more than two players left
        # compare their hands
        rankQueue = []
        for rank in player_with_ranks.keys():
            rankQueue.append(rank)
        rankQueue.sort()

        # if first two players are not in the same rank
        # give money to the first player
        if rankQueue[0][0] != rankQueue[1][0]:
            self.players[player_with_ranks[rankQueue[0]]].money += self.pot
            self.round = 1
            self.pot = 0
            self.board = []
            self.deck = self.DECK[:]
            return

        """
        If first two player (we only consider two players so far) are in the same rank
        compare the numerical values of their hands
        """
        # it's impossible that two players both have a royal flush
        # so we skip it

        winner = []
        if rankQueue[0][0] == 2:
            # straight flush
            # we compare the greatest cards in each combination
            if rankQueue[0][1][4] < rankQueue[1][1][4]:
                winner.append(player_with_ranks[rankQueue[1]])
            else:
                winner.append(player_with_ranks[rankQueue[0]])

        elif rankQueue[0][0] == 3:
            # four of a kind
            # since the players must have the same card that appear 4 times
            # so we just need to compare the fifth card
            four1 = rankQueue[0][1][2]
            four2 = rankQueue[1][1][2]
            # find the fifth card
            if four1 == rankQueue[0][1][0]:
                fifth_card1 = rankQueue[0][1][4]
            else:
                fifth_card1 = rankQueue[0][1][0]

            if four2 == rankQueue[1][1][0]:
                fifth_card2 = rankQueue[1][1][4]
            else:
                fifth_card2 = rankQueue[1][1][0]

            if fifth_card1 < fifth_card2:
                winner.append(player_with_ranks[rankQueue[1]])
            elif fifth_card2 == fifth_card1:
                winner.append(player_with_ranks[rankQueue[0]])
                winner.append(player_with_ranks[rankQueue[1]])
            else:
                winner.append(player_with_ranks[rankQueue[0]])

        elif rankQueue[0][0] == 4:
            # full house
            # first compare the threes
            # if equal, then compare the twos
            unique_cards1, counter1 = self.unique(rankQueue[0][1])
            unique_cards2, counter2 = self.unique(rankQueue[1][1])

            if counter1[0] == 3:
                three1 = unique_cards1[0]
                two1 = unique_cards1[1]
            else:
                three1 = unique_cards1[1]
                two1 = unique_cards1[0]

            if counter2[0] == 3:
                three2 = unique_cards2[0]
                two2 = unique_cards2[1]
            else:
                three2 = unique_cards2[1]
                two2 = unique_cards2[0]

            if three1 > three2:
                winner.append(rankQueue[0])
            elif three2 > three1:
                winner.append(rankQueue[1])
            elif three1 == three2:
                if two1 > two2:
                    winner.append(rankQueue[0])
                elif two2 > two1:
                    winner.append(rankQueue[1])
                elif two1 == two2:
                    winner.append(rankQueue[0])
                    winner.append(rankQueue[1])

        elif rankQueue[0][0] == 5:
            # flush
            # we compare from the greatest to the smallest
            cards1 = rankQueue[0][1]
            cards2 = rankQueue[1][1]
            tie = True
            for i in range(0, 5):
                if cards1[i] > cards2[i]:
                    winner.append(rankQueue[0])
                    tie = False
                    break
                elif cards2[i] > cards1[i]:
                    winner.append(rankQueue[1])
                    tie = False
                    break

            if tie:
                winner.append(rankQueue[0])
                winner.append(rankQueue[1])

        elif rankQueue[0][0] == 6:
            # straight
            # compare the greatest value in each combination
            if rankQueue[0][1][4] > rankQueue[1][1][4]:
                winner.append(rankQueue[0])
            elif rankQueue[0][1][4] < rankQueue[1][1][4]:
                winner.append(rankQueue[1])
            else:
                winner.append(rankQueue[0])
                winner.append(rankQueue[1])
        raise NotImplementedError()







if __name__ == '__main__':
    g = Game(0)
    g.stage = 'P'
    p = AI(0)
    p.calc_self_probs(g)