from .types import GameObject
from .player import Player
class Card(GameObject):
    def __init__(self, owner : Player = None):
        # CR108.3. The owner of a card in the game is the player who started the game with it in their deck.
        # If a card is brought into the game from outside the game rather than starting in a player’s deck,
        # its owner is the player who brought it into the game. If a card starts the game in the command zone,
        # its owner is the player who put it into the command zone to start the game. 
        self.owner = owner

        # CR108.4. A card doesn’t have a controller unless that card represents a permanent or spell;
        # in those cases, its controller is determined by the rules for permanents or spells.
        # See rules 110.2 and 112.2.

        # CR108.4a If anything asks for the controller of a card that doesn’t have one
        # (because it’s not a permanent or spell), use its owner instead.
        self.controller = owner