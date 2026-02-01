from .player import Player
from .interface import Interface
from random import choice
from enum import Enum

# CR500.1. A turn consists of five phases, in this order: beginning, precombat main, combat, postcombat main, and ending. 
class PHASE(Enum):
    beginning = 'beginning'
    precombat_main = 'precombat_main'
    combat = 'combat'
    postcombat_main = 'postcombat_main'
    ending = 'ending'
PHASES = [PHASE.beginning, PHASE.precombat_main, PHASE.combat, PHASE.postcombat_main, PHASE.ending]

class Game:
    """Game object
    
    """
    
    def __init__(self, players : list[Player], interface : Interface):
        """Constructor
        
        Keyword arguments:
        players -- each player participating in game
        """
        
        # TODO: assert that all Players are valid objects
        self.num_players = len(players)
        self.active_player = None
        self.players = players
    
    @property
    def active_player(self):
        return self._active_player
    
    @active_player.setter
    def active_player(self, p : Player):
        if not isinstance(p, Player):
            raise ValueError("Player must be a Player object")
        self._active_player = p
        # rotate the list of players so that the active player is first
        self._rotate_players()
        
    def _rotate_players(self):
        """Rotates the players list so that the active player is first"""
        if self.active_player is None:
            raise ValueError("Cannot rotate the player list without an active player")
        active_idx = self.players.index(self.active_player)
        self.players = self.players[active_idx:] + self.players[:active_idx]

    def start(self):
        """# CR103. Starting the Game"""
        for player in self.players:
            # CR103.1. At the start of a game, each player shuffles his or her deck
            player.shuffle_deck()
        # CR103.2. After the decks have been shuffled, the players determine which one of them will choose who takes the first turn.
        # In the first game of a match (including a single-game match), the players may use any mutually agreeable method (flipping a coin, rolling dice, etc.) to do so. 
        self.active_player = choice(self.players)
        # TODO: in matches after G1, have the losing player (or previous active player for draws), choose.
        # CR103.3. Each player begins the game with a starting life total of 20.
        for player in self.players:
            player.life = 20

        # CR103.4. Each player draws a number of cards equal to his or her starting hand size, which is normally seven. 
        mulligan = [True for player in self.players]
        hand_size = [7 for player in self.players]
        while any(mulligan):
            for i, player in enumerate(self.players):
                if mulligan[i]:
                    player.draw(hand_size[i])
            # A player who is dissatisfied with his or her initial hand may take a mulligan.
            # First, the starting player declares whether or not he or she will take a mulligan.
            # Then each other player in turn order does the same.
            for i, player in enumerate(self.players):
                mulligan[i] = player.mulligan(hand_size[i])
            # Once each player has made a declaration, all players who decided to take mulligans do so at the same time.
            # To take amulligan, a player shuffles his or her hand back into his or her library, 
            # then draws a new hand of one fewer cards than he or she had before.
            for i, player in enumerate(self.players):
                if mulligan[i]:
                    player.shuffle_deck(hand=True)
                     # TODO: add logic for multiplayer games to make first mulligan free
                    hand_size[i] -= 1

            # TODO: CR103.5. Some cards allow a player to take actions with them from his or her opening hand.


    def play(self):
        """Main gameplay loop: iteratively checks game state and passes priority to next player until a winner is determined
        Enforces the rules in CR105: Turn Structure
        """
        if self.active_player is None:
            raise RuntimeError("Game.start() must be run before playing a game.")
        first_turn = True
        extra_turns = []
        while True:
            phase_idx = 0
            phase = PHASES[phase_idx]
            pass_in_succession = True
            while True:
                # TODO: CR500.5. When a phase or step ends, any effects scheduled to last “until end of” that phase or step expire.
                # When a phase or step begins, any effects scheduled to last “until” that phase or step expire. 

                # TODO: 500.6. When a phase or step begins, any abilities that trigger “at the beginning of” that phase or step are added to the stack.

                # TODO: check actions, ask player with priority for game actions or pass
                pass_priority = True
                if not pass_priority:
                    pass_in_succession = False
                

                # CR500.2. A phase or step in which players receive priority ends when the stack is empty and all players pass in succession.
                if pass_in_succession:
                    if phase == 'ending':
                        phase_idx = 0
                        phase = PHASES[phase_idx]
                        if len(extra_turns) > 0:
                            self.active_player = extra_turns.pop()
                        else:
                            self.active_player = self.players[1]
                    phase_idx += 1
                    phase = PHASES[phase_idx]
            

