from .player import Player

class Game:
    """Game object
    
    """
    
    def __init__(self, players : list[Player]):
        """Constructor
        
        Keyword arguments:
        players -- each player participating in game
        """
        
        # TODO: assert that all Players are valid objects
        self.num_players = len(players)

    def play(self):
        """Main gameplay loop: iteratively checks game state and passes priority to next player until a winner is determined"""
        pass   
