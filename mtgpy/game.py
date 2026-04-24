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
    combat_damage = 'combat_damage'
    combat_damage_nofs = 'combat_damage_nofs'
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
        Step.combat_damage,
        Step.end_combat
    ],
    Phase.postcombat_main: [Step.no_step],
    # CR512.1. The ending phase consists of two steps: end and cleanup.
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
    Step.combat_damage_nofs: Phase.combat,
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
        
        # Fields used to track the normal steps/phases/turns outside of extra steps/phases/turns
        self.nonextra_step : Step = None
        self.nonextra_phase : Step = None
        self.nonextra_turn : Player = None

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
                    # CR509.1. First, the defending player declares blockers.
                    # This turn-based action doesn’t use the stack.
                    self.execute_declare_blockers()

                if self.step == Step.combat_damage:
                    # CR510.4. If at least one attacking or blocking creature has first strike (see rule 702.7)
                    # or double strike (see rule 702.4) as the combat damage step begins,
                    # the only creatures that assign combat damage in that step are those with first strike or double strike.
                    # After that step, instead of proceeding to the end of combat step,
                    # the phase gets a second combat damage step.
                    # The only creatures that assign combat damage in that step are the remaining attackers and blockers
                    # that had neither first strike nor double strike as the first combat damage step began,
                    # as well as the remaining attackers and blockers that currently have double strike.
                    # After that step, the phase proceeds to the end of combat step.
                    x_strike_creatures = [attacker for attacker in self.attacking_creatures.keys() if 
                                          'first_strike' in attacker.abilities or 'double_strike' in attacker.abilities] + \
                                         [blocker for blocker in self.blocking_creatures.keys() if 
                                          'first_strike' in blocker.abilities or 'double_strike' in blocker.abilities]
                    first_strike_step = len(x_strike_creatures) > 0
                    if first_strike_step:
                        self.extra_steps[Phase.combat][Step.combat_damage].append(Step.combat_damage_nofs)

                    # CR510.1. First, the active player announces how each attacking creature assigns its combat damage,
                    # then the defending player announces how each blocking creature assigns its combat damage.
                    # This turn-based action doesn’t use the stack.
                    damage_assignments = self.assign_combat_damage(first_strike=first_strike_step)

                if self.step == Step.combat_damage_nofs:
                    # CR510.1
                    damage_assignments = self.assign_combat_damage()


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


                # CR503.1, CR504.2, CR505.6, CR507.2, CR508.2, CR509.2, CR511.1, 513.1
                # ...the active player gets priority
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

            # CR511.3. As soon as the end of combat step ends, all creatures, battles, and planeswalkers are removed from combat.
            # After the end of combat step ends, the combat phase is over and the postcombat main phase begins (see rule 505).
            if self.step == Step.end_combat:
                self.attacking_player = None
                self.defending_players = []
                self.attacking_creatures.clear()
                self.blocking_creatures.clear()

            # Determine the next turn, phase, and step
            next_step, next_phase, next_turn, extra = self.next_step()
            if not extra:
                # only update the nonextra step/phase/turn if were are not entering an extra step/phase/turn
                self.step = self.nonextra_step = next_step
                self.phase = self.nonextra_phase = next_phase
                self.active_player = self.nonextra_turn = next_turn
            else:
                self.step = next_step
                self.phase = next_phase
                self.active_player = next_turn

            # CR500.12. No game events can occur between steps, phases, or turns.
                     
    def next_step(self) -> tuple[Step, Phase, Player, bool]:
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

        extra = False

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
                extra = True
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
                extra = False

            # CR500.11. Some effects can cause a step, phase, or turn
            # to be skipped.
            # To skip a step, phase, or turn is to proceed past it
            # as though it didn’t exist.
            if next_step in self.skip_steps or \
                next_phase in self.skip_phases or \
                next_turn in self.skip_turns:
                skip = True

        return next_step, next_phase, next_turn, extra

    def execute_untap_step(self) -> None:
        """As one of two steps without priority, 
        the untap step only executes a few defined actions.
        CR502"""
        if self.step != Step.untap:
            raise RuntimeError("Untap step actions can only be made in the untap step")
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

    def execute_cleanup_step(self) -> bool:
        """CR514"""
        # TODO: CR514.1. First, if the active player’s hand contains more cards than their maximum hand size
        # (normally seven), they discard enough cards to reduce their hand size to that number.
        # This turn-based action doesn’t use the stack.
        if self.active_player.hand_size > self.active_player.maximum_hand_size:
            self.active_player.discard(self.active_player.hand_size - self.active_player.maximum_hand_size)

        # TODO: CR514.2. Second, the following actions happen simultaneously:
        # all damage marked on permanents (including phased-out permanents) is removed
        # and all “until end of turn” and “this turn” effects end. This turn-based action doesn’t use the stack.
        
        # TODO: remove marked damage from all permanents

        # CR514.3. Normally, no player receives priority during the cleanup step,
        # so no spells can be cast and no abilities can be activated.
        # However, this rule is subject to the following exception:

        # CR514.3a At this point, the game checks to see if any state-based actions
        # would be performed and/or any triggered abilities are waiting to be put onto the stack
        # (including those that trigger “at the beginning of the next cleanup step”).
        # If so, those state-based actions are performed, then those triggered abilities are put on the stack,
        # then the active player gets priority.
        # Players may cast spells and activate abilities.
        # Once the stack is empty and all players pass in succession, another cleanup step begins.
        # TODO: check SBA and triggered abilities to see if players get priority in this step.
        # If so, add an extra cleanup step after the current one


    def execute_declare_attackers(self) -> list[tuple[Creature, Player | Planeswalker | Battle]]:
        """The active player declares attackers"""
        if self.step != Step.declare_attackers:
            raise RuntimeError("Declaring attackers can only be made in the declare attackers step")
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

        


        attackers : list[tuple[Creature, Player | Planeswalker | Battle]] = \
            self.active_player.declare_attackers()
        
        # CR508.1k Each chosen creature still controlled by the active player becomes an attacking creature.
        # It remains an attacking creature until it’s removed from combat or the combat phase ends, whichever comes first. See rule 506.4.
        for (creature, defender) in attackers:
            if creature not in self.attacking_creatures.keys():
                self.attacking_creatures[creature] = defender

        # CR508.1m Any abilities that trigger on attackers being declared trigger.
        

        # TODO: verify valid attackers
        return attackers

    def execute_declare_blockers(self) -> list[tuple[Creature, list[Creature]]]:
        """The defending players declare blockers"""
        if self.step != Step.declare_blockers:
            raise RuntimeError("Declaring blockers can only be made in the declare blockers step")

        # CR509.1a The defending player chooses which creatures they control, if any, will block.
        # The chosen creatures must be untapped and they can’t also be battles.
        # For each of the chosen creatures,
        # the defending player chooses one creature for it to block that’s attacking that player,
        # a planeswalker they control, or a battle they protect.

        # CR509.1b The defending player checks each creature they control to see
        # whether it’s affected by any restrictions (effects that say a creature can’t block,
        # or that it can’t block unless some condition is met).
        # If any restrictions are being disobeyed, the declaration of blockers is illegal.
        # A restriction may be created by an evasion ability
        # (a static ability an attacking creature has that restricts what can block it).
        # If an attacking creature gains or loses an evasion ability after a legal block has been declared,
        # it doesn’t affect that block. Different evasion abilities are cumulative.

        # CR509.1c The defending player checks each creature they control to see
        # whether it’s affected by any requirements
        # (effects that say a creature must block,
        # or that it must block if some condition is met).
        # If the number of requirements that are being obeyed is fewer than
        # the maximum possible number of requirements that could be obeyed
        # without disobeying any restrictions, the declaration of blockers is illegal.

        # CR509.1d If any of the chosen creatures require paying costs to block,
        # the defending player determines the total cost to block.
        # Costs may include paying mana, tapping permanents, sacrificing permanents,
        # discarding cards, and so on.

        # CR509.1e If any of the costs require mana,
        # the defending player then has a chance to activate mana abilities
        # (see rule 605, “Mana Abilities”).

        # CR509.1f Once the player has enough mana in their mana pool,
        # they pay all costs in any order. Partial payments are not allowed.

        # TODO: is a list the most appropriate data structure for this? or a set?
        blockers : list[tuple[Creature, list[Creature]]] = []
        for p in self.defending_players:
            p_blockers : list[tuple[Creature, list[Creature]]] = \
                p.declare_blockers()
            blockers.append(p_blockers)

        # CR509.1g Each chosen creature still controlled by the defending player becomes a blocking creature.
        # Each one is blocking the attacking creatures chosen for it.
        # It remains a blocking creature until it’s removed from combat or the combat phase ends,
        # whichever comes first. See rule 506.4.
        for (creature, blockees) in blockers:
            if creature not in self.blocking_creatures.keys():
                self.blocking_creatures[creature] = blockees

        # CR509.1i Any abilities that trigger on blockers being declared trigger.
        # See rule 509.2a for more information.

        return blockers
    
    def assign_combat_damage(self, first_strike = False) -> tuple[object]:
        if self.step != Step.combat_damage and self.step != Step.combat_damage_fs:
            raise RuntimeError("Assigning combat damage can only be made in a combat step")
        
        damage_assignments : dict[Creature, dict[Creature | Player | Planeswalker | Battle, int]] = {}
        
        # if we are in a first strike combat damage step, only creatures with first strike or double strike assign damage
        # if we are not, then only creatures without first strike or with double strike assign combat damage
        active_attackers : dict[Creature, Player | Planeswalker | Battle] = {}
        for attacker, defender in self.attacking_creatures.items():
            if first_strike:
                if 'first_strike' in attacker.abilities or 'double_strike' in attacker.abilities:
                    active_attackers[attacker] = defender
            else:
                # first strike attackers do not deal damage in non-fs damage step unless they also have double strike
                if 'first_strike' not in attacker.abilities or 'double_strike' in attacker.abilities:
                    active_attackers[attacker] = defender

        active_blockers : dict[Creature, list[Creature]] = {}
        for blocker, blockees in self.blocking_creatures.items():
            if first_strike:
                if 'first_strike' in blocker.abilities or 'double_strike' in blocker.abilities:
                    active_blockers[blocker] = blockees
            else:
                if 'first_strike' not in blocker.abilities or 'double_strike' in blocker.abilities:
                    active_blockers[blocker] = blockees

        blocked_attackers : dict[Creature, list[Creature]] = {}
        for blocker, blockees in self.blocking_creatures:
            for blocked_attacker in blockees:
                if blocked_attacker in active_attackers.keys():
                    blocked_attackers.setdefault(blocked_attacker, []).append(blocker)
        
        # CR510.1a Each attacking creature and each blocking creature assigns combat damage equal to its power.
        # Creatures that would assign 0 or less damage this way don’t assign combat damage at all.
        attackers_with_nonzero_power : dict[Creature, Player | Planeswalker | Battle] = {}
        for attacker, defender in active_attackers:
            if attacker.power > 0:
                attackers_with_nonzero_power[attacker] = defender

        blockers_with_nonzero_power : dict[Creature, list[Creature]] = {}
        for blocker, blockees in active_blockers:
            if blocker.power > 0:
                blockers_with_nonzero_power[blocker] = blockees

        # CR510.1b An unblocked creature assigns its combat damage to
        # the player, planeswalker, or battle it’s attacking.
        # If it isn’t currently attacking anything
        # (if, for example, it was attacking a planeswalker that has left the battlefield),
        # it assigns no combat damage.
        for attacker, defender in attackers_with_nonzero_power:
            if defender is None:
                continue
            if attacker not in blocked_attackers.keys():
                damage_assignments[attacker][defender] = attacker.power

        # CR510.1c A blocked creature assigns its combat damage to the creatures blocking it.
        # If no creatures are currently blocking it
        # (if, for example, they were destroyed or removed from combat),
        # it assigns no combat damage.
        # If exactly one creature is blocking it,
        # it assigns all its combat damage to that creature.
        # If two or more creatures are blocking it,
        # it assigns its combat damage to those creatures divided
        # as its controller chooses among them.
        for attacker, blockers in blocked_attackers:
            if len(blockers) == 0:
                # TODO: trample exception
                continue
            if len(blockers) == 1:
                damage_assignments[attacker][blockers[0]] = attacker.power
            else:
                damage_assignment : dict[Creature, int] = \
                    self.active_player.assign_combat_damage(attacker, blockers)
                damage_assignments[attacker] = damage_assignment
                
        # CR510.1d A blocking creature assigns combat damage to the creatures it’s blocking.
        # If it isn’t currently blocking any creatures
        # (if, for example, they were destroyed or removed from combat),
        # it assigns no combat damage.
        # If it’s blocking exactly one creature,
        # it assigns all its combat damage to that creature.
        # If it’s blocking two or more creatures,
        # it assigns its combat damage divided as its controller chooses among them.
        for blocker, blockees in blockers_with_nonzero_power:
            if len(blockees) == 0:
                continue
            if len(blockees) == 1:
                damage_assignments[blocker][blockees[0]] = blocker.power
            else:
                damage_assignment : dict[Creature, int] = \
                    blocker.player_controller.assign_combat_damage(blocker, blockees)
                damage_assignments[blocker] = damage_assignment
        
        # TODO: CR510.1e Once a player has assigned combat damage from each attacking or blocking creature they control,
        # the total damage assignment
        # (not solely the damage assignment of any individual attacking or blocking creature)
        # is checked to see if it complies with the above rules.
        # If it doesn’t, the combat damage assignment is illegal;
        # the game returns to the moment before that player began to assign combat damage.
        # (See rule 732, “Handling Illegal Actions.”)


        return damage_assignments

