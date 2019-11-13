"""
A class for users to play games of holdem
"""
import os

from Player import Player

class User(Player):

    def play(self):
        # get a valid action
        while True:
            try:
                action = input("It's your turn: ")
                if action in ['r', 'c', 'f', 'q']:
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Invalid input! Try again.")

        if action == 'r':
            rasieAmount = int(input("How much do you want to raise? "))
            # get a valid raise
            while True:
                try:
                    if self.money >= rasieAmount >= self.min:
                        self.bet('r', rasieAmount)
                    else:
                        raise ValueError
                except ValueError:
                    print("Invalid input! Try again.")
        elif action == 'c':
            print("Your hand: ", self.hand)
            self.bet('c', -1)
        elif action == 'f':
            self.bet('f', -1)
        else:
            # if we get a 'q', quit the game
            print("Player quit the game!")
            os.quit()

    raise NotImplementedError()


