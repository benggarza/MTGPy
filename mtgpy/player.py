from .card import Card
from random import shuffle

class Player:
    """An in-game instance of a Player.
    """
    
    pass
    def __init__(self, starting_life : int, library : list[Card], sideboard : list[Card]):
        self.life = starting_life
        self.library : list[Card] = library
        self.sideboard : list[Card] = sideboard
        self.hand = set()
        self.graveyard : list[Card] = []
        self.opponents : list[Player] = []
        

    @property
    def life(self):
        return self._life
    
    @life.setter
    def life(self, l : int):
        if not isinstance(l, int):
            raise ValueError("Life totals can only be integers.")
        self._life = l
    
    def choose_game_action(self) -> None:
        """Function called when priority is passed to the player.
        Player may activate abilities, cast spells, ..., or pass priority
        """
        pass

    def shuffle_deck(self, hand : bool = False, graveyard : bool = False) -> None:
        if hand:
            while len(self.hand) > 0:
                self.library.append(self.hand.pop())
        if graveyard:
            while len(self.graveyard) > 0:
                self.library.append(self.graveyard.pop())
        shuffle(self.library)

    def draw(self, num_draw : int):
        # TODO: how to announce to game that this player drew cards?
        # add effects to some queue to be checked during game state action checks?
        # TODO: how to allow replacement effects like dredge here?
        # have cards overload functions? (e.g. a dredge creature has a draw() function that replaces this one,
        # but refers back to this one if the player opts to not dredge)
        for _ in range(num_draw):
            self.hand.add(self.library.pop(0))
            self.game.add_effect_to_queue({"draw", })

    # TODO: serum powder should override this
    def mulligan(self, hand_size : int) -> bool:
        """Player decides whether to keep the cards they have in their hand or mulligan"""
        # TODO: Human/Comp players should override this
        if hand_size == 7:
            return True
        else:
            return False