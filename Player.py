"""
File for basic player class
"""


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
        print()

    """
    The following methods are used to decide which rank are the 5 selected cards in
    royal flush to highcard are defined as 1-10 
    """
    def in_which_rank(self, cards):
        """
        Decide which rank are the 5 selected cards in
        :param cards: 5 cards
        :return: a tuple, (rank, a list of the numerical values of cards in non-decreasing order)
        """
        ranks = [self.is_royal_flush, self.is_straight_flush, self.is_four_of_a_kind, self.is_full_house,
                 self.is_flush, self.is_straight, self.is_three_of_a_kind, self.is_two_pairs,
                 self.is_pair, self.is_highcard]

        result = (-1,None)
        while result[0] == -1:
            result = ranks.pop(0)(cards)

        return result


    def is_royal_flush(self, cards):
        """
        if is a royal flush, return (1, a list containing the numerical values of each card) else return (-1, None)
        """
        numbers = [x[0] for x in cards]
        suits = [x[1] for x in cards]
        # 10-A
        if ('10' in numbers) and ('J' in numbers) and ('Q' in numbers) and ('K' in numbers) and ('A' in numbers):
            # have the same suit
            if suits[0] == suits[1] == suits[2] == suits[3] == suits[4]:
                return (1, (10, 11, 12, 13, 14))
        return (-1, None)


    def is_straight_flush(self, cards):
        # if have the same suit
        if cards[0][1] == cards[1][1] == cards[2][1] == cards[3][1] == cards[4][1]:
            num = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
            numbers = [num[x[0]] for x in cards]
            numbers.sort()
            # since we only have one deck, and these 5 cards are in the same suit
            # which means the value of each card are distinct
            # numbers has been sorted, so if last - first === 4, then it's a straight
            if numbers[4] - numbers[0] == 4:
                return (2, tuple(numbers))

        return (-1, None)



    def is_four_of_a_kind(self, cards):

        num = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        numbers = [num[x[0]] for x in cards]
        numbers.sort()

        # two cases: first four or last four
        if (numbers[0] == numbers[1] == numbers[2] == numbers[3]) or (numbers[1] == numbers[2] == numbers[3] == numbers[4]):
            return (3, tuple(numbers))

        return (-1, None)



    def is_full_house(self, cards):
        num = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        numbers = [num[x[0]] for x in cards]
        numbers.sort()

        # two cases: first 3 and last 3
        if ((numbers[0] == numbers[1] == numbers[2]) and (numbers[3] == numbers[4])) or ((numbers[0] == numbers[1]) and (numbers[2] == numbers[3] == numbers[4])):
            return (4, tuple(numbers))
        return (-1, None)


    def is_flush(self, cards):
        num = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13,
               'A': 14}
        numbers = [num[x[0]] for x in cards]
        numbers.sort()
        if cards[0][1] == cards[1][1] == cards[2][1] == cards[3][1] == cards[4][1]:
            return (5, tuple(numbers))

        return (-1, None)


    def is_straight(self, cards):
        num = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13,
               'A': 14}
        numbers = [num[x[0]] for x in cards]
        numbers.sort()
        if numbers[1]-numbers[0] == 1 and numbers[2]-numbers[1] == 1 and numbers[3]-numbers[2] == 1 and numbers[4]-numbers[3] == 1:
            return (6, tuple(numbers))
        return (-1, None)

    def is_three_of_a_kind(self, cards):
        num = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13,
               'A': 14}
        numbers = [num[x[0]] for x in cards]
        numbers.sort()

        # three cases: 1-3, 2-4, or 3-5
        if (numbers[0] == numbers[1] == numbers[2]) or (numbers[1] == numbers[2] == numbers[3]) or (numbers[2] == numbers[3] == numbers[4]):
            return (7, tuple(numbers))

        return (-1, None)

    def is_two_pairs(self, cards):
        num = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13,
               'A': 14}
        numbers = [num[x[0]] for x in cards]
        numbers.sort()

        # three cases: 12 and 34, or 23 and 45, or 12 and 45
        if ((numbers[0] == numbers[1]) and (numbers[2] == numbers[3])) or ((numbers[1] == numbers[2]) and (numbers[3] == numbers[4])) or ((numbers[0] == numbers[1]) and (numbers[3] == numbers[4])):
            return (8, tuple(numbers))

        return (-1, None)

    def is_pair(self, cards):
        num = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13,
               'A': 14}
        numbers = [num[x[0]] for x in cards]
        numbers.sort()

        # four cases: 12, 23, 34, or 45
        if (numbers[0] == numbers[1]) or (numbers[1] == numbers[2]) or (numbers[2] == numbers[3]) or (numbers[3] == numbers[4]):
            return (9, tuple(numbers))

        return (-1, None)

    def is_highcard(self, cards):
        num = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13,
               'A': 14}
        numbers = [num[x[0]] for x in cards]
        numbers.sort()
        # anything else is a highcard
        return (10, tuple(numbers))
