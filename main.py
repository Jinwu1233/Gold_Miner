
import asyncio
import spade

from agent import GoldMinerAgent
from game_model import GameModel
from ui.game_window import GameWindow


async def main():

    # 1. Create the shared game model
    print("[1] Creating game model...")
    model = GameModel()

    # 2. Create SPADE agent
    print("[2] Creating Gold Miner Agent...")
    agent = GoldMinerAgent(
        "miner@localhost",
        "123456",
        model
    )

    # 3. Start SPADE agent
    print("[3] Starting SPADE Agent...")
    await agent.start()

    print("[4] SPADE Agent started successfully!")

    # 4. Create Pygame window
    print("[5] Starting Pygame game...")
    game = GameWindow(model, agent)

    try:
        # Run game and SPADE in the same asyncio event loop
        await game.run()

    finally:
        # Stop SPADE agent when game window closes
        await agent.stop()
        print("[6] Gold Miner Agent stopped.")


if __name__ == "__main__":
    spade.run(main())
