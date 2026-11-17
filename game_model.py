
import math
import random


class GameModel:

    def __init__(self):
        self.width = 1000
        self.height = 700

        # Hook pivot position
        self.pivot = (500, 125)
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

        # Level information
        self.level = 1
        self.target_money = 1000

        # Timer
        self.time_limit = 60
        self.remaining_time = self.time_limit

        self.game_status = "PLAYING"

        # Caught item
        self.caught_item = None

        # Item generation
        self.items = []
        self.target_item_count = 10

        self.generate_items(self.target_item_count)

        print("[GAME] Game initialized!")
        print(f"[GAME] Level: {self.level}")
        print(f"[GAME] Target money: ${self.target_money}")

    # --------------------------------
    # Generate items
    # --------------------------------
    def generate_items(self, count):

        for _ in range(count):

            item_type = self.random_item_type()

            # Generate a position without excessive overlap
            for attempt in range(50):

                x = random.randint(70, 930)
                y = random.randint(230, 620)

                valid_position = True

                for existing in self.items:
                    distance = math.hypot(
                        x - existing["x"],
                        y - existing["y"]
                    )

                    if distance < 75:
                        valid_position = False
                        break

                if valid_position:
                    break

            item = self.create_item(item_type, x, y)
            self.items.append(item)

    # --------------------------------
    # Random item type
    # --------------------------------
    def random_item_type(self):

        # Higher levels provide better rewards
        if self.level == 1:
            choices = [
                ("Small Gold", 40),
                ("Big Gold", 20),
                ("Diamond", 10),
                ("Rock", 30)
            ]

        elif self.level <= 3:
            choices = [
                ("Small Gold", 35),
                ("Big Gold", 25),
                ("Diamond", 20),
                ("Rock", 20)
            ]

        else:
            choices = [
                ("Small Gold", 25),
                ("Big Gold", 30),
                ("Diamond", 30),
                ("Rock", 15)
            ]

        names = [item[0] for item in choices]
        weights = [item[1] for item in choices]

        return random.choices(
            names,
            weights=weights,
            k=1
        )[0]

    # --------------------------------
    # Create an item
    # --------------------------------
    def create_item(self, name, x, y):

        item_data = {

            "Small Gold": {
                "radius": 20,
                "value": 100,
                "pull_speed": 280,
                "color": (255, 210, 0)
            },

            "Big Gold": {
                "radius": 30,
                "value": 250,
                "pull_speed": 180,
                "color": (255, 170, 0)
            },

            "Diamond": {
                "radius": 18,
                "value": 500,
                "pull_speed": 320,
                "color": (0, 230, 255)
            },

            "Rock": {
                "radius": 35,
                "value": 10,
                "pull_speed": 120,
                "color": (120, 120, 120)
            }
        }

        data = item_data[name]

        return {
            "name": name,
            "x": x,
            "y": y,
            "radius": data["radius"],
            "value": data["value"],
            "pull_speed": data["pull_speed"],
            "color": data["color"]
        }

    # --------------------------------
    # Replenish items
    # --------------------------------
    def replenish_items(self):

        if self.game_status != "PLAYING":
            return

        # Maintain enough items in the mine
        if len(self.items) <= 2:

            missing = self.target_item_count - len(self.items)

            if missing > 0:
                print("[GAME] Generating new items...")
                self.generate_items(missing)

    # --------------------------------
    # Level progression
    # --------------------------------
    def check_level_progress(self):

        while self.money >= self.target_money:

            self.level += 1

            # Increase the target for the next level
            self.target_money += 500 * (self.level - 1) + 500

            # Increase item count
            self.target_item_count = 8 + self.level * 2

            # Reset timer for the new level
            self.remaining_time = self.time_limit

            # Generate more items
            self.generate_items(
                max(0, self.target_item_count - len(self.items))
            )

            print("\n================================")
            print(f"[GAME] LEVEL {self.level} UNLOCKED!")
            print(f"[GAME] Current money: ${self.money}")
            print(f"[GAME] New target: ${self.target_money}")
            print(f"[GAME] New item count: {len(self.items)}")
            print("================================\n")

    # --------------------------------
    # Update timer
    # --------------------------------
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

    # --------------------------------
    # Update hook aiming
    # --------------------------------
    def update_aiming(self, dt):

        self.angle += self.angle_speed * dt

        if self.angle > self.max_angle:
            self.angle = self.max_angle
            self.angle_speed *= -1

        elif self.angle < -self.max_angle:
            self.angle = -self.max_angle
            self.angle_speed *= -1

        self.hook_x = (
            self.pivot_x +
            math.sin(self.angle) * self.rope_length
        )

        self.hook_y = (
            self.pivot_y +
            math.cos(self.angle) * self.rope_length
        )

    # --------------------------------
    # Launch hook
    # --------------------------------
    def launch_hook(self):

        if (
            self.hook_state == "AIMING"
            and self.game_status == "PLAYING"
        ):
            self.hook_state = "LOWERING"

    # --------------------------------
    # Check collision
    # --------------------------------
    def check_collision(self):

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

    # --------------------------------
    # Update hook movement
    # --------------------------------
    def update_hook(self, dt):

        if self.hook_state == "LOWERING":

            self.hook_x += (
                math.sin(self.angle) * self.hook_speed * dt
            )

            self.hook_y += (
                math.cos(self.angle) * self.hook_speed * dt
            )

            # Check collision
            self.check_collision()

            # Reached the bottom
            if self.hook_y >= self.height - 50:
                self.hook_state = "PULLING"

        elif self.hook_state == "PULLING":

            speed = self.hook_speed

            if self.caught_item is not None:

                speed = self.caught_item["pull_speed"]

                # Item follows the hook
                self.caught_item["x"] = self.hook_x
                self.caught_item["y"] = self.hook_y

            dx = self.pivot_x - self.hook_x
            dy = self.pivot_y - self.hook_y

            distance = math.hypot(dx, dy)

            if distance <= speed * dt:

                self.hook_x = self.pivot_x
                self.hook_y = self.pivot_y

                # Sell collected item
                if self.caught_item is not None:

                    item = self.caught_item

                    self.money += item["value"]

                    print(
                        f"[GAME] Sold {item['name']}: "
                        f"${item['value']}"
                    )

                    print(
                        f"[GAME] Total money: ${self.money}"
                    )

                    self.items.remove(item)
                    self.caught_item = None

                    # Check whether the player reached
                    # the next level
                    self.check_level_progress()

                    # Replenish the mine
                    self.replenish_items()

                self.hook_state = "AIMING"

            else:

                self.hook_x += dx / distance * speed * dt
                self.hook_y += dy / distance * speed * dt

    # --------------------------------
    # Restart game
    # --------------------------------
    def restart(self):

        self.__init__()

        print("[GAME] New game started!")

    # --------------------------------
    # Get game information
    # --------------------------------
    def get_game_info(self):

        return {
            "money": self.money,
            "level": self.level,
            "target_money": self.target_money,
            "remaining_time": self.remaining_time,
            "game_status": self.game_status,
            "hook_state": self.hook_state,
            "caught_item": self.caught_item,
            "item_count": len(self.items)
        }
