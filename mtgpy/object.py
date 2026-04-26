from .types import *
from .player import Player
from .card import Card
from __future__ import annotations

# CR109.1. An object is an ability on the stack, a card, a copy of a card, a token, a spell, a permanent, or an emblem.
class GameObject:

    _name : str | None
    _mana_cost : list[Symbol] | None
    _color : set[Color] | None
    _color_indicator : set[Color] | None
    _card_type : CardType | None
    _subtype : object | None
    _supertype : object | None
    _rules_text : str | None
    _abilities : set[Ability] | None
    _power : int | None
    _toughness : int | None
    _loyalty : int | None
    _defense : int | None
    _hand_modifier : int | None
    _life_modifier : int | None
    _owner : Player | None
    _controller : Player | None

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
                 controller : Player | None = None
                 ):
        self.name = name
        self.mana_cost = mana_cost
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
        self.owner = owner

        # CR109.4. Only objects on the stack or on the battlefield have a controller.
        # Objects that are neither on the stack nor on the battlefield aren’t controlled by any player.
        # See rule 108.4. 
        self.controller = controller

    @property
    def name(self):
        return self._name 
    
    @name.setter
    def name(self, n : str):
        if not isinstance(n, str) and n is not None:
            raise ValueError("name must be a string")
        self._name = n

    @property
    def mana_cost(self):
        return self._mana_cost
    
    @mana_cost.setter
    def mana_cost(self, mc : list[Symbol]):
        if not isinstance(mc, list) and mc is not None:
            raise ValueError("mana cost must be a list")
        for m in mc:
            if not isinstance(m, Symbol):
                raise ValueError("All mana symbols must be Symbols")
            
        self._mana_cost = mc

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, c):
        if not isinstance(c, set) and c is not None:
            raise ValueError("color must be a set of Color enums")
        for _c in list(c):
            if not isinstance(_c, Color):
                raise ValueError("All colors must be Color enums")

        self._color = c


    @property
    def color_indicator(self):
        return self._color_indicator
    
    @color_indicator.setter
    def color_indicator(self, ci):
        if not isinstance(ci, set) and ci is not None:
            raise ValueError("color must be a set of Color enums")
        for _c in list(ci):
            if not isinstance(_c, Color):
                raise ValueError("All colors must be Color enums")

        self._color_indicator = ci
    
    @property
    def card_type(self):
        return self._card_type
    
    @card_type.setter
    def card_type(self, ct):
        if not isinstance(ct, CardType) and ct is not None:
            raise ValueError("card_type must be a CardType")
        
        self._card_type = ct

    @property
    def subtype(self):
        return self._subtype
    
    @subtype.setter
    def subtype(self, st):
        if not isinstance(st, object) and st is not None:
            raise ValueError("subtype must be a ___")
        
        self._subtype = st

    @property
    def supertype(self):
        return self._supertype
    
    @supertype.setter
    def supertype(self, st):
        if not isinstance(st, object) and st is not None:
            raise ValueError("supertype must be a __")

        self._supertype = st

    @property
    def rules_text(self):
        return self._rules_text
    
    @rules_text.setter
    def rules_text(self, rt):
        if not isinstance(rt, str) and rt is not None:
            raise ValueError("rules_text must be a string")
        
        self._rules_text = rt

    @property
    def abilities(self):
        return self._abilities
    
    @abilities.setter
    def abilities(self, a):
        if not isinstance(a, set) and a is not None:
            raise ValueError("abilties must be a set of Ability objects")
        
        self._abilities = a

    @property
    def power(self):
        return self._power
    
    @power.setter
    def power(self, p):
        if not isinstance(p, int) and p is not None:
            raise ValueError("power must be an int")
        
        self._power = p

    @property
    def toughness(self):
        return self._power
    
    @toughness.setter
    def toughness(self, t):
        if not isinstance(t, int) and t is not None:
            raise ValueError("toughness must be an int")
        
        self._toughness = t

    @property
    def loyalty(self):
        return self._loyalty
    
    @loyalty.setter
    def loyalty(self, l):
        if not isinstance(l, int) and l is not None:
            raise ValueError("loyalty must be an int")
        
        self._loyalty = l

    @property
    def defense(self):
        return self._defense
    
    @defense.setter
    def defense(self, d):
        if not isinstance(d, int) and d is not None:
            raise ValueError("defense must be an int")
        
        self._defense = d

    @property
    def hand_modifier(self):
        return self._hand_modifier
    
    @hand_modifier.setter
    def hand_modifier(self, hm):
        if not isinstance(hm, int) and hm is not None:
            raise ValueError("hand_modifier must be an int")
        
        self._hand_modifier = hm
    
    @property
    def life_modifier(self):
        return self._life_modifier
    
    @life_modifier.setter
    def life_modifier(self, lm):
        if not isinstance(lm, int) and lm is not None:
            raise ValueError("life_modifier must be an int")
        
        self._life_modifier = lm
    
    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, o):
        if not isinstance(o, Player) and o is not None:
            raise ValueError("owner must be a Player")
        
        self._owner = o

    @property
    def controller(self):
        return self._controller
    
    @controller.setter
    def controller(self, c):
        if not isinstance(c, Player) and c is not None:
            raise ValueError("controller must be a Player")
        
        self._controller = c

