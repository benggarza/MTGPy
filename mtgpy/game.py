from .player import Player
from .interface import Interface
from .ability import Ability
from random import choice
from enum import Enum
from .types import *

# CR500.1. A turn consists of five phases, in this order:
# beginning, precombat main, combat, postcombat main, and ending. 

# CR505.1. There are two main phases in a turn.
# In each turn, the first main phase (also known as the precombat main phase)
# and the second main phase (also known as the postcombat main phase)
# are separated by the combat phase (see rule 506, “Combat Phase”).
# The precombat and postcombat main phases
# are individually and collectively known as the main phase.
class Phase(Enum):
    beginning = 'beginning'
    precombat_main = 'precombat_main'
    combat = 'combat'
    postcombat_main = 'postcombat_main'
    ending = 'ending'
class Step(Enum):
    untap = 'untap'
    upkeep = 'upkeep'
    draw = 'draw'
    begin_combat = 'begin_combat'
    declare_attackers = 'declare_attackers'
    declare_blockers = 'declare_blockers'
    combat_damage_fs = 'combat_damage_fs'
    combat_damage = 'combat_damage'
    end_combat = 'end_combat'
    end = 'end'
    cleanup = 'cleanup'
    no_step = 'no_step'

PHASES = [
    Phase.beginning,
    Phase.precombat_main,
    Phase.combat,
    Phase.postcombat_main,
    Phase.ending
]
STEPS = {
    # CR501.1. The beginning phase consists of three steps, in this order: untap, upkeep, and draw.
    Phase.beginning: [
        Step.untap,
        Step.upkeep,
        Step.draw
    ],
    Phase.precombat_main: [Step.no_step],
    # CR506.1. The combat phase has five steps, which proceed in order:
    # beginning of combat, declare attackers, declare blockers, combat damage, and end of combat. 
    # There are two combat damage steps if any attacking or blocking creature
    # has first strike (see rule 702.7) or double strike (see rule 702.4).
    Phase.combat: [
        Step.begin_combat,
        Step.declare_attackers,
        Step.declare_blockers,
        Step.combat_damage_fs,
        Step.combat_damage,
        Step.end_combat
    ],
    Phase.postcombat_main: [Step.no_step],
    Phase.ending: [Step.end, Step.cleanup]
}
STEP_PHASES = {
    Step.untap: Phase.beginning,
    Step.upkeep: Phase.beginning,
    Step.draw: Phase.beginning,
    Step.begin_combat: Phase.combat,
    Step.declare_attackers: Phase.combat,
    Step.declare_blockers: Phase.combat,
    Step.combat_damage: Phase.combat,
    Step.end_combat: Phase.combat,
    Step.end: Phase.ending,
    Step.cleanup: Phase.ending
}

