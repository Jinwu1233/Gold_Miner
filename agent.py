
import asyncio
import spade

from spade.behaviour import FSMBehaviour

from states import (
    StartState,
    AimingState,
    LoweringState,
    PullingState,
    SellingState,
    CheckingState,
    VictoryState,
    FailedState,
    EndState
)


class GoldMinerAgent(spade.agent.Agent):

    def __init__(self, jid, password, game_model):
        super().__init__(jid, password)

        # Share the same GameModel with Pygame
        self.model = game_model

        # Signal that the FSM has finished
        self.game_finished = asyncio.Event()

        # Signal that the player wants to restart
        self.restart_requested = asyncio.Event()

        # Count completed mining rounds
        self.round_number = 0

    async def setup(self):

        print("[SPADE] Gold Miner Agent started!")

        # Create FSM
        fsm = FSMBehaviour()

        # Register nine states
        fsm.add_state("START", StartState(), initial=True)
        fsm.add_state("AIMING", AimingState())
        fsm.add_state("LOWERING", LoweringState())
        fsm.add_state("PULLING", PullingState())
        fsm.add_state("SELLING", SellingState())
        fsm.add_state("CHECKING", CheckingState())
        fsm.add_state("VICTORY", VictoryState())
        fsm.add_state("FAILED", FailedState())
        fsm.add_state("END", EndState())

        # Define transitions
        fsm.add_transition("START", "AIMING")

        # Normal mining process
        fsm.add_transition("AIMING", "LOWERING")
        fsm.add_transition("LOWERING", "PULLING")
        fsm.add_transition("PULLING", "SELLING")
        fsm.add_transition("SELLING", "CHECKING")

        # Handle game status changes
        fsm.add_transition("AIMING", "CHECKING")
        fsm.add_transition("LOWERING", "CHECKING")
        fsm.add_transition("PULLING", "CHECKING")

        # Check whether to continue or finish
        fsm.add_transition("CHECKING", "AIMING")
        fsm.add_transition("CHECKING", "VICTORY")
        fsm.add_transition("CHECKING", "FAILED")

        # Game ending
        fsm.add_transition("VICTORY", "END")
        fsm.add_transition("FAILED", "END")

        # Restart the game
        fsm.add_transition("END", "START")

        # Attach FSM to the agent
        self.add_behaviour(fsm)

        print("[SPADE] FSM initialized!")
