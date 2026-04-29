from .gameobject  import GameObject
from ..player import Player
from ..utils import Symbol, Color
from .cardtype import CardType

class Card(GameObject):
    _mana_value : int

    # CR200.1. The parts of a card are
    # name, mana cost, illustration, color indicator, type line,
    # expansion symbol, text box, power and toughness, loyalty,
    # defense, hand modifier, life modifier, illustration credit,
    # legal text, and collector number.
    # Some cards may have more than one of any or all of these parts.
    def __init__(self,
                 name : str = None,
                 mana_cost : list[Symbol] | None = None,
                 color_indicator : set[Color] = set(),
                 card_type : CardType = None,
                 subtype = None,
                 supertype = None,
                 rules_text : str | None = None,
                 power : int | None = None,
                 toughness : int | None = None,
                 loyalty : int | None = None,
                 defense : int | None = None,
                 hand_modifier : int | None = None,
                 life_modifier : int | None = None,
                 # non-characteristics
                 owner : Player = None):
        # CR108.3. The owner of a card in the game is the player who started the game with it in their deck.
        # If a card is brought into the game from outside the game rather than starting in a player’s deck,
        # its owner is the player who brought it into the game. If a card starts the game in the command zone,
        # its owner is the player who put it into the command zone to start the game. 

        # CR108.4. A card doesn’t have a controller unless that card represents a permanent or spell;
        # in those cases, its controller is determined by the rules for permanents or spells.
        # See rules 110.2 and 112.2.

        # CR108.4a If anything asks for the controller of a card that doesn’t have one
        # (because it’s not a permanent or spell), use its owner instead.
        _controller = owner

        super().__init__(
            name = name,
            mana_cost = mana_cost,
            color_indicator = color_indicator,
            card_type = card_type,
            subtype = subtype,
            supertype = supertype,
            rules_text = rules_text,
            power = power,
            toughness = toughness,
            loyalty = loyalty,
            defense = defense,
            hand_modifier = hand_modifier,
            life_modifier = life_modifier,
            owner = owner, 
            controller = owner
        )

        # CR202.3. The mana value of an object is a number equal to the total amount of mana in its mana cost, regardless of color.
        self.mana_value = 0
        if mana_cost is not None:
            for s in mana_cost:
                # CR202.3e When calculating the mana value of an object with an {X} in its mana cost,
                # X is treated as 0 while the object is not on the stack,
                # and X is treated as the number chosen for it while the object is on the stack.
                if s == Symbol.X:
                    continue
                # CR202.3f When calculating the mana value of an object with
                # a hybrid mana symbol in its mana cost,
                # use the largest component of each hybrid symbol.
                elif '2' in s: # TODO: improve the method for checking for hybrid mana costs
                    self.mana_value += 2
                else:
                    self.mana_value += 1

        # CR202.4. Any additional cost listed in an object’s rules text or imposed by an effect isn’t part of the mana cost.
        # (See rule 601, “Casting Spells.”) Such costs are paid at the same time as the spell’s other costs.

    @property
    def mana_value(self):
        return self._mana_value
    
    @mana_value.setter
    def mana_value(self, mv):
        if not isinstance(mv, int):
            raise ValueError("mana_value can only be an int")
        self._mana_value = mv