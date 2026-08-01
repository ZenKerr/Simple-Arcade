from typing import TYPE_CHECKING

import pygame
from pygame import Surface
from pygame import key as keys
from pygame.math import Vector2, clamp

from app.entities.tail import Tail

if TYPE_CHECKING:
    from app.data import Data
    from app.screen_manager.screens import PlayScreen


class Player:
    __slots__ = (
        "app_data",
        "play_screen",
        "position",
        "radius",
        "speed",
        "tail",
    )

    app_data: "Data"
    play_screen: "PlayScreen"
    position: Vector2
    radius: float
    speed: float
    tail: Tail

    def __init__(self, app_data: "Data", play_screen: "PlayScreen"):
        self.app_data = app_data
        self.play_screen = play_screen

        self.radius = app_data.height * 0.014
        self.speed = app_data.height * 0.01
        self.tail = Tail(app_data, lambda: app_data.player_color, self.radius)

        self.reset()

    def reset(self):
        self.position = self.app_data.half_size

        self.tail.reset(self.position)

    def update(self):
        pressed_keys = keys.get_pressed()
        right = pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]
        left = pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]
        down = pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]
        up = pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]

        speed = Vector2(right - left, down - up)
        moving = speed.length_squared() > 0

        if moving:
            speed = speed.normalize() * self.speed * self.play_screen.time_coefficient

            self.position = Vector2(
                clamp(
                    self.position.x + speed.x,
                    self.radius,
                    self.app_data.width - self.radius,
                ),
                clamp(
                    self.position.y + speed.y,
                    self.radius,
                    self.app_data.height - self.radius,
                ),
            )

        self.tail.update(self.play_screen.time_coefficient, moving, self.position)

    def draw(self, surface: Surface):
        self.tail.draw(surface)