# CR110.1. A permanent is a card or token on the battlefield.
# A permanent remains on the battlefield indefinitely.
# A card or token becomes a permanent as it enters the battlefield
# and it stops being a permanent as it’s moved to another zone by an effect or rule.
class Permanent(GameObject):
    # CR110.5. A permanent’s status is its physical state.
    # There are four status categories,
    # each of which has two possible values:
    # tapped/untapped, flipped/unflipped, face up/face down, and phased in/phased out.
    # Each permanent always has one of these values for each of these categories.
    _tapped : bool
    _flipped : bool
    _face_up : bool
    _phased_in : bool

    # CR110.2. A permanent’s owner is the same as the owner of the card that represents it
    # (unless it’s a token; see rule 111.2).
    # A permanent’s controller is, by default,
    # the player under whose control it entered the battlefield.
    # Every permanent has a controller.
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
        if controller is None:
            raise ValueError("A permanent must have a controller")
        if owner is None:
            _owner = controller
        else:
            _owner = owner

        self.tapped = tapped
        self.flipped = flipped
        self.face_up = face_up
        self.phased_in = phased_in

        super().__init__(
            name = name,
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
            owner = _owner,
            controller = controller
        )

    @GameObject.controller.setter
    def controller(self, c):
        if not isinstance(c, Player):
            raise ValueError("controller must be a Player")
        
        self._controller = c

    @property
    def tapped(self):
        return self._tapped
    
    @tapped.setter
    def tapped(self, t : bool):
        if not isinstance(t, bool):
            raise ValueError("tapped must be a boolean")
        self._tapped = t

    @property
    def flipped(self):
        return self._flipped
    
    @flipped.setter
    def flipped(self, f : bool):
        if not isinstance(f, bool):
            raise ValueError("flipped must be a boolean")
        self._flipped = f

    @property
    def face_up(self):
        return self._face_up
    
    @face_up.setter
    def face_up(self, f : bool):
        if not isinstance(f, bool):
            raise ValueError("face_up must be a boolean")
        self._face_up = f

    @property
    def phased_in(self):
        return self._phased_in
    
    @phased_in.setter
    def phased_in(self, p : bool):
        if not isinstance(p, bool):
            raise ValueError("phased_in must be a boolean")
        self._phased_in = p

    @classmethod
    def from_card(c : Card) -> Permanent:
        if not isinstance(c, Card):
            raise ValueError("card must be a Card")
        if c.card_type == 'Instant' or c.card_type == 'Sorcery':
            raise ValueError("An instant or sorcery card cannot become a permanent")
        # CR110.3. A nontoken permanent’s characteristics are the same as those printed on its card,
        # as modified by any continuous effects.
        # See rule 613, “Interaction of Continuous Effects.”
        p = Permanent(
            name = c.name,
            mana_cost = c.mana_cost,
            color = c.color,
            color_indicator = c.color_indicator,
            card_type = c.card_type,
            subtype = c.subtype,
            supertype = c.supertype,
            rules_text = c.rules_text,
            abilities = c.abilities,
            power = c.power,
            toughness = c.toughness,
            loyalty = c.loyalty,
            defense = c.defense,
            hand_modifier = c.hand_modifier,
            life_modifier = c.life_modifier,
            owner = c.owner,
            controller = c.owner
            )
        # TODO: apply continuous effects
        return p
