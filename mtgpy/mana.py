from .utils import ManaType
from .types import GameObject
# CR106.3. Mana is produced by the effects of mana abilities (see rule 605).
# It may also be produced by the effects of spells,
# as well as by the effects of abilities that aren’t mana abilities.
# A spell or ability that produces mana instructs a player to add that mana.
# If mana is produced by a spell, the source of that mana is that spell.
# If mana is produced by an ability, the source of that mana is the source of that ability (see rule 113.7).
class Mana:
    def __init__(self, manaType : ManaType, source : GameObject):
        self.manaType = manaType
        # TODO: assert that source is either a spell or a permanent (with the mana-producing ability)
        self.source = source