class Game:
    """Game object
    
    """
    
    def __init__(self, players : list[Player], interface : Interface):
        """Constructor
        
        Keyword arguments:
        players -- each player participating in game
        """

        self.interface : Interface = Interface
        
        # TODO: assert that all Players are valid objects
        self.num_players : int = len(players)
        self.active_player : Player | None = None
        self.players : list[Player] = players

        self.attacking_player : Player | None = None
        self.defending_players : list[Player] = []

        # CR506.3. Only a creature can attack or block.
        # Only a player, a planeswalker, or a battle can be attacked.
        self.attacking_creatures : dict[Creature, Player | Planeswalker | Battle] = {}
        self.blocking_creatures : dict[Creature, list[Creature]] = {}

        self.step : Step = None
        self.phase : Phase = None

        self.extra_turns : list[Player] = []

        self.extra_phases : dict[Phase, list[Phase]] = {}
        for p in PHASES:
            self.extra_phases[p] = []

        self.extra_steps : dict[Phase, dict[Step, list[Step]]] = {}
        for p in PHASES:
            self.extra_steps[p] = {}
            for s in STEPS[p]:
                self.extra_steps[p][s] = []
        
        # TODO: should these be unordered collections instead?
        self.skip_turns : list[Player] = []
        self.skip_phases : list[Phase] = []
        self.skip_steps : list[Step] = [Step.draw]

        self.triggered_abilities : dict[Phase, dict[Step, set[Ability]]] = {}
        for p in PHASES:
            self.triggered_abilities[p] = {}
            for s in STEPS[p]:
                self.triggered_abilities[p][s] = set()
    
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
            raise ValueError(
                "Cannot rotate the player list without an active player"
            )
        active_idx = self.players.index(self.active_player)
        self.players = self.players[active_idx:] + self.players[:active_idx]

    def start(self):
        """# CR103. Starting the Game"""
        
        # CR103.2. At the start of a game,
        # the players determine which one of them will choose
        # who takes the first turn.
        # In the first game of a match (including a single-game match),
        # the players may use any mutually agreeable method
        # (flipping a coin, rolling dice, etc.) to do so. 

        # TODO: in matches after G1,
        # have the losing player (or previous active player for draws), choose.

        self.active_player = choice(self.players)
       
        # CR103.2b If any players wish to reveal a card with a companion ability
        # that they own from outside the game, they may do so.
        for player in self.players:
            player.declare_companion()

        # TODO: CR103.2c In a Commander game, each player puts their commander
        # from their deck face up into the command zone.

        # TODO: 103.2d In a constructed game, each player playing with
        # sticker sheets reveals all of their sticker sheets and
        # chooses three of them at random.

        for player in self.players:
            # 103.3. After the starting player has been determined and
            # any additional steps performed, each player shuffles their deck
            player.shuffle_deck()

        # TODO: 103.3a In a game using one or more supplementary decks of
        # nontraditional cards (see rule 100.2d),
        # each supplementary deck’s owner shuffles it

        
        # CR103.4. Each player begins the game with a starting life total of 20.
        # TODO: refactor Game to allow for formats with different life totals.
        # CR103.4a-e
        for player in self.players:
            player.life = 20

        # CR103.5. Each player draws a number of cards equal to
        # his or her starting hand size, which is normally seven. 
        mulligan = [True for player in self.players]
        hand_size = [7 for player in self.players]
        while any(mulligan):
            for i, player in enumerate(self.players):
                if mulligan[i]:
                    player.draw(hand_size[i])
            # A player who is dissatisfied with his or her initial hand
            # may take a mulligan.
            # First, the starting player declares whether or not he or she
            # will take a mulligan.
            # Then each other player in turn order does the same.
            for i, player in enumerate(self.players):
                mulligan[i] = player.mulligan(hand_size[i])
            # Once each player has made a declaration, all players who decided
            # to take mulligans do so at the same time.
            # To take a mulligan, a player shuffles his or her hand
            # back into his or her library, 
            # then draws a new hand of one fewer cards than he or she had before
            for i, player in enumerate(self.players):
                if mulligan[i]:
                    player.shuffle_deck(hand=True)
                     # TODO: add logic for multiplayer games
                     # to make first mulligan free CR103.5c
                    hand_size[i] -= 1

            # TODO: CR103.6. Some cards allow a player to take actions with them
            # from his or her opening hand.

        # CR103.8. The starting player takes their first turn.
        self.phase = PHASES[0]
        self.step = STEPS[self.phase][0]

    def play(self):
        """Main gameplay loop: iteratively checks game state
        and passes priority to next player until a winner is determined
        Enforces the rules in CR5XX: Turn Structure
        """
        if self.active_player is None:
            raise RuntimeError(
                "Game.start() must be run before playing a game."
                )
        
        # Main turn/phase/step loop
        while True: 

            # CR500.12. No game events can occur between steps, phases, or turns.
            
            # TODO: CR500.4. As a step or phase begins,
            # if there are effects that last until that step or phase,
            # those effects expire.

            # TODO: CR500.6. When a phase or step begins, 
            # any abilities that trigger “at the beginning of”
            # that phase or step are added to the stack.

            # CR506.2. During the combat phase, the active player is the attacking player;
            # creatures that player controls may attack.
            # During the combat phase of a two-player game,
            # the nonactive player is the defending player;
            # that player, planeswalkers they control, and battles they protect may be attacked.
            if self.phase == Phase.combat:
                self.attacking_player = self.active_player
                # TODO: in multiplayer games, the attacking player *chooses* defending players
                self.defending_players = [p for p in self.players if p != self.active_player]
            else:
                self.attacking_player = None
                self.defending_players = []

            # CR500.3. A step in which no players receive priority
            # ends when all specified actions that take place during
            # that step are completed.
            # The only such steps are
            # the untap step (see rule 502)
            # and certain cleanup steps (see rule 514).
            if self.step == Step.untap or self.step == Step.cleanup:
                if self.step == Step.untap:
                    self.execute_untap_step()

                if self.step == Step.cleanup:
                    self.execute_cleanup_step()
  
            else:
                # Step-specific actions that do not use the stack
                if self.step == Step.draw:
                    # CR504.1. First, the active player draws a card.
                    self.active_player.draw(1)

                if self.phase == Phase.precombat_main:
                    # TODO: CR505.4. Second, if the active player controls
                    # one or more Saga enchantments and
                    # it’s the active player’s precombat main phase,
                    # the active player puts a lore counter on each Saga
                    # they control with one or more chapter abilities.

                    # TODO: CR505.5. Third, if the active player controls
                    # one or more Attractions and it’s the active player’s
                    # precombat main phase, the active player rolls
                    # to visit their Attractions.
                    pass

                if self.step == Step.begin_combat:
                    # TODO: CR507.1. First, if the game being played is
                    # a multiplayer game in which the active player’s opponents
                    # don’t all automatically become defending players,
                    # the active player chooses one of his or her
                    # opponents. That player becomes the defending player.
                    pass

                if self.step == Step.declare_attackers:
                    # CR508.1. First, the active player declares attackers.
                    self.execute_declare_attackers()

                if self.step == Step.declare_blockers:
                    self.execute_declare_blockers()

                # Place triggered abilities onto the stack in APNAP order
                # CR503.1a, CR504.2
                triggered_abilities = \
                    self.triggered_abilities[self.phase][self.step]
                # TODO: CR503.1a. Any abilities that triggered
                # during the untap step and any abilities that triggered
                # at the beginning of the upkeep are put onto the stack
                # before the active player gets priority

                # TODO: how to implement placing abilities onto the stack
                # such that it handles triggers to the draw step draw.
                
                # TODO: adding triggered abilities to stack will be
                # handled once we go over CR603


                # CR503.1, CR504.2, CR505.6, CR507.2, CR508.2. ...the active player gets priority
                while True: 
                    pass_in_succession = True

                    priority_player = self.active_player
                    for p in self.players:
                        action = p.priority()
                        if action is not None:
                            pass_in_succession = False

                            # TODO: check action legality and execute
                            # Most often is one of:
                            # casting spell, activating ability, playing land (CR505.6a,b)
                            # But can also be other things like:
                            # turning a morph card face-up, ninjutsu in combat..
                    

                    # CR500.2. A phase or step in which players receive priority
                    # ends when the stack is empty and all players
                    # pass in succession.
                    # CR505.2. The main phase has no steps,
                    # so a main phase ends when all players pass in succession
                    # while the stack is empty. (See rule 500.2.)
                    if pass_in_succession:
                        break

            # TODO: CR500.5. As a step or phase ends, if there are effects that
            # last until the end of that step or phase, those effects expire.

            # Then any unspent mana left in a player’s mana pool empties.
            for player in self.players:
                player.empty_mana_pool()

            # Determine the next turn, phase, and step
            self.step, self.phase, self.active_player = self.next_step()

            # CR500.12. No game events can occur between steps, phases, or turns.
                     
    def next_step(self) -> tuple[Step, Phase, Player]:
        """Determine the next step, phase and turn according to:
        normal turn structure,
        extra steps/phases/turns,
        skipped steps/phases/turns.
        Enforces CR500.1, CR500.7-10, CR501.1, ...
        """
        step_idx = STEPS[self.phase].index(self.step)
        phase_idx = PHASES.index(self.phase)

        next_step = None
        next_phase = self.phase
        next_turn = self.active_player

        skip = False
        while skip:

            # CR500.9. Some effects can add steps to a phase.
            # They do this by adding the steps directly after a specified
            # step or directly before a specified step.
            # If multiple extra steps are created after the same step, the
            # most recently created step will occur first.
            if len(self.extra_steps[self.phase][self.step]) > 0:
                next_step = self.extra_steps[self.phase][self.step].pop()

                # CR500.10. Some effects add a step after
                # a particular phase. In that case,
                # that effect first creates the phase which normally contains
                # that step directly after the specified phase.
                # Any other steps that phase would normally have are skipped
                # (see rule 500.11).
                next_phase = STEP_PHASES.get(next_step, next_phase)
            else:
                step_idx += 1
                # If it is the last step of the phase, move to the
                # next phase.
                if step_idx == len(STEPS[self.phase]):
                    # CR500.8. Some effects can add phases to a turn.
                    # They do this by adding the phases directly after the
                    # specified phase.
                    if len(self.extra_phases[self.phase][self.step]) > 0:
                        self.phase = self.extra_phases[self.phase][self.step].pop()
                    else:
                        phase_idx += 1
                        # If it is the last phase of the turn, move to the
                        # next turn.
                        if phase_idx == len(PHASES):
                            # CR500.7. Some effects can give a player
                            # extra turns.
                            # They do this by adding the turns directly
                            # after the current turn.
                            if len(self.extra_turns) > 0:
                                next_turn = self.extra_turns.pop()
                            else:
                                next_turn = self.players[1]
                            phase_idx = 0
                        next_phase = PHASES[phase_idx]
                    step_idx = 0
                next_step = STEPS[next_phase][step_idx]

            # CR500.11. Some effects can cause a step, phase, or turn
            # to be skipped.
            # To skip a step, phase, or turn is to proceed past it
            # as though it didn’t exist.
            if next_step in self.skip_steps or \
                next_phase in self.skip_phases or \
                next_turn in self.skip_turns:
                skip = True

        return next_step, next_phase, next_turn

    def execute_untap_step(self) -> None:
        """As one of two steps without priority, 
        the untap step only executes a few defined actions.
        CR502"""
        # TODO: CR502.1. First, all phased-in permanents
        # with phasing that the active player controls phase out,
        # and all phased-out permanents
        # that the active player controlled when they phased out
        # phase in.

        # TODO: CR502.2. Second, if it’s day and
        # the previous turn’s active player didn’t cast any spells
        # during that turn, it becomes night.

        # CR502.3. Third, the active player determines
        # which permanents he or she controls will untap.
        # Then he or she untaps them all simultaneously. 
        self.active_player.untap_permanents()

        # TODO: CR502.4. No player receives priority during the untap step,
        # so no spells can be cast or resolve and
        # no abilities can be activated or resolve.
        # Any ability that triggers during this step will be held until
        # the next time a player would receive priority,
        # which is usually during the upkeep step.

        # check if any triggers are slated for untap step and move them to upkeep step

    def execute_cleanup_step(self) -> None:
        pass

    def execute_declare_attackers(self) -> list[tuple[Creature, Player | Planeswalker | Battle]]:
        """The active player declares attackers"""
        # CR508.1a The active player chooses which creatures that they control, if any, will attack.
        # The chosen creatures must be untapped, they can’t also be battles,
        # and each one must either have haste or have been controlled by the active player continuously
        # since the turn began.

        # CR508.1b If the defending player controls any planeswalkers,
        # is the protector of any battles,
        # or the game allows the active player to attack multiple other players,
        # the active player announces which player, planeswalker, or battle
        # each of the chosen creatures is attacking.

        # CR508.1c The active player checks each creature they control to see
        # whether it’s affected by any restrictions
        # (effects that say a creature can’t attack,
        # or that it can’t attack unless some condition is met).
        # If any restrictions are being disobeyed,
        # the declaration of attackers is illegal.

        # CR508.1d The active player checks each creature they control to see
        # whether it’s affected by any requirements
        # (effects that say a creature attacks if able, or that it attacks if some condition is met).

        # CR508.1e If any of the chosen creatures have banding or a “bands with other” ability,
        # the active player announces which creatures, if any, are banded with which. (See rule 702.22, “Banding.”)

        # CR508.1f The active player taps the chosen creatures.
        # Tapping a creature when it’s declared as an attacker isn’t a cost;
        # attacking simply causes creatures to become tapped.

        # CR508.1g If there are any optional costs to attack with the chosen creatures
        # (expressed as costs a player may pay “as” a creature attacks),
        # the active player chooses which, if any, they will pay.

        # CR508.1h If any of the chosen creatures require paying costs to attack,
        # or if any optional costs to attack were chosen,
        # the active player determines the total cost to attack.

        # CR508.1i If any of the costs require mana,
        # the active player then has a chance to activate mana abilities (see rule 605, “Mana Abilities”).

        # CR508.1j Once the player has enough mana in their mana pool,
        # they pay all costs in any order. Partial payments are not allowed.

        # CR508.1k Each chosen creature still controlled by the active player becomes an attacking creature.
        # It remains an attacking creature until it’s removed from combat or the combat phase ends, whichever comes first. See rule 506.4.

        # CR508.1m Any abilities that trigger on attackers being declared trigger.


        attackers : list[tuple[Creature, Player | Planeswalker | Battle]] = \
            self.active_player.declare_attackers()
        

        # TODO: verify valid attackers
        return attackers