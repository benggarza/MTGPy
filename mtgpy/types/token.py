from .permanent import Permanent
from ..utils import *
from .cardtype import CardType
from ..player import Player

# CR111.1. Some effects put tokens onto the battlefield.
# A token is a marker used to represent any permanent that isn’t represented by a card.
class Token(Permanent):
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
        
        # CR111.2. The player who creates a token is its owner.
        # The token enters the battlefield under that player’s control.
        if owner is None:
            raise ValueError("A token must have an owner")

        # CR111.3. The spell or ability that creates a token may define the values
        # of any number of characteristics for the token.
        # This becomes the token’s “text.” The characteristic values defined this way are functionally equivalent
        # to the characteristic values that are printed on a card; for example, they define the token’s copiable values.
        # A token doesn’t have any characteristics not defined by the spell or ability that created it.

        # CR111.4. A spell or ability that creates a token sets both its name and its subtype(s).
        # If the spell or ability doesn’t specify the name of the token,
        # its name is the same as its subtype(s) plus the word “Token.”
        # Once a token is on the battlefield,
        # changing its name doesn’t change its subtype(s), and vice versa.
        if subtype is None:
            raise ValueError("A token must have a subtype")
        _name = name
        if _name is None:
            _name = subtype + " Token."
        
        super().__init__(
            name = _name,
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
            owner = owner,
            controller = owner,
            tapped = tapped,
            flipped = flipped,
            face_up = face_up,
            phased_in = phased_in
        )

    # CR111.10. Some effects instruct a player to create a predefined token.
    # These effects use the definition below to determine the characteristics the token is created with.
    # The effect that creates a predefined token may also modify or add to the predefined characteristics.

    # CR111.10a A Treasure token is a colorless Treasure artifact token with
    # “{T}, Sacrifice this token: Add one mana of any color.”
    @classmethod
    def treasure():
        return Token(
            name = 'Treasure',
            color = None,
            card_type = CardType.ARTIFACT,
            subtype = 'Treasure', # TODO: replace this with the enumerated artifact treasure type
            rules_text = '{T}, Sacrifice this token: Add one mana of any color.',
            abilities = None # TODO: add the mana ability
        )
    
    # CR111.10b A Food token is a colorless Food artifact token with
    # “{2}, {T}, Sacrifice this token: You gain 3 life.”
    @classmethod
    def food():
        return Token(
            name = 'Food',
            color = None,
            card_type = CardType.ARTIFACT,
            subtype = 'Food', # TODO: replace this with the enumerated artifact food type
            rules_text = '{2}, {T}, Sacrifice this token: You gain 3 life.',
            abilities = None # TODO: add the food ability
        )
    
    # CR111.10c A Gold token is a colorless Gold artifact token with
    # “Sacrifice this token: Add one mana of any color.”
    @classmethod
    def gold():
        return Token(
            name = 'Gold',
            color = None,
            card_type = CardType.ARTIFACT,
            subtype = 'Gold', # TODO: replace this with the enumerated artifact gold type
            rules_text = 'Sacrifice this token: Add one mana of any color.',
            abilities = None # TODO: add the mana ability
        )
    
    # CR111.10d A Walker token is a 2/2 black Zombie creature token named Walker.
    @classmethod
    def walker():
        return Token(
            name = 'Walker',
            color = Color.BLACK,
            card_type = CardType.CREATURE,
            subtype = 'Zombie' # TODO: Replace with the enumerated type
        )

    # CR111.10e A Shard token is a colorless Shard enchantment token with
    # “{2}, Sacrifice this token: Scry 1, then draw a card.”
    @classmethod
    def shard():
        return Token(
            name = 'Shard',
            color = None,
            card_type = CardType.ENCHANTMENT,
            subtype = 'Shard', # TODO: enumerate
            rules_text = '{2}, Sacrifice this token: Scry 1, then draw a card.',
            abilities = None # TODO: add ability
        )
    
    # TODO: remaining predefined tokens in CR111.10

    # CR111.11. If an effect instructs a player to create a token by name,
    # doesn’t define any other characteristics for that token,
    # and the name is not one of the types in the list of predefined tokens above,
    # that player uses the card with that name in the Oracle card reference
    # to determine the characteristics of that token.
    @classmethod
    def by_name(card_name : str):
        # TODO: set up access to oracle card db to lookup card name and pull characteristics from that
        return Token(name = card_name)
    
