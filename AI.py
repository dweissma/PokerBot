"""
Our AI which plays Texas Holdem
"""

from Player import Player

class AI(Player):
    def play(self):
        # the ai always raise a minimum
        self.bet('r', self.min)

    raise NotImplementedError()