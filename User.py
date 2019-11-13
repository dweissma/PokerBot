"""
A class for users to play games of holdem
"""
import os

from Player import Player
import func_timeout


class User(Player):

    @func_timeout.func_set_timeout(15)
    def get_input(self):
        return input("It's your turn: ")

    def play(self):

        # get a valid action
        while True:
            try:
                # if we didnt get input within 15 seconds, fold
                try:
                    action = self.get_input()
                except func_timeout.exceptions.FunctionTimedOut:
                    action = 'f'

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


