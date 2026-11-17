
import pygame
import math

from game_model import GameModel


class GameWindow:
    def __init__(self):
        pygame.init()

        self.model = GameModel()

        self.screen = pygame.display.set_mode(
            (self.model.width, self.model.height)
        )

        pygame.display.set_caption("Gold Miner")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 28, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 20)

        self.running = True

    
    def handle_events(self):
        for event in pygame.event.get():

            # Window close button
            if event.type == pygame.QUIT:
                self.running = False

            # Keyboard events
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    self.model.launch_hook()

                elif event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_r:
                    if self.model.game_status in ("WON", "LOST"):
                        self.model.restart()


    def draw_background(self):
        # Sky
        self.screen.fill((110, 190, 235))

        # Underground
        pygame.draw.rect(
            self.screen,
            (130, 85, 45),
            (0, 180, self.model.width, 520)
        )

        # Ground surface
        pygame.draw.rect(
            self.screen,
            (70, 150, 55),
            (0, 165, self.model.width, 25)
        )

        # Underground layers
        for y in [300, 450, 600]:
            pygame.draw.line(
                self.screen,
                (160, 110, 65),
                (0, y),
                (self.model.width, y),
                3
            )

    def draw_miner(self):
        x = self.model.pivot_x
        y = self.model.pivot_y

        # Head
        pygame.draw.circle(
            self.screen,
            (255, 190, 120),
            (x, 65),
            22
        )

        # Helmet
        pygame.draw.arc(
            self.screen,
            (245, 190, 40),
            (x - 25, 40, 50, 35),
            math.pi,
            2 * math.pi,
            8
        )

        # Body
        pygame.draw.rect(
            self.screen,
            (40, 70, 160),
            (x - 22, 88, 44, 42),
            border_radius=8
        )

        # Arms
        pygame.draw.line(
            self.screen,
            (255, 190, 120),
            (x - 20, 100),
            (x - 35, 120),
            8
        )

        pygame.draw.line(
            self.screen,
            (255, 190, 120),
            (x + 20, 100),
            (x + 35, 120),
            8
        )

        # Hook machine
        pygame.draw.rect(
            self.screen,
            (70, 70, 70),
            (x - 18, y - 8, 36, 18),
            border_radius=5
        )

    def draw_hook(self):
        model = self.model

        # Rope
        pygame.draw.line(
            self.screen,
            (40, 40, 40),
            (model.pivot_x, model.pivot_y),
            (int(model.hook_x), int(model.hook_y)),
            4
        )

        # Hook ring
        pygame.draw.circle(
            self.screen,
            (190, 190, 190),
            (int(model.hook_x), int(model.hook_y)),
            12,
            4
        )

        # Hook tip
        pygame.draw.arc(
            self.screen,
            (210, 210, 210),
            (
                int(model.hook_x) - 12,
                int(model.hook_y),
                25,
                25
            ),
            0,
            math.pi,
            4
        )

    
    def draw_items(self):
        for item in self.model.items:
            x = int(item["x"])
            y = int(item["y"])
            radius = item["radius"]

            pygame.draw.circle(
                self.screen,
                item["color"],
                (x, y),
                radius
            )

            # Highlight
            pygame.draw.circle(
                self.screen,
                (255, 255, 255),
                (x - radius // 3, y - radius // 3),
                max(3, radius // 5)
            )


    def draw_ui(self):
        money_text = self.font.render(
            f"Money: ${self.model.money}",
            True,
            (255, 255, 255)
        )

        time_text = self.font.render(
            f"Time: {int(self.model.remaining_time)}s",
            True,
            (255, 255, 255)
        )



        target_text = self.font.render(
            f"Target: ${self.model.target_money}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(money_text, (20, 20))
        self.screen.blit(target_text, (750, 20))
        self.screen.blit(time_text, (400, 20))
        if self.model.hook_state == "AIMING":
            message = "Press SPACE to launch the hook"
        else:
            message = self.model.hook_state

        text = self.small_font.render(
            message,
            True,
            (255, 255, 255)
        )

        self.screen.blit(text, (20, 65))

    def draw(self):
        self.draw_background()
        self.draw_items()
        self.draw_miner()
        self.draw_hook()
        self.draw_ui()
        self.draw_game_over()
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            self.handle_events()

            if self.model.game_status == "PLAYING":

                self.model.update_timer(dt)

            if self.model.game_status == "PLAYING":
                if self.model.hook_state == "AIMING":
                    self.model.update_aiming(dt)
                else:
                    self.model.update_hook(dt)

            self.draw()

        pygame.quit()

    def draw_game_over(self):
        if self.model.game_status == "PLAYING":
            return

        overlay = pygame.Surface(
            (self.model.width, self.model.height),
            pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        if self.model.game_status == "WON":
            message = "YOU WIN!"
            color = (255, 220, 0)
        else:
            message = "GAME OVER!"
            color = (255, 80, 80)

        title = pygame.font.SysFont(
            "Arial", 64, bold=True
        ).render(message, True, color)

        score = self.font.render(
            f"Final Money: ${self.model.money}",
            True,
            (255, 255, 255)
        )

        restart = self.small_font.render(
            "Press R to restart",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            title,
            title.get_rect(center=(500, 280))
        )
        self.screen.blit(
            score,
            score.get_rect(center=(500, 360))
        )
        self.screen.blit(
            restart,
            restart.get_rect(center=(500, 420))
        )


if __name__ == "__main__":
    GameWindow().run()
