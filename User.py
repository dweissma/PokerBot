"""
A class for users to play games of holdem
"""
import os

from Player import Player
import func_timeout


class User(Player):

    @func_timeout.func_set_timeout(1000)
    def get_input(self):
        return input("It's your turn: ")

    def bet(self, game):
        # get a valid action
        print(f"It is {game.playerCodes[self.id]}'s turn")
        print(f"The pot is {game.pot}")
        print(f"You currently have {self.money} dollars")
        plist = [p.id for p in game.players]
        selfI = plist.index(self.id)
        betI = game.bets[selfI]
        w = max(game.bets)
        print(f"Calling will cost {w-betI}")
        print(f"The min raise is {game.min}")
        print("Your hand is")
        self.cardPrinter(self.hand)
        print("The current board is")
        self.cardPrinter(game.board)
        print("Press f to fold, c to call, r to raise")
        while True:
                # if we didnt get input within 90 seconds, fold
            try:
                try:
                    action = self.get_input()
                except func_timeout.exceptions.FunctionTimedOut:
                    action = 'f'

                if action in ['r', 'c', 'f', 'q']:
                    break
                else:
                    raise ValueError
            except ValueError:
                action = input("Invalid input! Try again.")

        if action == 'r':
            # get a valid raise
            while True:
                rasieAmount = int(input("How much do you want to raise? "))
                try:
                    if self.money >= rasieAmount >= game.min:
                        return ('r', rasieAmount)
                    else:
                        raise ValueError
                except ValueError:
                    print("Invalid input! Try again.")
        elif action == 'c':
            print("Your hand: ", self.hand)
            return ('c', -1)
        elif action == 'f':
            return ('f', -1)
        else:
            # if we get a 'q', quit the game
            print("Player quit the game!")
            os.quit()

