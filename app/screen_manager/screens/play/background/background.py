from typing import TYPE_CHECKING

from pygame import Surface

from app.screen_manager.screens.play.background.layer import Layer

if TYPE_CHECKING:
    from app.data import Data
    from app.entities import Player


class Background:
    __slots__ = ("layers",)

    layers: tuple[Layer, ...]

    def __init__(self, app_data: "Data", player: "Player"):
        parallax_coefficients = (0.2, 0.225, 0.25, 0.275, 0.3)

        self.layers = tuple(
            Layer(
                app_data,
                player,
                parallax_coefficient,
                len(parallax_coefficients),
            )
            for parallax_coefficient in parallax_coefficients
        )

    def reset(self):
        for layer in self.layers:
            layer.reset()

    def draw(self, surface: Surface):
        for layer in self.layers:
            layer.draw(surface)
