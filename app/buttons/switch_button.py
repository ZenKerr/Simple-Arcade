from collections.abc import Callable
from enum import ReprEnum
from typing import TYPE_CHECKING

from pygame import Vector2

from app.buttons import Button
from app.buttons.content import ButtonContent

if TYPE_CHECKING:
    from app.data import Data


class SwitchButton[T: ButtonContent, U: ReprEnum](Button[T]):
    __slots__ = ("get_target", "value")

    get_target: Callable[[], U]
    value: U

    def __init__(
        self,
        app_data: "Data",
        content: T,
        position: Vector2,
        size: Vector2,
        value: U,
        get_target: Callable[[], U],
    ):
        super().__init__(app_data, content, position, size)

        self.value = value
        self.get_target = get_target

    def reset(self):
        super().reset()

        if self.check_selected():
            self.scale = 1.1

            self.redraw()
            self.rect = self.surface.get_rect(center=self.position)

    def check_selected(self) -> bool:
        return self.value == self.get_target()

    def scale_target(self) -> float:
        return 1.1 if self.check_selected() else 1.05 if self.is_hover else 1.0
