from .gameobject import GameObject
from .ability import Ability
from ..player import Player

# CR114.1. Some effects put emblems into the command zone.
# An emblem is a marker used to represent an object that has one or more abilities,
# but usually no other characteristics.
class Emblem(GameObject):
    # CR114.2. An effect that creates an emblem is written “[Player] gets an emblem with [ability].”
    # This means that [player] puts an emblem with [ability] into the command zone.
    # The emblem is both owned and controlled by that player.

    # CR114.3. An emblem has no characteristics other than the abilities defined by the effect that created it.
    # In particular, an emblem has no types, no mana cost, and no color.
    # Most emblems also have no name.
    def __init__(self,
                 name : str | None = None,
                 rules_text : str | None = None,
                 abilities : set[Ability] | None = None,
                 # non-characteristics
                 owner : Player | None = None,
                 controller : Player | None = None # TODO: owner and controller should be the same
                 ):
        super().__init__(
            name = name,
            rules_text = rules_text,
            abilities = abilities,
            owner = owner,
            controller = controller
        )

        # CR114.4. Abilities of emblems function in the command zone.

        # CR114.5. An emblem is neither a card nor a permanent. Emblem isn’t a card type.
