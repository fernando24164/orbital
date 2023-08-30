import sys

import pygame

from settings import Settings
from entities.planet import Planet


class Game:
    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Orbital")
        self.player_planet = Planet(
            20,
            True,
            (self.settings.screen_width // 2, self.settings.screen_height // 2),
        )
        self.enemy_planet = Planet(5, False, (30, self.settings.screen_height // 3))
        self.player_planet.connect_to_planet(self.enemy_planet)
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load("src/assets/images/space.png")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.player_planet.handle_event(event)

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.blit(self.bg, (0, 0))
        self.player_planet.draw(self.screen)
        self.enemy_planet.draw(self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run_game()
