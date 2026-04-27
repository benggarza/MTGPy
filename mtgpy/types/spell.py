from .gameobject import GameObject
from .cardtype import *
from .ability import Ability
from ..card import Card

# CR112.1. A spell is a card on the stack.
# As the first step of being cast (see rule 601, “Casting Spells”),
# the card becomes a spell and is moved to the top of the stack from the zone it was in,
# which is usually its owner’s hand. (See rule 405, “Stack.”)
# A spell remains on the stack as a spell until it resolves
# (see rule 608, “Resolving Spells and Abilities”), is countered (see rule 701.6),
# or otherwise leaves the stack.
# For more information, see section 6, “Spells, Abilities, and Effects.”
class Spell(GameObject):
    # CR112.2. A spell’s owner is the same as the owner of the card that represents it,
    # unless it’s a copy. In that case,
    # the owner of the spell is the player under whose control it was put on the stack.
    # A spell’s controller is, by default,
    # the player who put it on the stack.
    # Every spell has a controller.
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
                 card : Card | None = None
                 ):
        if controller is None:
            raise ValueError("A spell must have a controller")
        _owner = owner
        if _owner is None:
            if card is not None:
                _owner = card.owner
            else:
                _owner = controller
        # CR112.3. A noncopy spell’s characteristics are the same as those printed on its card,
        # as modified by any continuous effects. See rule 613, “Interaction of Continuous Effects.”
        if name is None:
            _name = card.name
        if mana_cost is None:
            _mana_cost = card.mana_cost
        # TODO: make it so that a card's copiable characteristics are easily exported as a tuple
        # so I don't have to write if statements for every characteristic
                

    # CR112.1a A copy of a spell is also a spell, even if it has no card associated with it. See rule 707.10.
    def copy(self):
        return Spell(
            name = self.name,
            mana_cost = self.mana_cost,
            color = self.color,
            color_indicator = self.color_indicator,
            card_type = self.card_type,
            subtype = self.subtype,
            supertype = self.supertype,
            rules_text = self.rules_text,
            abilities = self.abilities,
            power = self.power,
            toughness = self.toughness,
            loyalty = self.loyalty,
            defense = self.defense,
            hand_modifier = self.hand_modifier,
            life_modifier = self.life_modifier,
            owner = self.owner,
            controller = self.controller
        )