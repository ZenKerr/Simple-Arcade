from typing import TYPE_CHECKING

from pygame import Surface, Vector2

from app.screen_manager.screens.custom.color_selector.part import (
    ColorSelectorPart,
    ColorSelectorPartColor,
)
from app.screen_manager.screens.custom.custom_screen_target import CustomScreenTarget
from app.scroll_direction import ScrollDirection
from app.types import Colors, ColorSource
from app.utils import get_mouse_position

if TYPE_CHECKING:
    from app.data import Data


class ColorSelector[T: ColorSource]:
    __slots__ = ("app_data", "colors", "parts", "target")

    app_data: "Data"
    colors: tuple[tuple[tuple[int, T], ...], ...]
    parts: tuple[ColorSelectorPart[T], ...]
    target: CustomScreenTarget

    def __init__(self, app_data: "Data", colors: Colors[T], target: CustomScreenTarget):
        self.app_data = app_data

        self.target = target

        levels = tuple(sorted({price for price, _ in colors}))

        self.colors = tuple(
            tuple(
                (i, color) for i, (price, color) in enumerate(colors) if price == level
            )
            for level in levels
        )

        match self.target:
            case CustomScreenTarget.PLAYER:
                unlock_list = self.app_data.unlock_player_colors
                get_selected_index = lambda: self.app_data.player_color_index
            case CustomScreenTarget.ENEMY:
                unlock_list = self.app_data.unlock_enemy_colors
                get_selected_index = lambda: self.app_data.enemy_color_index
            case CustomScreenTarget.INTERFACE:
                unlock_list = self.app_data.unlock_text_colors
                get_selected_index = lambda: self.app_data.text_color_index

        self.parts = tuple(
            ColorSelectorPart(
                app_data,
                f"Level {i + 1}",
                f"Price {levels[i]}$",
                colors,
                unlock_list,
                get_selected_index,
                Vector2(
                    app_data.height * 0.3,
                    app_data.height * 0.155
                    + app_data.height * 0.15 * i
                    + app_data.height * self.target,
                ),
                levels[i],
            )
            for i, colors in enumerate(self.colors)
        )

    def update(
        self,
        selected_target: CustomScreenTarget,
        scroll_direction: ScrollDirection,
        click: bool,
    ) -> ColorSelectorPartColor | None:
        mouse_position = get_mouse_position()

        selected = None
        for i, part in enumerate(self.parts):
            selected = selected or part.update(
                mouse_position,
                self.target,
                selected_target,
                i,
                scroll_direction,
                click,
            )

        return selected

    def redraw(self):
        for part in self.parts:
            part.redraw()

    def draw(self, surface: Surface):
        for part in self.parts:
            part.draw(surface)
