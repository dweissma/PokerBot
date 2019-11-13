"""
File for basic player class
"""

from Game import Game

class Player(Game):
    def __init__(self):
        self.hand = None #The player's hand
        self.money = None #How much money/chips the player has
        self.playing = True # if fold, turn it to false
        raise NotImplementedError()

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
        # to ensure a valid input
        while True:
            if action == 'r':
                # In case the player gives an invalid amount
                while True:
                    # should add some rules
                    # amount = int(input("How much do you want to raise? "))
                    if amount >= self.min:
                        self.money -= amount
                        self.pot += amount
                        break
            elif action == 'f':
                self.playing = False
                break
            elif action == 'c':
                print("Your hand: " + self.hand)
                break

        raise NotImplementedError() #Not sure who is working on this but plz add timer(15secs) with automatic fold if time out to match game class
        #We need scanner for terminal to read bet amount
        #The Call action should also reduce player money and add to pot




