
import spade

from agent import GoldMinerAgent


async def main():
    print("[1] Starting Gold Miner Agent...")

    agent = GoldMinerAgent(
        "miner@localhost",
        "123456"
    )

    await agent.start()

    print("[2] Gold Miner game is running!")

    await agent.game_finished.wait()

    await agent.stop()

    print("[3] Gold Miner agent stopped.")


if __name__ == "__main__":
    spade.run(main())
