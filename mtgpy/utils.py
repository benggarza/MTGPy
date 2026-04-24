from enum import Enum
import random


# CR106.1. Mana is the primary resource in the game.
# Players spend mana to pay costs,
# usually when casting spells and activating abilities.

# CR106.1a There are five colors of mana: white, blue, black, red, and green.
class ManaColor(Enum):
    W = 'W'
    U = 'U'
    B = 'B'
    R = 'R'
    G = 'G'

# CR106.1b There are six types of mana: white, blue, black, red, green, and colorless.
class ManaType(Enum):
    W = 'W'
    U = 'U'
    B = 'B'
    R = 'R'
    G = 'G'
    C = 'C'

# CR106.2. Mana is represented by mana symbols (see rule 107.4).
# Mana symbols also represent mana costs (see rule 202).

# CR107.4a There are five primary colored mana symbols:
# {W} is white, {U} blue, {B} black, {R} red, and {G} green.
# These symbols are used to represent colored mana,
# and also to represent colored mana in costs.
# Colored mana in costs can be paid only with the appropriate color of mana.
# See rule 202, “Mana Cost and Color.”
class ManaSymbol(Enum):
    W = 'W'
    U = 'U'
    B = 'B'
    R = 'R'
    G = 'G'
    C = 'C'

# CR107.4. The mana symbols are {W}, {U}, {B}, {R}, {G}, and {C};
# the numerical symbols {0}, {1}, {2}, {3}, {4}, and so on;
# the variable symbol {X};
# the hybrid symbols {W/U}, {W/B}, {U/B}, {U/R}, {B/R}, {B/G}, {R/G}, {R/W}, {G/W}, and {G/U};
# the monocolored hybrid symbols {2/W}, {2/U}, {2/B}, {2/R}, {2/G}, {C/W}, {C/U}, {C/B}, {C/R}, and {C/G};
# the Phyrexian mana symbols {W/P}, {U/P}, {B/P}, {R/P}, and {G/P};
# the hybrid Phyrexian symbols {W/U/P}, {W/B/P}, {U/B/P}, {U/R/P}, {B/R/P}, {B/G/P}, {R/G/P}, {R/W/P},
# {G/W/P}, and {G/U/P};
# and the snow mana symbol {S}.
class Symbol(Enum):
    W = ManaSymbol.W
    U = ManaSymbol.U
    B = ManaSymbol.B
    R = ManaSymbol.R
    G = ManaSymbol.G
    # variable symbol
    X = 'X'

    # hybrid symbols
    # TODO: string representation or tuple representation?
    WU = 'W/U'
    WB = (ManaSymbol.W, ManaSymbol.B)
    UB = 'U/B'
    UR = 'U/R'
    BR = 'B/R'
    BG = 'B/G'
    RG = 'R/G'
    RW = 'R/W'
    GW = 'G/W'
    GU = 'G/U'
    
    # TODO remaining hybrid/phrexian symbols

    # snow mana symbol
    S = 'S'

# CR105.1. There are five colors in the Magic game: white, blue, black, red, and green.
class Color(Enum):
    WHITE = 'White'
    BLUE = 'Blue'
    BLACK = 'Black'
    RED = 'Red'
    GREEN = 'Green'


# CR100.3 Some cards require coins or traditional dice.
# Some casual variants require additional items,
# such as specially designated cards, nontraditional Magic cards, and specialized dice.
def flip_coin() -> int:
    """Flips a single coin, and returns 1 for heads and 2 for tails"""
    return int(random.random()*2)

def flip_coins(num : int) -> set[int]:
    """Flips multiple coins and returns the set of results"""
    return set([flip_coin() for _ in range(num)])

def roll_die(sides : int) -> int:
    """Rolls a single die and returns the result"""
    return int(1 + random.random()*sides)

def roll_dice(num : int, sides : int) -> set[int]:
    """Rolls multiple dice of the same shape and returns the results"""
    return set([roll_die(sides) for _ in range(num)])