"""A minimal Enduro-style racing game using pygame.

This module implements a simplified version of the classic Atari "Enduro"
game.  The player controls a car that moves left and right to avoid other
cars while the road scrolls toward the player.  The goal is simply to
survive for as long as possible.

The game is intentionally small so it can serve as a starting point for
further experiments in VS Code.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

import pygame

# Basic colors
WHITE = (255, 255, 255)
GREY = (50, 50, 50)
RED = (200, 0, 0)
BLUE = (0, 0, 200)


@dataclass
class Car:
    """Representation of a car on the track."""

    rect: pygame.Rect
    color: tuple[int, int, int]
    speed: int = 0


class EnduroGame:
    """Encapsulates game state and the main loop."""

    width: int = 480
    height: int = 640
    road_width: int = 320
    player_speed: int = 5
    obstacle_speed: int = 6
    spawn_delay_ms: int = 800

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mini Enduro")
        self.clock = pygame.time.Clock()

        # Player car setup
        car_width, car_height = 40, 60
        start_x = (self.width - car_width) // 2
        start_y = self.height - car_height - 20
        self.player = Car(pygame.Rect(start_x, start_y, car_width, car_height), BLUE)

        # Obstacle cars
        self.obstacles: list[Car] = []
        self.next_spawn = 0
        self.running = True
        self.lane_offset = 0

    # ------------------------------------------------------------------
    def spawn_obstacle(self) -> None:
        """Create a new obstacle car at a random horizontal position."""

        car_width, car_height = 40, 60
        left_bound = (self.width - self.road_width) // 2
        right_bound = left_bound + self.road_width - car_width
        x = random.randint(left_bound, right_bound)
        rect = pygame.Rect(x, -car_height, car_width, car_height)
        self.obstacles.append(Car(rect, RED, self.obstacle_speed))

    # ------------------------------------------------------------------
    def handle_input(self) -> None:
        """Process user input for movement and quitting."""

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.rect.x -= self.player_speed
        if keys[pygame.K_RIGHT]:
            self.player.rect.x += self.player_speed

        # Keep player within road bounds
        left_bound = (self.width - self.road_width) // 2
        right_bound = left_bound + self.road_width - self.player.rect.width
        self.player.rect.x = max(left_bound, min(self.player.rect.x, right_bound))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    # ------------------------------------------------------------------
    def update_obstacles(self) -> None:
        """Move obstacles and remove those off-screen."""

        for car in list(self.obstacles):
            car.rect.y += car.speed
            if car.rect.top > self.height:
                self.obstacles.remove(car)

        # Spawn new obstacles periodically
        now = pygame.time.get_ticks()
        if now >= self.next_spawn:
            self.spawn_obstacle()
            self.next_spawn = now + self.spawn_delay_ms

    # ------------------------------------------------------------------
    def check_collisions(self) -> None:
        """End the game if the player hits another car."""

        for car in self.obstacles:
            if self.player.rect.colliderect(car.rect):
                self.running = False

    # ------------------------------------------------------------------
    def draw_road(self) -> None:
        """Draw the scrolling road and lane markers."""

        self.screen.fill(GREY)
        left_bound = (self.width - self.road_width) // 2
        pygame.draw.rect(
            self.screen,
            (30, 30, 30),
            (left_bound, 0, self.road_width, self.height),
        )

        # Lane markers
        self.lane_offset = (self.lane_offset + 5) % 40
        for y in range(-40, self.height, 40):
            pygame.draw.rect(
                self.screen,
                WHITE,
                (
                    left_bound + self.road_width // 2 - 5,
                    y + self.lane_offset,
                    10,
                    20,
                ),
            )

    # ------------------------------------------------------------------
    def draw(self) -> None:
        """Render all game objects."""

        self.draw_road()
        pygame.draw.rect(self.screen, self.player.color, self.player.rect)
        for car in self.obstacles:
            pygame.draw.rect(self.screen, car.color, car.rect)
        pygame.display.flip()

    # ------------------------------------------------------------------
    def run(self) -> None:
        """Main loop of the game."""

        while self.running:
            self.clock.tick(60)
            self.handle_input()
            self.update_obstacles()
            self.check_collisions()
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    EnduroGame().run()

