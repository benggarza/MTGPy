from .cardtype import *
from ..player import Player
from ..card import Card
from .gameobject import GameObject
from .ability import Ability
from __future__ import annotations

# CR110.1. A permanent is a card or token on the battlefield.
# A permanent remains on the battlefield indefinitely.
# A card or token becomes a permanent as it enters the battlefield
# and it stops being a permanent as it’s moved to another zone by an effect or rule.
class Permanent(GameObject):
    # CR110.5. A permanent’s status is its physical state.
    # There are four status categories,
    # each of which has two possible values:
    # tapped/untapped, flipped/unflipped, face up/face down, and phased in/phased out.
    # Each permanent always has one of these values for each of these categories.
    _tapped : bool
    _flipped : bool
    _face_up : bool
    _phased_in : bool

    # CR110.2. A permanent’s owner is the same as the owner of the card that represents it
    # (unless it’s a token; see rule 111.2).
    # A permanent’s controller is, by default,
    # the player under whose control it entered the battlefield.
    # Every permanent has a controller.
    def __init__(self,
                 name : str | None = None,
                 mana_cost : list[Symbol] | None = None,
                 color : set[Color] | None = None,
                 color_indicator : set[Color] | None = None,
                 card_type : CardType | None = None,
                 subtype = None,
                 supertype = None,
                 rules_text : str | None = None,
                 abilities : set[Ability] | None = None,
                 power : int | None = None,
                 toughness : int | None = None,
                 loyalty : int | None = None,
                 defense : int | None = None,
                 hand_modifier : int | None = None,
                 life_modifier : int | None = None,
                 owner : Player | None = None,
                 controller : Player = None,
                 tapped : bool = False,
                 flipped : bool = False,
                 face_up : bool = True,
                 phased_in : bool = True
                 ):
        if controller is None:
            raise ValueError("A permanent must have a controller")
        if owner is None:
            _owner = controller
        else:
            _owner = owner

        self.tapped = tapped
        self.flipped = flipped
        self.face_up = face_up
        self.phased_in = phased_in

        super().__init__(
            name = name,
            mana_cost = mana_cost,
            color = color,
            color_indicator = color_indicator,
            card_type = card_type,
            subtype = subtype,
            supertype = supertype,
            rules_text = rules_text,
            abilities = abilities,
            power = power,
            toughness = toughness,
            loyalty = loyalty,
            defense = defense,
            hand_modifier = hand_modifier,
            life_modifier = life_modifier,
            owner = _owner,
            controller = controller
        )

    @GameObject.controller.setter
    def controller(self, c):
        if not isinstance(c, Player):
            raise ValueError("controller must be a Player")
        
        self._controller = c

    @property
    def tapped(self):
        return self._tapped
    
    @tapped.setter
    def tapped(self, t : bool):
        if not isinstance(t, bool):
            raise ValueError("tapped must be a boolean")
        self._tapped = t

    @property
    def flipped(self):
        return self._flipped
    
    @flipped.setter
    def flipped(self, f : bool):
        if not isinstance(f, bool):
            raise ValueError("flipped must be a boolean")
        self._flipped = f

    @property
    def face_up(self):
        return self._face_up
    
    @face_up.setter
    def face_up(self, f : bool):
        if not isinstance(f, bool):
            raise ValueError("face_up must be a boolean")
        self._face_up = f

    @property
    def phased_in(self):
        return self._phased_in
    
    @phased_in.setter
    def phased_in(self, p : bool):
        if not isinstance(p, bool):
            raise ValueError("phased_in must be a boolean")
        self._phased_in = p

    @classmethod
    def from_card(c : Card) -> Permanent:
        if not isinstance(c, Card):
            raise ValueError("card must be a Card")
        if c.card_type == 'Instant' or c.card_type == 'Sorcery':
            raise ValueError("An instant or sorcery card cannot become a permanent")
        # CR110.3. A nontoken permanent’s characteristics are the same as those printed on its card,
        # as modified by any continuous effects.
        # See rule 613, “Interaction of Continuous Effects.”
        p = Permanent(
            name = c.name,
            mana_cost = c.mana_cost,
            color = c.color,
            color_indicator = c.color_indicator,
            card_type = c.card_type,
            subtype = c.subtype,
            supertype = c.supertype,
            rules_text = c.rules_text,
            abilities = c.abilities,
            power = c.power,
            toughness = c.toughness,
            loyalty = c.loyalty,
            defense = c.defense,
            hand_modifier = c.hand_modifier,
            life_modifier = c.life_modifier,
            owner = c.owner,
            controller = c.owner
            )
        # TODO: apply continuous effects
        return p
