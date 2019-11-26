"""
Our AI which plays Texas Holdem
"""

from Player import Player
from scipy.special import comb
from numpy import nan, isnan
from itertools import combinations
from math import exp
import torch
import torch.nn as nn
import torch.nn.functional as F

def filter_by_suit(suit, cards):
    return list(filter(lambda x: x[0] == suit, cards))

def filter_by_rank(rank, cards):
    return list(filter(lambda x: x[1] == rank, cards))

class AI(Player, nn.Module):
    CARDSLEFT = {
        'P': 7,
        'B': 5,
        'F': 2,
        'T': 1,
        'R': 0,
    }  

    DEFAULT_PK = 0.7
    DEFAULT_POT_FACT = 1/300
    
    ORDERING = ['RF', 'SF', 'FK', 'FH', 'FL', 'ST', 'TK', 'TP', 'PA']

    def __init__(self, money):
        super(AI, self).__init__(money)
        self.inputLayer = nn.Linear(11, 10)
        self.hidden = nn.Linear(10, 10)
        self.output = nn.Linear(10, 2)
        #First output node tells whether to fold or not and the second decides how much to bet

    def forward(self, x):
        x = F.relu(self.inputLayer(x))
        x = F.relu(self.hidden(x))
        x = F.relu(self.output(x))
        return x

    def calc_loss(self, outcome, bet, output):
        if outcome < 0:
            target = (50, 0)
        else:
            target = (0, bet)
        output[0] = output[0] * 50
        return nn.MSELoss(output, target)

    
    def play(self):
        # the ai always raise a minimum
        self.bet('r', self.min)

    def fix_probs(self, toFix):
        soFar = 0
        for keys in self.ORDERING:
            prob_key = toFix[keys]
            if soFar >= 1:
                toFix[keys] = 0
            elif prob_key < 0:
                toFix[keys] = 0
            elif prob_key > 1:
                toFix[keys] = 1 #Two straights can cause a calculation error
            else:
                soFar += prob_key


    def calc_self_probs(self, game):
        cards = self.hand + game.board
        players = len(game.players)
        cardsInDeck = len(game.deck)
        unknownCards = 52 - len(cards)
        left = 7 - len(cards)
        if left == 0:
            return
        self.probs = {}
        self.probs['RF'] = self.royal_flush(game, cards, cardsInDeck, left) 
        self.probs['SF'] = self.straight_flush(game, cards, cardsInDeck, left) 
        self.probs['FK'] = self.four_of_a_kind(game, cards, cardsInDeck, left) 
        self.probs['FH'] = self.full_house(game, cards, cardsInDeck, left)
        self.probs['FL'] = self.flush(game, cards, cardsInDeck, left) - self.probs['RF'] -self.probs['SF']
        self.probs['ST'] = self.straight(game, cards, cardsInDeck, left) -self.probs['RF'] - self.probs['SF']
        self.probs['TK'] = self.three_of_a_kind(game, cards, cardsInDeck, left) - self.probs['FK'] - self.probs['FH']
        self.probs['TP'] = self.two_pair(game, cards, cardsInDeck, left) - self.probs['FH']
        self.probs['PA'] = self.pair(game, cards, cardsInDeck, left) - self.probs['FH'] -self.probs['TP'] 

    def p_oppbetter_hand(self, hand):
        """
        Uses the other probs dict to estimate a naive probability
        that the opponent has a better hand than the given hand
        """
        if hand is None:
            ind = len(self.ORDERING)
        else:
            ind = self.ORDERING.index(hand)
        probs = [self.otherProbs[x] for x in self.ORDERING[:ind]]
        return sum(probs)

    def calc_other_probs(self, game):
        cards = game.board
        players = len(game.players)
        cardsInDeck = len(game.deck)
        unknownCards = 52 - len(cards)
        left = 7 - len(game.board)
        if left == 0:
            return
        self.otherProbs = {}
        self.otherProbs['RF'] = self.royal_flush(game, cards, cardsInDeck, left) 
        self.otherProbs['SF'] = self.straight_flush(game, cards, cardsInDeck, left) 
        self.otherProbs['FK'] = self.four_of_a_kind(game, cards, cardsInDeck, left) 
        self.otherProbs['FH'] = self.full_house(game, cards, cardsInDeck, left)
        self.otherProbs['FL'] = self.flush(game, cards, cardsInDeck, left) - self.otherProbs['RF'] -self.otherProbs['SF']
        self.otherProbs['ST'] = self.straight(game, cards, cardsInDeck, left) -self.otherProbs['RF'] - self.otherProbs['SF']
        self.otherProbs['TK'] = self.three_of_a_kind(game, cards, cardsInDeck, left) - self.otherProbs['FK'] - self.otherProbs['FH']
        self.otherProbs['TP'] = self.two_pair(game, cards, cardsInDeck, left) - self.otherProbs['FH']
        self.otherProbs['PA'] = self.pair(game, cards, cardsInDeck, left) - self.otherProbs['FH'] - self.otherProbs['TK'] -self.otherProbs['TP'] - self.otherProbs['FK']

    def royal_flush(self, game, cards, inDeck, left):
        known = len(cards)
        cumProb = 0
        rRanks = set(game.RANKS[-5:])
        for suit in game.SUITS:
            suitCards = filter_by_suit(suit, cards)
            suitRanks = [x[1] for x in suitCards]
            combined = len(set(suitRanks).intersection(rRanks))
            wrong = known - combined
            freedom = left - (5-combined)
            if freedom >= 0:
                N = 52 - wrong - 5 #Number of unknowns which don't contribute and could still be dealt
                k = freedom #Number of spots to deal unknowns to
                suitProb = comb(N, k)/comb(52-known, left)
                cumProb += suitProb
            else:
                continue
        return cumProb

    def straight_flush(self, game, cards, inDeck, left):
        known = len(cards)
        cumProb = 0
        allFlushes = [game.RANKS[x:x+5] for x in range(0, 8)]
        for suit in game.SUITS:
            suitCards = filter_by_suit(suit, cards)
            suitRanks = [x[1] for x in suitCards]
            for flushes in allFlushes:
                combined = len(set(suitRanks).intersection(flushes))
                wrong = known - combined
                freedom = left - (5-combined)
                if freedom >= 0:
                    N = 52 - wrong - 5 #Number of unknowns which don't contribute and can be dealt
                    k = freedom #Number of spots to deal noncontributing cards to
                    flushProb = comb(N, k)/comb(52-known, left)
                    less1 = game.RANKS[game.RANKS.index(flushes[0])-1]
                    if less1 in suitRanks and less1 != 'A':
                        prob1less = 1
                    elif less1 != 'A':
                        prob1less = comb(N-1, k-1)/comb(52-known, left)
                    else:
                        prob1less = 0
                    mutprob = prob1less * flushProb
                    flushProb -= mutprob
                    cumProb += flushProb
        return cumProb

    def four_of_a_kind(self, game, cards, inDeck, left):
        known = len(cards)
        cumProb = 0
        for rank in game.RANKS:
            rankCount = len(filter_by_rank(rank, cards))
            wrong = known - rankCount
            freedom = left - (4-rankCount)
            if freedom >= 0:
                N = 52 - wrong - 4
                k = freedom
                rankProb = comb(N, k)/comb(52-known, left)
                cumProb += rankProb
        return cumProb

    def full_house(self, game, cards, inDeck, left):
        known = len(cards)
        cumProb = 0
        for pair in combinations(game.RANKS, 2):
            rank1Count = len(filter_by_rank(pair[0], cards))
            rank2Count = len(filter_by_rank(pair[1], cards))
            ranksCount = rank1Count + rank2Count
            if ranksCount == 5:
                return 1
            wrong = known - ranksCount
            freedom = left - (5-ranksCount)
            if freedom >= 0:
                N = 52 - wrong - 5
                k = freedom
                if rank1Count <=2 and rank2Count <= 2:
                    pairProb = ((comb(4-rank1Count, 2) * comb(4-rank2Count, 1)) + (comb(4-rank2Count, 2) * comb(4-rank1Count, 1)))  * comb(N, k)/comb(52-known, left) #There are 4C2 * 4C! ways to pick the suits and 2 ranks to pick suits for
                elif rank1Count > 2 and rank2Count <= 2:
                    pairProb = comb(4-rank2Count, 2) * comb(N, k)/comb(52-known, left)
                elif rank2Count > 2 and rank1Count <= 2:
                    pairProb = comb(4-rank1Count, 2) * comb(N, k)/comb(52-known, left)
                else:
                    pairProb = 1
                cumProb += pairProb
        return cumProb

    def flush(self, game, cards, inDeck, left):
        known = len(cards)
        cumProb = 0
        for suit in game.SUITS:
            suitCount = len(filter_by_suit(suit, cards))
            wrong = known - suitCount
            freedom = left - (5-suitCount)
            if freedom >= 0:
                N = 52 - wrong - 5
                k = freedom
                suitProb = comb(13-suitCount, 5-suitCount) * comb(N, k)/comb(52-known, left)
                cumProb += suitProb
        return cumProb

    def straight(self, game, cards, inDeck, left):
        known = len(cards)
        cumProb = 0
        allFlushes = [game.RANKS[x:x+5] for x in range(0, 9)]
        ranks = [x[1] for x in cards]
        for flushes in allFlushes:
                combined = len(set(ranks).intersection(flushes))
                wrong = known - combined
                freedom = left - (5-combined)
                if freedom >= 0:
                    N = 52 - wrong - 5 #Number of unknowns which don't contribute and can be dealt
                    k = freedom #Number of spots to deal noncontributing cards to
                    if freedom > 0:
                        flushProb = ((4**(5-combined))*comb(N, k)/comb(52-known, left))
                        flushProb -=  11 * (comb(N-1, k-1)/comb(52-known, freedom)) * flushProb 
                    else:
                        flushProb = ((4**(5-combined))*comb(N, k)/comb(52-known, left))
                    cumProb += flushProb
        return cumProb

    def three_of_a_kind(self, game, cards, inDeck, left):
        known = len(cards)
        cumProb = 0
        for rank in game.RANKS:
            rankCount = len(filter_by_rank(rank, cards))
            if rankCount == 3:
                return 1
            wrong = known - rankCount
            freedom = left - (3-rankCount)
            rankProb = 0
            if freedom >= 0:
                N = 52 - wrong - 3
                k = freedom
                rankProb = comb(4-rankCount,1)*(comb(N, k)/comb(52-known, left)) # 4C1 ways to make this particular 3 of a kind (since we ignored suit)
                mutProb = 0
                for ranks in filter(lambda x: game.RANKS.index(x) < game.RANKS.index(rank), game.RANKS):
                    rankCount = len(filter_by_rank(rank, cards))
                    wrong = known - rankCount
                    freedomMut = freedom - (3-rankCount)
                    mutProb = 0
                    if freedomMut >= 0:
                        N = 52 - wrong - 3
                        k = freedomMut
                        mutProb = comb(4-rankCount,1)*(comb(N, k)/comb(52-known, left))
                rankProb -= mutProb * rankProb
                cumProb += rankProb
        return cumProb

    def two_pair(self, game, cards, inDeck, left):
        known = len(cards)
        cumProb = 0
        for pair in combinations(game.RANKS, 2):
            rank1Count = len(filter_by_rank(pair[0], cards))
            rank2Count = len(filter_by_rank(pair[1], cards))
            ranksCount = rank1Count + rank2Count
            wrong = known - ranksCount
            freedom = left - (4-ranksCount)
            pairProb = 0
            if freedom >= 0:
                N = 52 - wrong - 4
                k = freedom
                if rank1Count < 2 and rank2Count < 2:
                    pairProb = (comb(4-rank1Count, 2) * comb(4-rank2Count, 2))  * comb(N, k)/comb(52-known, left) #There are 4C2 * 4C! ways to pick the suits and 2 ranks to pick suits for
                elif rank1Count >= 2 and rank2Count < 2:
                    pairProb = comb(4-rank2Count, 2) * comb(N, k)/comb(52-known, left)
                elif rank2Count > 2 and rank1Count < 2:
                    pairProb = comb(4-rank1Count, 2) * comb(N, k)/comb(52-known, left)
                else:
                    return 1
                mutProb = 0
                if freedom > 0:
                    mutProb = comb(4-rank1Count, 1) * (comb(N-1, k-1)/comb(52-known, left-1))
                    mutProb += comb(4-rank2Count, 1) * (comb(N-1, k-1)/comb(52-known, left-1))
                for rank in game.RANKS:
                    if rank not in pair:# and rank < min(pair):
                        rankCount = len(filter_by_rank(rank, cards))
                        wrong = known - rankCount
                        freedomMut = freedom - (2-rankCount)
                        if freedomMut >= 0:
                            N = 52 - wrong - 2
                            k = freedomMut
                            rankProb = comb(4-rankCount, 2) * (comb(N, k)/comb(52-known, freedom)) #4C2 ways to make this particular pair (since we ignored suit)
                            mutProb += rankProb * pairProb
                pairProb -= mutProb
                cumProb += pairProb
        return cumProb

    def pair(self, game, cards, inDeck, left):
        known = len(cards)
        cumProb = 0
        for rank in game.RANKS:
            rankCount = len(filter_by_rank(rank, cards))
            if rankCount == 2:
                return 1
            wrong = known - rankCount
            freedom = left - (2-rankCount)
            rankProb = 0
            if freedom >= 0:
                N = 52 - wrong - 2
                k = freedom
                rankProb = comb(4-rankCount, 2) * (comb(N, k)/comb(52-known, left)) #4C2 ways to make this particular pair (since we ignored suit)
                mutProb = 0
                if freedom > 0:
                    mutProb = comb(4-rankCount, 1) * (comb(N-1, k-1)/comb(52-known, left))
                rankProb -= mutProb * rankProb
            cumProb += rankProb
        return cumProb

    def better_hands(self, hand):
        return self.ORDERING[:self.ORDERING.index(hand)]

    def estimate_bet_prob(self, oBH, pSize, pK, potFact=None):
        """
        Function used to model the probability that an opponent will bet
        Takes a probability that the opponent has the best hand, a pot size,
        and a betting constant used to model how aggressive a player is
        """
        if potFact is None:
            potFact = self.DEFAULT_POT_FACT
        pfact = pSize * potFact
        pfact = 1/(1+exp(pfact))
        r = (pfact + pK)/2
        if isnan(oBH**r):
            print(f"nan found r: {r} oBH: {oBH}")
            print(self.otherProbs)
        return oBH**r

    def model_opponent(self, bet, pSize=None, pK=None):
        """
        Returns the probability than an opponent has a better hand than you 
        """
        if pK is None:
            pK = self.DEFAULT_PK
        soFar = 0
        if not bet:
            for hands in self.ORDERING[1:]:
                soFar += (self.p_oppbetter_hand(hands) * self.probs[hands])
            noGood = (self.p_oppbetter_hand(None) * (1- sum(self.probs.values())))
            if noGood <= 1 and noGood > 0:
                soFar += noGood
            return soFar
        else:
            #Calculate what the opponent thinks their probability of having the best hand is
            p_bet = 0
            for hands in self.ORDERING:
                bHprob = (1-self.p_oppbetter_hand(hands)) 
                if self.otherProbs[hands] > 0:
                    p_bet += self.estimate_bet_prob(bHprob, pSize, pK) * self.otherProbs[hands]
            totProb = 0
            for hands in self.ORDERING[1:]:
                hand_prob = 0
                for h in self.better_hands(hands):
                    bHprob = (1-self.p_oppbetter_hand(h)) 
                    if self.otherProbs[h] > 0:
                        hand_prob += self.estimate_bet_prob(bHprob, pSize, pK) * self.otherProbs[h]
                hand_prob = hand_prob/p_bet
                totProb += hand_prob * self.probs[hands]
            return totProb

    def prob_best_hand(self, bettors, total):
        """
        Takes a list of players still in the game and a list of players who bet
        and a list of all the player still in the game
        """
        if len(total) == 0:
            return 1 #There's no one else left
        nonbets = [x for x in total if x not in bettors]
        nonBetProb = self.model_opponent(False)
        totProb = 0
        for x in range(len(nonbets)):
            totProb += nonBetProb - (nonBetProb * totProb)
        for x in range(len(bettors)):
            #TODO add player specific pKs
            betProb = self.model_opponent(True)
            totProb += betProb - (betProb * totProb)
        return 1-totProb

    def training_prob_bh(self, game, bettors, nonbettors, potSize):
        """
        Takes a number of players still in the game and a number of players who bet
        and a game
        """
        if bettors + nonbettors == 0:
            return 1
        self.calc_self_probs(game)
        self.calc_other_probs(game)
        self.fix_probs(self.probs)
        self.fix_probs(self.otherProbs)
        self.debug_probs(game)
        nonBetProb = self.model_opponent(False, potSize)
        betProb = self.model_opponent(True, potSize)
        totProb = 0
        for x in range(nonbettors):
            totProb += nonBetProb - (nonBetProb * totProb)
        for x in range(bettors):
            totProb += betProb - (betProb * totProb)
        return 1 - totProb 

    def debug_probs(self, game):
        for k, v in self.probs.items():
            if v >1 or v < 0:
                print(f"{k} gives incorrect prob {v} for player hand")
                print(f"The following hand {self.hand} and board {game.board} caused this error")
                print(self.probs)
        for k, v in self.otherProbs.items():
            if v >1 or v < 0:
                print(f"{k} gives incorrect prob {v} for nonplayer hand")
                print(f"The following board {game.board} caused this error")

    def select_five_cards(self):
        raise NotImplementedError()

