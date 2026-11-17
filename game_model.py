
import math


class GameModel:
    def __init__(self):
        self.width = 1000
        self.height = 700

        # Hook pivot
        self.pivot_x = 500
        self.pivot_y = 125

        # Hook movement
        self.angle = 0.0
        self.angle_speed = 0.8
        self.max_angle = math.radians(65)

        self.rope_length = 100
        self.hook_speed = 300

        self.hook_state = "AIMING"
        self.hook_x = self.pivot_x
        self.hook_y = self.pivot_y + self.rope_length

        # Game information
        self.money = 0
        self.target_money = 1000

        # Timer and game status
        self.time_limit = 60
        self.remaining_time = 60
        self.game_status = "PLAYING"

        # Caught item
        self.caught_item = None

        # All items in the mine
        self.items = [
            {"name": "Small Gold", "x": 270, "y": 270,
             "radius": 20, "value": 100, "pull_speed": 280,
             "color": (255, 210, 0)},

            {"name": "Big Gold", "x": 600, "y": 330,
             "radius": 30, "value": 250, "pull_speed": 180,
             "color": (255, 170, 0)},

            {"name": "Diamond", "x": 450, "y": 580,
             "radius": 18, "value": 500, "pull_speed": 320,
             "color": (0, 230, 255)},

            {"name": "Rock", "x": 180, "y": 350,
             "radius": 35, "value": 10, "pull_speed": 120,
             "color": (120, 120, 120)},

            {"name": "Rock", "x": 830, "y": 570,
             "radius": 45, "value": 10, "pull_speed": 100,
             "color": (120, 120, 120)}
        ]

    def update_timer(self, dt):
        if self.game_status != "PLAYING":
            return

        self.remaining_time -= dt

        if self.remaining_time <= 0:
            self.remaining_time = 0

            if self.money >= self.target_money:
                self.game_status = "WON"
            else:
                self.game_status = "LOST"

            print("[GAME] Time is up!")
            print(f"[GAME] Final money: ${self.money}")
            print(f"[GAME] Result: {self.game_status}")

    def update_aiming(self, dt):
        self.angle += self.angle_speed * dt

        if self.angle > self.max_angle:
            self.angle = self.max_angle
            self.angle_speed *= -1
        elif self.angle < -self.max_angle:
            self.angle = -self.max_angle
            self.angle_speed *= -1

        self.hook_x = (
            self.pivot_x + math.sin(self.angle) * self.rope_length
        )
        self.hook_y = (
            self.pivot_y + math.cos(self.angle) * self.rope_length
        )

    def launch_hook(self):
        if (self.hook_state == "AIMING" and self.game_status == "PLAYING"):
            self.hook_state = "LOWERING"

    def check_collision(self):
        """Check whether the hook touches any item."""
        for item in self.items:
            distance = math.hypot(
                self.hook_x - item["x"],
                self.hook_y - item["y"]
            )

            if distance <= 12 + item["radius"]:
                self.caught_item = item
                self.hook_state = "PULLING"
                print(f"[GAME] Caught: {item['name']}")
                return

    def update_hook(self, dt):
        if self.hook_state == "LOWERING":
            self.hook_x += math.sin(self.angle) * self.hook_speed * dt
            self.hook_y += math.cos(self.angle) * self.hook_speed * dt

            # Check collision after moving
            self.check_collision()

            # Reached the bottom without catching anything
            if self.hook_y >= self.height - 50:
                self.hook_state = "PULLING"

        elif self.hook_state == "PULLING":
            speed = self.hook_speed

            if self.caught_item is not None:
                speed = self.caught_item["pull_speed"]

                # The caught item follows the hook
                self.caught_item["x"] = self.hook_x
                self.caught_item["y"] = self.hook_y

            dx = self.pivot_x - self.hook_x
            dy = self.pivot_y - self.hook_y

            distance = math.hypot(dx, dy)

            if distance <= speed * dt:
                self.hook_x = self.pivot_x
                self.hook_y = self.pivot_y

                # Add money when the item reaches the miner
                if self.caught_item is not None:
                    self.money += self.caught_item["value"]
                    if self.money >= self.target_money:
                        self.game_status = "WON"
                        print("[GAME] YOU WIN!")

                    print(
                        f"[GAME] Sold {self.caught_item['name']}: "
                        f"${self.caught_item['value']}"
                    )
                    print(f"[GAME] Total money: ${self.money}")

                    self.items.remove(self.caught_item)
                    self.caught_item = None

                self.hook_state = "AIMING"

            else:
                self.hook_x += dx / distance * speed * dt
                self.hook_y += dy / distance * speed * dt

    def restart(self):
        self.__init__()
        print("[GAME] New game started!")

    def get_game_info(self):
        return {
            "money": self.money,
            "remaining_time": self.remaining_time,
            "game_status": self.game_status,
            "hook_state": self.hook_state,
            "caught_item": self.caught_item
        }