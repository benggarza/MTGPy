from enum import Enum
class Mana(Enum):
    W = 'W'
    U = 'U'
    B = 'B'
    R = 'R'
    G = 'G'
    # Colorless
    C = 'C'
    # TODO: how to designate mana as snow mana

class CostMana(Enum):
    W = Mana.W
    U = Mana.U
    B = Mana.B
    R = Mana.R
    G = Mana.G
    C = Mana.C
    # Generic Snow
    S = 'S'
    # TODO: how to designate generic mana costs, phyrexian mana costs
