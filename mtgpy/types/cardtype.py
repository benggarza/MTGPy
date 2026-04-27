from utils import *
from ..player import Player
from enum import Enum

class CardType(Enum):
    INSTANT = "Instant"
    SORCERY = "Sorcery"
    CREATURE = "Creature"
    LAND = "Land"
    PLANESWALKER = "Planeswalker"
    BATTLE = "Battle"
    ENCHANTMENT = "Enchantment"
    ARTIFACT = "Artifact"
    KINDRED = "Kindred"

# CR110.4. There are six permanent types:
# artifact, battle, creature, enchantment, land, and planeswalker.
# Instant and sorcery cards can’t enter the battlefield and thus can’t be permanents.
# Some kindred cards can enter the battlefield and some can’t,
# depending on their other card types. See section 3, “Card Types.”
class PermanentType(Enum):
    CREATURE = CardType.CREATURE
    LAND = CardType.LAND
    PLANESWALKER = CardType.PLANESWALKER
    BATTLE = CardType.BATTLE
    ENCHANTMENT = CardType.ENCHANTMENT
    ARTIFACT = CardType.ARTIFACT