from .card import Card
from .mana import Mana
from .game import Game
from .types import *

from random import shuffle
from typing import Callable
from __future__ import annotations

class Player:
    """An in-game instance of a Player.
    """
    
    _life : int
    
    def __init__(
            self,
            game : Game,
            starting_life : int,
            library : list[Card],
            sideboard : list[Card]
        ):
        self.life = starting_life

        self.library : list[Card] = library
        self.sideboard : list[Card] = sideboard
        self.hand = set()
        self.graveyard : list[Card] = []

        self.companion_zone : Card = None


        self.opponents : list[Player] = []
        self.mana_pool = {
            Mana.W: 0,
            Mana.U: 0,
            Mana.B: 0,
            Mana.R: 0,
            Mana.G: 0,
            Mana.C: 0
        }

        # Replaceable functions
        self.draw = self._draw
        self.mulligan : Callable = self._mulligan
        self.empty_mana_pool : Callable = self._empty_mana_pool
        self.untap_permanents = self._untap_permanents

        # Properties
        self.cards_drawn_this_turn = 0
        

    @property
    def life(self):
        return self._life
    
    @life.setter
    def life(self, l : int):
        if not isinstance(l, int):
            raise ValueError("Life totals can only be integers.")
        self._life = l
    
    def priority(self):
        """Function called when priority is passed to the player.
        Player may activate abilities, cast spells, ..., or pass priority

        Returns: a game action, or None if player passes priority
        """
        return None
    
    def declare_companion(self) -> Card | None:
        """The player gets the opportunity to declare a companion
        and place them in the companion zone outside of the game."""
        return None

    def shuffle_deck(
            self,
            hand : bool = False,
            graveyard : bool = False
        ) -> None:
        if hand:
            while len(self.hand) > 0:
                self.library.append(self.hand.pop())
        if graveyard:
            while len(self.graveyard) > 0:
                self.library.append(self.graveyard.pop())
        shuffle(self.library)

    def draw(self, num_draw : int):
        pass

    def _draw(self, num_draw : int):
        # TODO: how to announce to game that this player drew cards?
        # add effects to a queue to be checked during game state action checks?
        # TODO: how to allow replacement effects like dredge here?
        # have cards overload functions?
        # (e.g. a dredge creature has a draw() function that replaces this one,
        # but refers back to this one if the player opts to not dredge)
        for _ in range(num_draw):
            self.hand.add(self.library.pop(0))
            self.game.add_effect_to_queue({"draw", })

    def mulligan(self, hand_size : int):
        pass

    # TODO: serum powder should override this CR103.5b
    def _mulligan(self, hand_size : int) -> bool:
        """Player decides whether to keep their hand or mulligan"""
        # TODO: Human/Comp players should override this
        if hand_size == 7:
            return True
        else:
            return False
        
    # TODO: cards like Ashling, Horizon Stone should override this
    def _empty_mana_pool(self) -> None:
        """Resets mana pool"""
        self.mana_pool = {
            Mana.W: 0,
            Mana.U: 0,
            Mana.B: 0,
            Mana.R: 0,
            Mana.G: 0,
            Mana.C: 0
        }

    # TODO: cards like Stasis, Winter Moon, should override this
    def _untap_permanents(self) -> None:
        """Untap all permanents as part of the untap step"""
        # TODO: iterate over all controlled permanents and untap them
        pass

    def _declare_attackers(self) -> list[tuple[Creature, Player | Planeswalker | Battle]]:
        """Choose attacking creatures and the player"""
        # TODO: CR
        return []