"""
Runs a game of texas holdem
"""

class Game(object):
    STAGES = {
        'begin':'B',
        'flop':'F',
        'turn':'T',
        'river':'R',
    }    

    def __init__(self):
        self.players = []
        self.publicCards = []
        self.stage = Game.STAGES['begin']
        raise NotImplementedError()

    def play_hand(self):
        """
        Plays through a single hand of texas holdem
        using the current amounts of money each player has
        """
        raise NotImplementedError()

    def play_game(self):
        """
        Plays hands of texas holdem until either
        all players but 1 are bankrupt or the user
        want's the game to stop
        """
        raise NotImplementedError()
        
    
    