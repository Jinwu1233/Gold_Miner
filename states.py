
import asyncio

from spade.behaviour import State


class StartState(State):
    """Initialize the FSM for a new game."""

    async def run(self):
        agent = self.agent
        model = agent.model

        agent.round_number = 0

        print("\n========== GOLD MINER ==========")
        print("Welcome to the Gold Mine!")
        print(f"Target money: ${model.target_money}")
        print(f"Time limit: {model.time_limit} seconds")
        print("================================\n")

        self.set_next_state("AIMING")


class AimingState(State):
    """Wait for the player to launch the hook."""

    async def run(self):
        agent = self.agent
        model = agent.model

        print("[FSM] AIMING: Waiting for player...")

        while model.game_status == "PLAYING":
            if model.hook_state != "AIMING":
                agent.round_number += 1
                print(f"[FSM] Round {agent.round_number}")
                self.set_next_state("LOWERING")
                return

            await asyncio.sleep(0.05)

        self.set_next_state("CHECKING")


class LoweringState(State):
    """Monitor the hook while it moves downward."""

    async def run(self):
        model = self.agent.model

        print("[FSM] LOWERING: Hook is moving down...")

        while model.game_status == "PLAYING":
            if model.hook_state == "PULLING":
                print("[FSM] Hook caught an item or reached the bottom.")
                self.set_next_state("PULLING")
                return

            await asyncio.sleep(0.05)

        self.set_next_state("CHECKING")


class PullingState(State):
    """Wait until the hook returns to the miner."""

    async def run(self):
        model = self.agent.model

        print("[FSM] PULLING: Hook is returning...")

        while model.game_status == "PLAYING":
            if model.hook_state == "AIMING":
                print("[FSM] Hook returned to the miner.")
                self.set_next_state("SELLING")
                return

            await asyncio.sleep(0.05)

        self.set_next_state("CHECKING")


class SellingState(State):
    """Confirm that the collected item has been sold."""

    async def run(self):
        model = self.agent.model

        print("[FSM] SELLING: Checking collected item...")

        # GameModel has already updated the money
        # when the item reaches the miner.
        print(f"[FSM] Current money: ${model.money}")

        self.set_next_state("CHECKING")


class CheckingState(State):
    """Check the game result and decide the next state."""

    async def run(self):
        model = self.agent.model

        print("[FSM] CHECKING: Checking game status...")

        if model.money >= model.target_money:
            model.game_status = "WON"
            self.set_next_state("VICTORY")

        elif model.game_status == "WON":
            self.set_next_state("VICTORY")

        elif model.game_status == "LOST":
            self.set_next_state("FAILED")

        elif model.remaining_time <= 0:
            model.game_status = "LOST"
            self.set_next_state("FAILED")

        else:
            self.set_next_state("AIMING")


class VictoryState(State):
    """Handle a winning result."""

    async def run(self):
        model = self.agent.model

        model.game_status = "WON"

        print("\n********************************")
        print("          YOU WIN!")
        print("********************************")
        print(f"Final money: ${model.money}")

        self.set_next_state("END")


class FailedState(State):
    """Handle a losing result."""

    async def run(self):
        model = self.agent.model

        model.game_status = "LOST"

        print("\n********************************")
        print("          GAME OVER!")
        print("********************************")
        print(f"Final money: ${model.money}")
        print(f"Target money: ${model.target_money}")

        self.set_next_state("END")


class EndState(State):
    """Finish the FSM execution."""

    async def run(self):
        agent = self.agent
        model = agent.model

        print("\n========== GAME SUMMARY ==========")
        print(f"Total money: ${model.money}")
        print(f"Mining rounds: {agent.round_number}")
        print(f"Time used: {int(model.time_limit - model.remaining_time)} seconds")
        print("Thanks for playing Gold Miner!")
        print("==================================")

        agent.game_finished.set()
