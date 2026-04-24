from .types import *
from .player import Player

# CR109.1. An object is an ability on the stack, a card, a copy of a card, a token, a spell, a permanent, or an emblem.
class GameObject:
    # CR109.3. An object’s characteristics are
    # name, mana cost, color, color indicator, card type,
    # subtype, supertype, rules text, abilities, power,
    # toughness, loyalty, defense, hand modifier, and life modifier.
    # Objects can have some or all of these characteristics.
    # Any other information about an object isn’t a characteristic.
    # For example, characteristics don’t include whether
    # a permanent is tapped, a spell’s target, an object’s owner or controller, what an Aura enchants, and so on.
    def __init__(self,
                 name : str | None = None,
                 manaCost : list[Symbol] | None = None,
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
                 controller : Player | None = None
                 ):
        self.name = name
        self.manaCost = manaCost
        self.color = color
        self.color_indicator = color_indicator
        self.card_type = card_type
        self.subtype = subtype
        self.supertype = supertype
        self.rules_text = rules_text
        self.abilities = abilities
        self.power = power
        self.toughness = toughness
        self.loyalty = loyalty
        self.defense = defense
        self.hand_modifier = hand_modifier
        self.life_modifier = life_modifier

        # CR109.4. Only objects on the stack or on the battlefield have a controller.
        # Objects that are neither on the stack nor on the battlefield aren’t controlled by any player.
        # See rule 108.4. 
        self.controller = controller

# CR110.1. A permanent is a card or token on the battlefield.
# A permanent remains on the battlefield indefinitely.
# A card or token becomes a permanent as it enters the battlefield
# and it stops being a permanent as it’s moved to another zone by an effect or rule.
class Permanent(GameObject):
    pass