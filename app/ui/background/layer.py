from random import uniform
from typing import TYPE_CHECKING

from pygame import Surface, Vector2

from app.entities import Star
from app.entities.groups import Stars

if TYPE_CHECKING:
    from app.entities import Player
    from app.services.app_data import AppData


class Layer:
    __slots__ = (
        "app_data",
        "layers_number",
        "parallax_coefficient",
        "player",
        "screen_size_coefficient",
        "stars",
    )

    app_data: "AppData"
    layers_number: int
    parallax_coefficient: float
    player: "Player"
    screen_size_coefficient: float
    stars: Stars

    def __init__(
        self,
        app_data: "AppData",
        player: "Player",
        parallax_coefficient: float,
        layers_number: int,
    ):
        self.app_data = app_data
        self.player = player

        self.parallax_coefficient = parallax_coefficient
        self.layers_number = layers_number
        self.stars = Stars()

        self.screen_size_coefficient = 1 + parallax_coefficient

        self.reset()

    def reset(self):
        self.stars.reset()

        for _ in range(350 // self.layers_number):
            position = Vector2(
                uniform(0, self.app_data.width),
                uniform(0, self.app_data.height),
            )

            self.stars.add(
                Star(
                    self.app_data,
                    self.screen_size_coefficient,
                    position * self.screen_size_coefficient,
                    Vector2(0),
                )
            )

    def draw(self, surface: Surface):
        offset = -self.player.position * self.parallax_coefficient

        self.stars.draw(surface, offset)
