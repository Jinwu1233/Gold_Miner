
import asyncio
import random
import time

from spade.behaviour import State

from game_config import GAME_TIME, TARGET_MONEY, ITEMS


class StartState(State):
    """
    Initialize the game before the miner starts working.
    """

    async def run(self):
        agent = self.agent

        agent.money = 0
        agent.start_time = time.monotonic()
        agent.current_item = None
        agent.round_number = 0

        print("\n========== GOLD MINER ==========")
        print("Welcome to the Gold Mine!")
        print(f"Target money: ${TARGET_MONEY}")
        print(f"Time limit: {GAME_TIME} seconds")
        print("================================\n")

        self.set_next_state("AIMING")


class AimingState(State):
    """
    Decide whether the miner can start another mining attempt.
    """

    async def run(self):
        agent = self.agent

        elapsed = time.monotonic() - agent.start_time
        remaining = GAME_TIME - elapsed

        print(f"\nTime remaining: {max(0, int(remaining))} seconds")
        print(f"Current money: ${agent.money}")

        # Give the player a short moment before launching the claw.
        await asyncio.sleep(1)

        self.set_next_state("LOWERING")


class LoweringState(State):
    """
    Simulate the claw moving down into the mine.
    """

    async def run(self):
        agent = self.agent

        agent.round_number += 1

        print(f"\n--- Mining Round {agent.round_number} ---")
        print("The claw is moving down...")

        await asyncio.sleep(1)

        self.set_next_state("PULLING")


class PullingState(State):
    """
    Randomly select an object and simulate pulling it up.
    """

    async def run(self):
        agent = self.agent

        # Each mining attempt can produce a different object.
        agent.current_item = random.choice(ITEMS)

        item = agent.current_item

        print(f"The claw caught: {item['name']}")
        print(f"Pulling time: {item['weight']} seconds")

        await asyncio.sleep(item["weight"])

        print("The claw has returned to the surface!")

        self.set_next_state("SELLING")


class SellingState(State):
    """
    Sell the collected object and update the player's money.
    """

    async def run(self):
        agent = self.agent

        item = agent.current_item
        value = item["value"]

        agent.money += value

        print(f"Sold: {item['name']}")
        print(f"Earned: ${value}")
        print(f"Total money: ${agent.money}")

        self.set_next_state("CHECKING")


class CheckingState(State):
    """
    Check whether the player has won or run out of time.
    """

    async def run(self):
        agent = self.agent

        elapsed = time.monotonic() - agent.start_time

        if agent.money >= TARGET_MONEY:
            print("\nYou reached the target!")
            self.set_next_state("VICTORY")

        elif elapsed >= GAME_TIME:
            print("\nTime is up!")
            self.set_next_state("FAILED")

        else:
            self.set_next_state("AIMING")


class VictoryState(State):
    """
    Display the result when the player reaches the target.
    """

    async def run(self):
        agent = self.agent

        print("\n********************************")
        print("          YOU WIN!")
        print("********************************")
        print(f"Final money: ${agent.money}")

        self.set_next_state("END")


class FailedState(State):
    """
    Display the result when the time limit is reached.
    """

    async def run(self):
        agent = self.agent

        print("\n********************************")
        print("          GAME OVER!")
        print("********************************")
        print(f"Final money: ${agent.money}")
        print(f"Target money: ${TARGET_MONEY}")

        self.set_next_state("END")


class EndState(State):
    """
    Display the final game summary.
    """

    async def run(self):
        agent = self.agent

        elapsed = time.monotonic() - agent.start_time

        print("\n========== GAME SUMMARY ==========")
        print(f"Total money: ${agent.money}")
        print(f"Mining rounds: {agent.round_number}")
        print(f"Time used: {int(elapsed)} seconds")
        print("Thanks for playing Gold Miner!")
        print("==================================")
        agent.game_finished.set()
        # No next state: the FSM execution finishes here.
        