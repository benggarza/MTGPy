class CardType:
    pass

class Creature(CardType):
    pass

class Planeswalker(CardType):
    pass

class Battle(CardType):
    pass

class Artifact(CardType):
    pass

class Enchantment(CardType):
    pass

class Land(CardType):
    pass

class Kindred(CardType):
    pass


class SuperType:
    pass

class Legendary(SuperType):
    pass

class Permanent:
    player_owner = None
    player_controller = None