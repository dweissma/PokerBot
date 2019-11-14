"""
Our AI which plays Texas Holdem
"""

from Player import Player
from scipy.special import comb
from itertools import combinations

def filter_by_suit(suit, cards):
    return list(filter(lambda x: x[0] == suit, cards))

def filter_by_rank(rank, cards):
    return list(filter(lambda x: x[1] == rank, cards))

class AI(Player):
    CARDSLEFT = {
        'P': 7,
        'B': 5,
        'F': 2,
        'T': 1,
        'R': 0,
    }  

    def __init__(self, money):
        super().__init__(money)

    def play(self):
        # the ai always raise a minimum
        self.bet('r', self.min)

    def calc_self_probs(self, game: Game):
        cards = self.hand + game.board
        players = len(game.players)
        cardsInDeck = len(game.deck)
        unknownCards = cardsInDeck + (players-1) * 2
        left = self.CARDSLEFT[game.stage]
        self.probs = {}
        self.probs['RF'] = self.royal_flush(game, cards, cardsInDeck, left) 
        self.probs['SF'] = self.straight_flush(game, cards, cardsInDeck, left) 
        self.probs['FK'] = self.four_of_a_kind(game, cards, cardsInDeck, left) 
        self.probs['FH'] = self.full_house(game, cards, cardsInDeck, left)
        self.probs['FL'] = self.flush(game, cards, cardsInDeck, left) - self.probs['RF'] -self.probs['SF']
        self.probs['ST'] = self.straight(game, cards, cardsInDeck, left) -self.probs['RF'] - self.probs['SF']
        self.probs['TK'] = self.three_of_a_kind(game, cards, cardsInDeck, left) - self.probs['FK'] - self.probs['FH']
        self.probs['TP'] = self.two_pair(game, cards, cardsInDeck, left) - self.probs['FH']
        self.probs['PA'] = self.pair(game, cards, cardsInDeck, left) - self.probs['FH'] - self.probs['TK'] -self.probs['TP'] - self.probs['FK']
        print(self.probs)

    def royal_flush(self, game: Game, cards, inDeck, left):
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

    def straight_flush(self, game:Game, cards, inDeck, left):
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

    def four_of_a_kind(self, game:Game, cards, inDeck, left):
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

    def full_house(self, game:Game, cards, inDeck, left):
        known = len(cards)
        cumProb = 0
        for pair in combinations(game.RANKS, 2):
            rank1Count = len(filter_by_rank(pair[0], cards))
            rank2Count = len(filter_by_rank(pair[1], cards))
            ranksCount = rank1Count + rank2Count
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

    def flush(self, game:Game, cards, inDeck, left):
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

    def straight(self, game:Game, cards, inDeck, left):
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
                    flushProb = (4**(5-combined))*comb(N, k)/comb(52-known, left)
                    less1 = game.RANKS[game.RANKS.index(flushes[0])-1]
                    if less1 in ranks and less1 != 'A':
                        prob1less = 1
                    elif  less1 != 'A':
                        prob1less = 4 * comb(N-1, k-1)/comb(52-known, left)
                    else:
                        prob1less = 0
                    mutprob = prob1less * flushProb
                    flushProb -= mutprob
                    cumProb += flushProb
        return cumProb

    def three_of_a_kind(self, game:Game, cards, inDeck, left):
        known = len(cards)
        cumProb = 0
        for rank in game.RANKS:
            rankCount = len(filter_by_rank(rank, cards))
            wrong = known - rankCount
            freedom = left - (3-rankCount)
            rankProb = 0
            if freedom >= 0:
                N = 52 - wrong - 3
                k = freedom
                rankProb = comb(4-rankCount,1)*(comb(N, k)/comb(52-known, left)) # 4C1 ways to make this particular 3 of a kind (since we ignored suit)
                for ranks in filter(lambda x: x < rank, game.RANKS):
                    rankCount = len(filter_by_rank(rank, cards))
                    wrong = known - rankCount
                    freedomMut = freedom - (3-rankCount)
                    mutProb = 0
                    if freedomMut >= 0:
                        N = 52 - wrong - 3
                        k = freedomMut
                        mutProb = comb(4-rankCount,1)*(comb(N, k)/comb(52-known, freedom))
                rankProb -= mutProb
                cumProb += rankProb
        return cumProb

    def two_pair(self, game:Game, cards, inDeck, left):
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
                    pairProb = 1
            mutProb = 0
            for rank in game.RANKS:
                if rank not in pair and rank < min(pair):
                    rankCount = len(filter_by_rank(rank, cards))
                    wrong = known - rankCount
                    freedomMut = freedom - (2-rankCount)
                    if freedomMut >= 0:
                        N = 52 - wrong - 2
                        k = freedomMut
                        rankProb = comb(4-rankCount, 2) * (comb(N, k)/comb(52-known, freedom)) #4C2 ways to make this particular pair (since we ignored suit)
                        mutProb += rankProb
            pairProb -= mutProb
            cumProb += pairProb
        return cumProb

    def pair(self, game:Game, cards, inDeck, left):
        known = len(cards)
        cumProb = 0
        for rank in game.RANKS:
            rankCount = len(filter_by_rank(rank, cards))
            wrong = known - rankCount
            freedom = left - (2-rankCount)
            if freedom >= 0:
                N = 52 - wrong - 2
                k = freedom
                rankProb = comb(4-rankCount, 2) * (comb(N, k)/comb(52-known, left)) #4C2 ways to make this particular pair (since we ignored suit)
                cumProb += rankProb
        return cumProb

    def select_five_cards(self):
        raise NotImplementedError()

if __name__ == '__main__':
    g = Game(0)
    g.stage = 'P'
    p = AI(0)
    p.calc_self_probs(g)
