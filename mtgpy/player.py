from .card import Card

class Player:
    """An in-game instance of a Player.
    """
    
    pass
    def __init__(self, starting_life : int, library : list[Card], sideboard : list[Card]):
        self.life = starting_life
        self.library = library
        self.sideboard = sideboard
        pass
    
    def choose_game_action(self) -> None:
        """Function called when priority is passed to the player.
        Player may activate abilities, cast spells, ..., or pass priority
        """
        pass