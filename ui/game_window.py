
import pygame
import math
import asyncio


class GameWindow:

    def __init__(self, model, agent):
        pygame.init()

        self.model = model
        self.agent = agent

        self.width = 1000
        self.height = 700

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )
        pygame.display.set_caption("Gold Miner - SPADE Agent")

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("arial", 32)
        self.small_font = pygame.font.SysFont("arial", 22)
        self.title_font = pygame.font.SysFont("arial", 42, bold=True)

        self.running = True

    # -----------------------------
    # Handle keyboard and window events
    # -----------------------------
    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    self.model.launch_hook()

                elif event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_r:

                    if self.model.game_status in ("WON", "LOST"):
                        self.agent.restart_requested.set()

    # -----------------------------
    # Draw background
    # -----------------------------
    def draw_background(self):

        self.screen.fill((25, 35, 55))

        # Sky
        pygame.draw.rect(
            self.screen,
            (80, 160, 210),
            (0, 0, self.width, 180)
        )

        # Ground
        pygame.draw.rect(
            self.screen,
            (110, 75, 40),
            (0, 180, self.width, self.height - 180)
        )

        # Ground surface
        pygame.draw.line(
            self.screen,
            (80, 180, 80),
            (0, 180),
            (self.width, 180),
            8
        )

    # -----------------------------
    # Draw miner
    # -----------------------------
    def draw_miner(self):

        miner_x = 500
        miner_y = 105

        # Body
        pygame.draw.circle(
            self.screen,
            (255, 200, 100),
            (miner_x, miner_y),
            25
        )

        # Hat
        pygame.draw.rect(
            self.screen,
            (120, 60, 20),
            (miner_x - 25, miner_y - 28, 50, 10)
        )

        # Body
        pygame.draw.rect(
            self.screen,
            (40, 80, 180),
            (miner_x - 20, miner_y + 20, 40, 45)
        )

    # -----------------------------
    # Draw hook
    # -----------------------------
    def draw_hook(self):

        pivot_x, pivot_y = self.model.pivot

        hook_x = self.model.hook_x
        hook_y = self.model.hook_y

        pygame.draw.line(
            self.screen,
            (30, 30, 30),
            (pivot_x, pivot_y),
            (hook_x, hook_y),
            4
        )

        # Hook tip
        pygame.draw.circle(
            self.screen,
            (220, 220, 220),
            (int(hook_x), int(hook_y)),
            10
        )

        pygame.draw.arc(
            self.screen,
            (220, 220, 220),
            (
                int(hook_x) - 10,
                int(hook_y) - 5,
                25,
                25
            ),
            math.pi,
            math.pi * 1.8,
            4
        )

    # -----------------------------
    # Draw items
    # -----------------------------
    def draw_items(self):

        for item in self.model.items:

            x = int(item["x"])
            y = int(item["y"])
            radius = item["radius"]
            name = item["name"]

            if name == "Small Gold":
                color = (255, 215, 0)

            elif name == "Big Gold":
                color = (255, 170, 0)

            elif name == "Diamond":
                color = (0, 230, 255)

            elif name == "Rock":
                color = (110, 110, 110)

            else:
                color = (180, 180, 180)

            pygame.draw.circle(
                self.screen,
                color,
                (x, y),
                radius
            )

            # Item outline
            pygame.draw.circle(
                self.screen,
                (40, 40, 40),
                (x, y),
                radius,
                2
            )

    # -----------------------------
    # Draw score and timer
    # -----------------------------
    def draw_info(self):

        money_text = self.font.render(
            f"Money: ${self.model.money}",
            True,
            (255, 255, 255)
        )

        time_text = self.font.render(
            f"Time: {int(self.model.remaining_time)}",
            True,
            (255, 255, 255)
        )

        target_text = self.small_font.render(
            f"Target: ${self.model.target_money}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(money_text, (30, 25))
        self.screen.blit(time_text, (780, 25))
        self.screen.blit(target_text, (30, 65))

        instruction = self.small_font.render(
            "SPACE: Launch Hook     ESC: Quit",
            True,
            (255, 255, 255)
        )

        self.screen.blit(instruction, (350, 650))

    # -----------------------------
    # Draw game status overlay
    # -----------------------------
    def draw_game_over(self):

        if self.model.game_status not in ("WON", "LOST"):
            return

        overlay = pygame.Surface(
            (self.width, self.height)
        )

        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))

        self.screen.blit(overlay, (0, 0))

        if self.model.game_status == "WON":
            result_text = "YOU WIN!"
            result_color = (255, 215, 0)

        else:
            result_text = "GAME OVER!"
            result_color = (255, 80, 80)

        title = self.title_font.render(
            result_text,
            True,
            result_color
        )

        score = self.font.render(
            f"Final Money: ${self.model.money}",
            True,
            (255, 255, 255)
        )

        restart = self.small_font.render(
            "Press R to Restart",
            True,
            (255, 255, 255)
        )

        quit_text = self.small_font.render(
            "Press ESC to Quit",
            True,
            (200, 200, 200)
        )

        self.screen.blit(
            title,
            title.get_rect(center=(500, 280))
        )

        self.screen.blit(
            score,
            score.get_rect(center=(500, 350))
        )

        self.screen.blit(
            restart,
            restart.get_rect(center=(500, 420))
        )

        self.screen.blit(
            quit_text,
            quit_text.get_rect(center=(500, 460))
        )

    # -----------------------------
    # Draw complete game screen
    # -----------------------------
    def draw(self):

        self.draw_background()
        self.draw_miner()
        self.draw_items()
        self.draw_hook()
        self.draw_info()
        self.draw_game_over()

        pygame.display.flip()

    # -----------------------------
    # Main asynchronous game loop
    # -----------------------------
    async def run(self):

        while self.running:

            dt = self.clock.tick(60) / 1000.0

            self.handle_events()

            # Update countdown timer
            if self.model.game_status == "PLAYING":
                self.model.update_timer(dt)

            # Update game objects
            if self.model.game_status == "PLAYING":

                if self.model.hook_state == "AIMING":
                    self.model.update_aiming(dt)

                else:
                    self.model.update_hook(dt)

            # Render the game
            self.draw()

            # Allow SPADE FSM behaviours to execute
            await asyncio.sleep(0)

        pygame.quit()
