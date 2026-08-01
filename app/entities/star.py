from random import randint
from typing import TYPE_CHECKING, cast

from pygame import Surface, Vector2, draw

from app.types import Color
from app.utils import smooth

if TYPE_CHECKING:
    from app.data import Data


class Star:
    __slots__ = ("app_data", "color", "position", "radius", "speed")

    app_data: "Data"
    color: Color
    position: Vector2
    radius: float
    speed: Vector2

    def __init__(
        self,
        app_data: "Data",
        size_coefficient: float,
        position: Vector2,
        speed: Vector2,
    ):
        self.app_data = app_data

        self.position = position
        self.speed = speed

        radius = self.app_data.height / 1000 * size_coefficient * 1.5

        self.color = cast(Color, tuple(randint(156, 236) for _ in range(3)))
        self.radius = max(radius, 1)

    def update(self):
        self.position += self.speed

        self.speed.update(
            smooth(0, self.speed.x, 0.0001),
            smooth(0, self.speed.y, 0.0001),
        )

    def draw(self, surface: Surface, offset: Vector2):
        draw.circle(surface, self.color, self.position + offset, self.radius)
