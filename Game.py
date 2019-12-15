"""
Runs a game of texas holdem
"""

from itertools import product
from random import shuffle
from random import randint
from AI import AI
from User import User
from itertools import combinations
import heapq
# from copy import deepcopy

def filter_by_suit(suit, cards):
    return list(filter(lambda x: x[0] == suit, cards))

def filter_by_rank(rank, cards):
    return list(filter(lambda x: x[1] == rank, cards))

class Game(object):
    STAGES = {
        'prehand':'P', #Stage of the game before any players are actually dealt
        'begin':'B',
        'flop':'F',
        'turn':'T',
        'river':'R',
    }    
    RANKS = ['2', '3','4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    SUITS = ['H', 'D', 'S', 'C'] # Heart-H, Diamond-D, Spade-S, Club-C

    #A card is represented as a suit rank tuple given as (suit, rank)
    #For example a Jack of hearts would be ('H', 'J')

    DECK = list(product(SUITS, RANKS))

    @classmethod
    def serialize_card(cls, card):
        num = cls.RANKS.index(card[1]) * 4
        num += cls.SUITS.index(card[0]) + 1
        return num

    def __init__(self, players):
        self.players = players
        self.board = [] ## 5 cards on board
        self.round = 1
        self.stage = Game.STAGES['begin']
        self.pot = 0
        self.min = 0 # every time you bet, should greater than this number
        self.deck = self.DECK[:]
        self.playerCodes = {}
        ids = []
        for p in self.players:
            p.decisions = []
            if p.id not in ids:
                ids.append(p.id)
            else:
                i = randint(1, 1000)
                while i in ids:
                    i = randint(1, 1000)
                p.id = i
                ids.append(i)
        # shuffle(self.deck)
        # raise NotImplementedError()

    def rotate_players(self):
        p = self.players.pop(0)
        self.players.append(p)

    def get_or_rotate(self, i):
        return self.players[i%len(self.players)]

    def get_by_id(self, i):
    #returns the player object associated to a given id
        for p in self.players:
            if p.id == i:
                return p
        raise KeyError("No player associated to the given value")

    def demo(self):
        a_i = 1
        p_i = 1
        for p in self.players:
            if isinstance(p, AI):
                self.playerCodes[p.id] = f"AI{a_i}"
                a_i += 1
            else:
                self.playerCodes[p.id] = f"Player{p_i}"
                p_i += 1
        hands = 0
        while all([p.money > 0 for p in self.players]):
            print(f"You've played {hands} hands")
            self.play_hand_demo()       
            hands += 1

    def play_hand_demo(self):
        """
        Plays through hands printing events as they happen
        """
        self.deck = self.DECK[:]
        for p in self.players:
            p.hand = []
        self.board = []
        self.shuffleDeck()
        self.rotate_players()
        self.round = 1
        self.assignCards()
        self.bets = [0 for x in range(len(self.players))]
        self.pot = 75
        self.min = 50
        self.players[0].money -= 25
        self.players[1].money -= 50
        self.bets[0] = 25
        self.bets[1] = 50
        self.inGame = set([x.id for x in self.players])
        self.allIn = set([])
        i = 2%len(self.players)
        self.betting_round(i, demo=True)
        i = 0
        if len(self.inGame) > 1:
            self.round += 1
            self.assignCards()
            self.betting_round(i, demo=True)
        else:
            winner = self.get_by_id(self.inGame.pop())
            winner.money += self.pot
            print(f"{self.playerCodes[winner.id]} won this hand and {self.pot} dollars")
            return
        if len(self.inGame) > 1:
            self.round += 1
            self.assignCards()
            self.betting_round(i, demo=True)
        else:
            winner = self.get_by_id(self.inGame.pop())
            winner.money += self.pot
            print(f"{self.playerCodes[winner.id]} won this hand and {self.pot} dollars")
            return
        if len(self.inGame) > 1:
            self.round += 1
            self.assignCards()
            self.betting_round(i, demo=True)
        else:
            winner = self.get_by_id(self.inGame.pop())
            winner.money += self.pot
            print(f"{self.playerCodes[winner.id]} won this hand and {self.pot} dollars")
            return 
        if len(self.inGame) > 1:
            try:
                winner = self.showdown2()
            except:
                for p in self.inGame:
                    player = self.get_by_id(p)
                    player.money += self.pot/len(self.inGame)
                    print("Players tied")
                    return #Hands are for all intensive purposes tied so training won't really work (skip this set)
        else:
            winner = self.get_by_id(self.inGame.pop())
        winner.money += self.pot
        print(f"{self.playerCodes[winner.id]} won this hand and {self.pot} dollars with a hand of {winner.hand}")
        return

    def play_hand_train(self):
        """
        Plays through a single hand of texas holdem
        using the current amounts of money each player has
        """
        self.deck = self.DECK[:]
        for p in self.players:
            p.hand = []
        self.board = []
        self.shuffleDeck()
        self.rotate_players()
        self.round = 1
        self.assignCards()
        self.bets = [0 for x in range(len(self.players))]
        self.pot = 75
        self.min = 50
        self.players[0].money -= 25
        self.players[1].money -= 50
        self.bets[0] = 25
        self.bets[1] = 50
        self.inGame = set([x.id for x in self.players])
        self.allIn = set([])
        i = 2%len(self.players)
        self.betting_round(i)
        i = 0
        if len(self.inGame) > 1:
            self.round += 1
            self.assignCards()
            self.betting_round(i)
        else:
            winner = self.get_by_id(self.inGame.pop())
            winner.money += self.pot
            for p in self.players:
                if p.id == winner.id:
                    p.do_loss(True, winner.hand, self)
                else:
                    p.do_loss(False, winner.hand, self)
            return
        if len(self.inGame) > 1:
            self.round += 1
            self.assignCards()
            self.betting_round(i)
        else:
            winner = self.get_by_id(self.inGame.pop())
            winner.money += self.pot
            for p in self.players:
                if p.id == winner.id:
                    p.do_loss(True, winner.hand, self)
                else:
                    p.do_loss(False, winner.hand, self)
            return
        if len(self.inGame) > 1:
            self.round += 1
            self.assignCards()
            self.betting_round(i)
        else:
            winner = self.get_by_id(self.inGame.pop())
            winner.money += self.pot
            for p in self.players:
                if p.id == winner.id:
                    p.do_loss(True, winner.hand, self)
                else:
                    p.do_loss(False, winner.hand, self)
            return 
        if len(self.inGame) > 1:
            try:
                winner = self.showdown2()
            except:
                for p in self.inGame:
                    player = self.get_by_id(p)
                    player.money += self.pot/len(self.inGame)
                    return #Hands are for all intensive purposes tied so training won't really work (skip this set)
        else:
            winner = self.get_by_id(self.inGame.pop())
        for p in self.players:
            if p.id == winner.id:
                p.do_loss(True, winner.hand, self)
            else:
                p.do_loss(False, winner.hand, self)
        winner.money += self.pot
        return
                
    def process_bet(self, bet, playerIndex, demo=False):
        r = bet[0]
        if r == "f":
            self.bets[playerIndex] = 0
            self.inGame.remove(self.players[playerIndex].id)
            if demo:
                print(f"{self.playerCodes[self.players[playerIndex].id]} has folded")
        elif r == "c":
            betI = self.bets[playerIndex]
            w = max(self.bets)
            self.players[playerIndex].money -= (w-betI)
            self.pot += (w-betI)
            self.bets[playerIndex] = w
            if demo:
                print(f"{self.playerCodes[self.players[playerIndex].id]} has called")
        elif r == "a":
            self.pot += self.players[playerIndex].money
            if self.players[playerIndex].money + self.bets[playerIndex] <= max(self.bets):
                self.bets[playerIndex] = max(self.bets)
            else:
                self.bets[playerIndex] += self.players[playerIndex].money
            self.players[playerIndex].money = 0
            self.allIn.add(self.players[playerIndex].id)
            if demo:
                print(f"{self.playerCodes[self.players[playerIndex].id]} is all in")
        else:
            if bet[1] < self.min:
                raise ValueError("Raise is less than the min raise")
            else:
                self.min = bet[1]
                b = bet[1] + (max(self.bets) - self.bets[playerIndex])
                self.players[playerIndex].money -= b
                self.pot += b
                self.bets[playerIndex] = bet[1] + max(self.bets)
                if demo:
                    print(f"{self.playerCodes[self.players[playerIndex].id]} has raised {b}")

    def bets_done(self):
        if set(self.bets) - set([0, max(self.bets)]):
            return False
        else:
            return True

    def betting_round(self, initial, demo=False):
        i = initial
        b = self.players[i].bet(self)
        p = self.players[i]
        if p.id not in self.allIn and p.id in self.inGame:
            self.process_bet(b, i, demo=demo)
        i += 1
        while i%len(self.players) != initial and len(self.inGame) > 1:
            p = self.players[i%len(self.players)]
            if p.id not in self.allIn and p.id in self.inGame:
                b = p.bet(self)
                self.process_bet(b, i%len(self.players), demo=demo)
            i += 1
        while not self.bets_done() and len(self.inGame) > 1:
            p = self.players[i%len(self.players)]
            if p.id not in self.allIn and p.id in self.inGame:
                b = p.bet(self)
                self.process_bet(b, i%len(self.players), demo=demo)
            i += 1



        

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


    def compare_hands(self, hand1, hand2):
        """
        compares two hands returning 0 if the first is better
        and then 1 if the second hand is better
        """
        if self.is_royal_flush(hand1) and self.is_royal_flush(hand2):
            result = None
        elif self.is_royal_flush(hand1):
            return 0
        elif self.is_royal_flush(hand2):
            return 1
        result = None
        comparators = [self.compare_straight_flush, self.compare_four_of_a_kind, self.compare_full_house, 
        self.compare_flush, self.compare_straight, self.compare_three_of_a_kind, self.compare_two_pair, self.compare_pair, self.compare_higher_card]
        for c in comparators:
            result = c(hand1, hand2)
            if result is not None:
                return result
        return None

    def showdown2(self):
        players = []
        tie = False
        for pid in self.inGame:
            p = self.get_by_id(pid)
            players.append(p)
        winner = players[0]
        for p in players[1:]:
            r = self.compare_hands(winner.hand + self.board, p.hand + self.board)
            if r == 1:
                winner = p
                tie = False
            elif r == 0:
                pass
            else:
                tie = True
        if tie:
            raise ValueError("Can't compare hands")
        return winner

    def in_hand(self, hand, cards):
        for c in cards:
            if c not in hand:
                return False
        return True

    def is_royal_flush(self, hand):
        straight = ['10', 'J', 'Q', 'K', 'A']
        hands = [[(x, y) for y in straight] for x in self.SUITS]
        return any([self.in_hand(hand, x) for x in hands])

    def compare_straight_flush(self, hand1, hand2):
        allFlushes = [self.RANKS[x:x+5] for x in range(0, 9)]
        allFlushes = allFlushes[::-1]
        allFlushes.append(['A'] + self.RANKS[0:4])
        for f in allFlushes:    
            for s in self.SUITS:
                sCards1 = filter_by_suit(s, hand1)
                sCards1 = [x[1] for x in sCards1]
                sCards2 = filter_by_suit(s, hand2)
                sCards2 = [x[1] for x in sCards2]
                isSF1 = len(set(sCards1).intersection(f)) >= 5
                isSF2 = len(set(sCards2).intersection(f)) >= 5
                if isSF1 and isSF2:
                    return None
                elif isSF1:
                    return 0
                elif isSF2:
                    return 1
        return None

    def compare_four_of_a_kind(self, hand1, hand2):
        for r in self.RANKS[::-1]:
            rc1 = [x[1] for x in hand1].count(r)
            rc2 = [x[1] for x in hand2].count(r)
            if rc1 == 4 and rc2 == 4:
                return None
            elif rc1 == 4:
                return 0
            elif rc2 == 4:
                return 1
        return None
    
    def compare_full_house(self, hand1, hand2):
        combs = combinations(self.RANKS, 2)
        combs = list(combs)[::-1]
        for comb in combs:
            c1 = comb[1]
            c2 = comb[0]
            ranks1 = [x[1] for x in hand1]
            ranks2 = [x[1] for x in hand2]
            r1 = ranks1.count(c1) >= 3 and ranks1.count(c2) >= 2
            r2 = ranks1.count(c1) >= 3 and ranks1.count(c2) >= 2
            if r1 and r2:
                return None
            elif r1:
                return 0
            elif r2:
                return 1
            c1 = comb[0]
            c2 = comb[1]
            ranks1 = [x[1] for x in hand1]
            ranks2 = [x[1] for x in hand2]
            r1 = ranks1.count(c1) >= 3 and ranks1.count(c2) >= 2
            r2 = ranks1.count(c1) >= 3 and ranks1.count(c2) >= 2
            if r1 and r2:
                return None
            elif r1:
                return 0
            elif r2:
                return 1
        return None

    def compare_flush(self, hand1, hand2):
        suit1 = [x[0] for x in hand1]
        suit2 = [x[0] for x in hand2]
        suitCount1 = max([suit1.count(x) for x in self.SUITS])
        suitCount2 = max([suit2.count(x) for x in self.SUITS])
        if suitCount1 >= 5 and suitCount2 >= 5:
            return self.compare_higher_card(hand1, hand2)
        elif suitCount1 >= 5:
            return 0
        elif suitCount2 >= 5:
            return 1
        return None
            
    def compare_straight(self, hand1, hand2):
        allFlushes = [self.RANKS[x:x+5] for x in range(0, 9)]
        allFlushes = allFlushes[::-1]
        allFlushes.append(['A'] + self.RANKS[0:4])
        for f in allFlushes:    
            sCards1 = [x[1] for x in hand1]
            sCards2 = [x[1] for x in hand2]
            isF1 = len(set(sCards1).intersection(f)) >= 5
            isF2 = len(set(sCards2).intersection(f)) >= 5
            if isF1 and isF2:
                return None
            elif isF1:
                return 0
            elif isF2:
                return 1
        return None

    def compare_three_of_a_kind(self, hand1, hand2):
        for r in self.RANKS[::-1]:
            rc1 = [x[1] for x in hand1].count(r)
            rc2 = [x[1] for x in hand2].count(r)
            if rc1 == 3 and rc2 == 3:
                return None
            elif rc1 == 3:
                return 0
            elif rc2 == 3:
                return 1
        return None

    def compare_two_pair(self, hand1, hand2):
        combs = combinations(self.RANKS, 2)
        combs = list(combs)[::-1]
        for comb in combs:
            c1 = comb[1]
            c2 = comb[0]
            ranks1 = [x[1] for x in hand1]
            ranks2 = [x[1] for x in hand2]
            r1 = ranks1.count(c1) >= 2 and ranks1.count(c2) >= 2
            r2 = ranks1.count(c1) >= 2 and ranks1.count(c2) >= 2
            if r1 and r2:
                return None
            elif r1:
                return 0
            elif r2:
                return 1
        return None

    def compare_pair(self, hand1, hand2):
        for r in self.RANKS[::-1]:
            rc1 = [x[1] for x in hand1].count(r)
            rc2 = [x[1] for x in hand2].count(r)
            if rc1 == 2 and rc2 == 2:
                return None
            elif rc1 == 2:
                return 0
            elif rc2 == 2:
                return 1
        return None

    def compare_higher_card(self, hand1, hand2):
        ranks1 = [x[1] for x in hand1] 
        ranks2 = [x[1] for x in hand2]
        ranks1 = [self.RANKS.index(x) for x in ranks1]
        ranks2 = [self.RANKS.index(x) for x in ranks2]
        if not ranks1: #Hands are equivalent (used for training only)
            return None
        if max(ranks1) == max(ranks2):
            h1 = hand1[:]
            h2 = hand2[:]
            h1.pop(ranks1.index(max(ranks1)))
            h2.pop(ranks2.index(max(ranks2)))
            return self.compare_higher_card(h1, h2)
        elif max(ranks1) > max(ranks2):
            return 0
        else:
            return 1

if __name__ == '__main__':
    players = []
    startingPlayers = int(input("How many AIs would you like to play against?"))
    model = "./params/best.pkl"
    for x in range(startingPlayers):
        p = AI(5000)
        p.load_model_from_path(model)
        players.append(p)
    u = User(5000)
    players.append(u)
    g = Game(players)
    g.demo()
    