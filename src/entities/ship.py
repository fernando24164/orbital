import math

import pygame


class Ship:
    def __init__(self, coordinates, destination_coordinates):
        self.coordinates = coordinates
        self.destination = destination_coordinates

        self.image = self.scale_image()
        self.rect = self.image.get_rect()

        self.speed = 5

        dx = self.destination[0] - self.rect.x
        dy = self.destination[1] - self.rect.y
        angle = math.atan2(dy, dx)
        self.direction = angle * 180 / math.pi

        self.active = True
        self.rotated_image = pygame.transform.rotate(self.image, self.direction)

    def scale_image(self):
        original_image = pygame.image.load("src/assets/images/spaceship.png")
        orig_width, orig_height = original_image.get_size()
        new_width = int(orig_width * 0.05)
        new_height = int(orig_height * 0.05)
        return pygame.transform.scale(original_image, (new_width, new_height))

    def update(self):
        self.direction_radians = math.radians(self.direction)
        self.rotated_image = pygame.transform.rotate(self.image, self.direction)
        self.rect = self.rotated_image.get_rect(center=self.rect.center)

        if self.active:
            dx = math.cos(self.direction_radians) * self.speed
            dy = math.sin(self.direction_radians) * self.speed
            self.rect.x += dx
            self.rect.y += dy

            distance = math.sqrt(
                (self.rect.x - self.destination[0]) ** 2
                + (self.rect.y - self.destination[1]) ** 2
            )
            if distance < 20:
                self.active = False

    def draw(self, surface):
        if self.active:
            self.update()
            surface.blit(self.rotated_image, self.rect)
        else:
            del self
        surface.blit(self.image, self.rect)
