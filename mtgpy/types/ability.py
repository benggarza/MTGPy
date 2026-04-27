from .gameobject import GameObject

# CR113.1. An ability can be one of three things:

# 113.1a An ability can be a characteristic an object has that lets it affect the game.
# An object’s abilities are defined by its rules text or by the effect that created it.
# Abilities can also be granted to objects by rules or effects.
# (Effects that grant abilities usually use the words “has,” “have,” “gains,” or “gain.”)
# Abilities generate effects. (See rule 609, “Effects.”)

# 113.1b An ability can be something that a player has that changes how the game affects the player.
# A player normally has no abilities unless granted to that player by effects.

# 113.1c An ability can be an activated or triggered ability on the stack.
# This kind of ability is an object. (See section 6, “Spells, Abilities, and Effects.”)
class Ability(GameObject):
    pass