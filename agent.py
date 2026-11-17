
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

    async def setup(self):
        print("Gold Miner Agent started!")

        # Shared game data
        self.game_finished = asyncio.Event()

        # Create the finite state machine
        fsm = FSMBehaviour()

        # Register all nine states
        fsm.add_state("START", StartState(), initial=True)
        fsm.add_state("AIMING", AimingState())
        fsm.add_state("LOWERING", LoweringState())
        fsm.add_state("PULLING", PullingState())
        fsm.add_state("SELLING", SellingState())
        fsm.add_state("CHECKING", CheckingState())
        fsm.add_state("VICTORY", VictoryState())
        fsm.add_state("FAILED", FailedState())
        fsm.add_state("END", EndState())

        # Define possible state transitions
        fsm.add_transition("START", "AIMING")

        fsm.add_transition("AIMING", "LOWERING")
        fsm.add_transition("LOWERING", "PULLING")
        fsm.add_transition("PULLING", "SELLING")
        fsm.add_transition("SELLING", "CHECKING")

        fsm.add_transition("CHECKING", "AIMING")
        fsm.add_transition("CHECKING", "VICTORY")
        fsm.add_transition("CHECKING", "FAILED")

        fsm.add_transition("VICTORY", "END")
        fsm.add_transition("FAILED", "END")

        # Attach FSM to the agent
        self.add_behaviour(fsm)
