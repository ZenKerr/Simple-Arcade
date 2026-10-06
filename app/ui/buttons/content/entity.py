from collections.abc import Callable
from math import cos, sin, tau
from typing import TYPE_CHECKING

from pygame import Surface, Vector2

from app.entities import Tail
from app.types import ColorSource
from app.ui.buttons.content import ButtonContent

if TYPE_CHECKING:
    from app.services.app_data import AppData


class EntityButtonContent(ButtonContent):
    __slots__ = (
        "app_data",
        "counter",
        "position",
        "radius",
        "tail",
    )

    app_data: "AppData"
    counter: float
    position: Vector2
    radius: float
    tail: Tail

    def __init__(
        self,
        app_data: "AppData",
        get_color_source: Callable[[], ColorSource],
        width: float,
        height: float,
    ):
        self.app_data = app_data

        self.tail = Tail(
            app_data,
            get_color_source,
            app_data.height * 0.014,
        )
        self.counter = 0
        self.position = Vector2(width, height) * self.app_data.half_height
        self.radius = self.position.x / 2

        while self.counter < tau * 0.75:
            self.update()

    def update(self):
        self.counter = (self.counter + 0.075) % tau

        self.tail.update(
            0.5,
            True,
            self.position + self.radius * Vector2(cos(self.counter), sin(self.counter)),
        )

    def draw(self, surface: Surface, size: Vector2):
        self.tail.draw(surface)
