from collections.abc import Callable
from typing import TYPE_CHECKING

from pygame import Surface, Vector2, draw

from app.types import ColorSource
from app.utils import get_color

if TYPE_CHECKING:
    from app.data import Data


class ColorSelectorPartColor[T: ColorSource]:
    __slots__ = (
        "app_data",
        "color",
        "get_selected_index",
        "index",
        "max_x",
        "min_x",
        "unlock_list",
        "x",
    )

    app_data: "Data"
    color: T
    get_selected_index: Callable[[], int]
    index: int
    max_x: float
    min_x: float
    unlock_list: list[bool]
    x: float

    def __init__(
        self,
        app_data: "Data",
        index: int,
        color: T,
        unlock_list: list[bool],
        get_selected_index: Callable[[], int],
        x: float,
        min_x: float,
    ):
        self.app_data = app_data

        self.index = index
        self.color = color
        self.unlock_list = unlock_list
        self.get_selected_index = get_selected_index
        self.x = x
        self.min_x = min_x
        self.max_x = x

    def update(self, offset: float):
        self.x = max(min(self.x + offset, self.max_x), self.min_x)

    def draw(self, surface: Surface):
        position = (self.x, self.app_data.height * 0.05)

        if not self.unlock_list[self.index]:
            draw.circle(
                surface,
                (255, 0, 0),
                position,
                self.app_data.height * 0.03,
            )

        if self.x + self.app_data.height * 0.03 > 0:
            if self.index == self.get_selected_index():
                draw.circle(
                    surface,
                    (255, 255, 255),
                    position,
                    self.app_data.height * 0.03,
                )

            draw.circle(
                surface,
                get_color(self.color),
                position,
                self.app_data.height * 0.025,
            )

    def check_click(self, mouse_position: Vector2) -> bool:
        radius = self.app_data.height * 0.025
        corrected_mouse_x = mouse_position.x - self.app_data.height * 0.30

        return self.x - radius < corrected_mouse_x < self.x + radius
