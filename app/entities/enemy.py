from random import choice, uniform
from typing import TYPE_CHECKING

from pygame import Surface, Vector2

from app.entities.tail import Tail

if TYPE_CHECKING:
    from app.data import Data


class Enemy:
    __slots__ = (
        "app_data",
        "position",
        "radius",
        "speed",
        "stopped",
        "tail",
        "wait_delete",
    )

    app_data: "Data"
    position: Vector2
    radius: float
    speed: Vector2
    stopped: bool
    tail: Tail
    wait_delete: bool

    def __init__(self, app_data: "Data", target: Vector2):
        self.app_data = app_data

        self.radius = uniform(app_data.height * 0.01, app_data.height * 0.02)

        half_radius = self.radius / 2
        spawn_x = uniform(0, app_data.width)
        spawn_y = uniform(0, app_data.height)

        self.position = choice(
            (
                Vector2(-half_radius, spawn_y),
                Vector2(app_data.width + half_radius, spawn_y),
                Vector2(spawn_x, -half_radius),
                Vector2(spawn_x, app_data.height + half_radius),
            ),
        )

        target_spread = app_data.height * 0.2
        spread_vector = Vector2(
            uniform(-target_spread, target_spread),
            uniform(-target_spread, target_spread),
        )

        self.speed = (
            (target - self.position + spread_vector).normalize()
            * app_data.height
            * 0.015
        )

        color = app_data.enemy_color()
        self.tail = Tail(app_data, lambda: color, self.radius)

        self.stopped = False
        self.wait_delete = False

    def update(self, alpha_normalize: float):
        moving = not self.stopped

        if moving:
            self.position += self.speed * alpha_normalize

            bound_rect = self.app_data.display_rect.inflate(
                self.radius * 2,
                self.radius * 2,
            )

            if not bound_rect.collidepoint(self.position):
                self.stopped = True
        elif not len(self.tail):
            self.wait_delete = True

        self.tail.update(alpha_normalize, moving, self.position)

    def draw(self, surface: Surface):
        self.tail.draw(surface)
