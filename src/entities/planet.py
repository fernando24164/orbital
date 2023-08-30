import logging
import math
import random

import pygame

planet_images = ["gas_planet", "enemy_planet"]


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Planet:
    def __init__(self, size, belongs_to_player, coordinates):
        self.size = size
        self.max_power = min(size * 10, 40)
        self.belongs_to_player = belongs_to_player
        self.selected = False
        self.connected_planet = None
        self.current_power = 0
        self.power_increment = 1
        self.image_escalation = 30
        self.coordinates = coordinates
        self.last_update_time = pygame.time.get_ticks()
        if not self.belongs_to_player:
            self.image = pygame.image.load(
                f"src/assets/images/{random.choices(planet_images)[0]}.png"
            )
            self.image = pygame.transform.scale(
                self.image, (self.image_escalation, self.image_escalation)
            )
        if self.belongs_to_player:
            self.image = pygame.image.load("src/assets/images/blue_planet.png")
            self.image = pygame.transform.scale(self.image, (30, 30))
        self.size = max(self.image.get_width(), self.image.get_height())

    def draw_planet(self, screen):
        if hasattr(self, "image"):
            screen.blit(self.image, self.coordinates)
        else:
            color = (0, 255, 0) if self.belongs_to_player else (255, 0, 0)
            pygame.draw.circle(screen, color, self.coordinates, self.size)

    def draw_max_power_text(self, screen):
        font = pygame.font.SysFont("Arial", 12)
        text_surface = font.render(str(self.current_power), True, (255, 255, 255))

        text_width, text_height = text_surface.get_size()

        x = self.coordinates[0] + self.image_escalation / 2 - text_width / 2
        y = self.coordinates[1] + self.image_escalation / 2 - text_height / 2

        text_pos = (x, y)

        screen.blit(text_surface, text_pos)

    def update_power(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (
            current_time - self.last_update_time
            if self.belongs_to_player
            else current_time - self.last_update_time - random.randrange(500, 1000)
        )
        if elapsed_time >= random.randrange(1000, 2000):
            self.last_update_time = current_time
            if self.current_power < self.max_power:
                self.current_power += self.power_increment

    def draw_circles(self, screen, scaled_coordinates):
        if self.selected and self.belongs_to_player:
            pygame.draw.circle(
                screen,
                (0, 255, 0),
                scaled_coordinates,
                self.size + 3,
                1,
            )
        if not self.belongs_to_player:
            pygame.draw.circle(
                screen,
                (255, 0, 0),
                scaled_coordinates,
                self.size + 3,
                1,
            )

    def draw_line_with_connections(self, screen, scaled_coordinates):
        if (
            self.selected
            and self.connected_planet
            and not self.connected_planet.belongs_to_player
        ):
            pygame.draw.line(
                screen,
                (255, 255, 255),
                scaled_coordinates,
                (
                    self.connected_planet.coordinates[0]
                    + self.connected_planet.image_escalation // 2,
                    self.connected_planet.coordinates[1]
                    + self.connected_planet.image_escalation // 2,
                ),
            )

            # Define the size and color of the squares
            square_size = 10
            square_color = (255, 255, 255)

            # Calculate the distance between the two planets
            dx = self.connected_planet.coordinates[0] - self.coordinates[0]
            dy = self.connected_planet.coordinates[1] - self.coordinates[1]
            distance = math.sqrt(dx**2 + dy**2)

            # Calculate the position of the squares based on the distance and frame count
            frame_count = pygame.time.get_ticks() // 10
            offset = (frame_count % distance) - distance / 2
            x = self.coordinates[0] + dx * ((offset + distance / 2) / distance)
            y = self.coordinates[1] + dy * ((offset + distance / 2) / distance)

            pygame.draw.rect(screen, square_color, (x, y, square_size, square_size))

    def draw(self, screen):
        self.draw_planet(screen)
        self.update_power()
        self.draw_max_power_text(screen)

        # Scale coordinates by image_escalation
        scaled_x = self.coordinates[0] + self.image_escalation // 2
        scaled_y = self.coordinates[1] + self.image_escalation // 2
        scaled_coordinates = (scaled_x, scaled_y)

        self.draw_circles(screen, scaled_coordinates)
        self.draw_line_with_connections(screen, scaled_coordinates)

    def check_click_on_image(self, mouse_x, mouse_y):
        image_width, image_height = (
            self.image.get_width() + self.image_escalation,
            self.image.get_height() + self.image_escalation,
        )
        image_x, image_y = self.coordinates[0], self.coordinates[1]

        if (
            image_x - image_width / 2 < mouse_x < image_x + image_width / 2
            and image_y - image_height / 2 < mouse_y < image_y + image_height / 2
        ):
            return True

        return False

    def check_click_on_connected_image(self, mouse_x, mouse_y):
        image_width, image_height = (
            self.connected_planet.image.get_width()
            + self.connected_planet.image_escalation,
            self.connected_planet.image.get_height()
            + self.connected_planet.image_escalation,
        )
        image_x, image_y = (
            self.connected_planet.coordinates[0],
            self.connected_planet.coordinates[1],
        )

        if (
            image_x - image_width / 2 < mouse_x < image_x + image_width / 2
            and image_y - image_height / 2 < mouse_y < image_y + image_height / 2
        ):
            return True

        return False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.check_click_on_image(mouse_x, mouse_y):
                self.selected = not self.selected
            if self.check_click_on_connected_image(mouse_x, mouse_y):
                if self.current_power >= 5:
                    self.current_power -= 5
                else:
                    self.current_power = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.selected = False

    def connect_to_planet(self, planet):
        self.connected_planet = planet
