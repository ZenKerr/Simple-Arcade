from typing import TYPE_CHECKING

from pygame import Surface, Vector2, draw

from app.types import Color, ColorSource
from app.utils import get_color

if TYPE_CHECKING:
    from app.data import Data


class TailSegment:
    __slots__ = ("app_data", "color_source", "position", "radius")

    app_data: "Data"
    color_source: Color
    position: Vector2
    radius: float

    def __init__(
        self,
        app_data: "Data",
        radius: float,
        position: Vector2,
        color_source: ColorSource,
    ):
        self.app_data = app_data

        self.radius = radius
        self.position = position.copy()
        self.color_source = get_color(color_source)

    def update(self, fade_rate: float) -> bool:
        if self.radius < 1:
            return True
        else:
            self.radius -= fade_rate

            return False

    def draw(self, surface: Surface):
        if self.app_data.display_rect.collidepoint(self.position):
            draw.circle(surface, self.color_source, self.position, self.radius)
