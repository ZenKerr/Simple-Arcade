from collections.abc import Callable
from typing import TYPE_CHECKING

from pygame import Surface, Vector2, draw

from app.constants import BACKGROUND_COLOR
from app.screen_manager.screens.custom.color_selector.part.color import (
    ColorSelectorPartColor,
)
from app.scroll_direction import ScrollDirection
from app.types import Colors, ColorSource
from app.utils import relative_scale, smooth

if TYPE_CHECKING:
    from app.data import Data
    from app.screen_manager.screens.custom import CustomScreenTarget


class ColorSelectorPart[T: ColorSource]:
    __slots__ = (
        "app_data",
        "colors",
        "cost",
        "get_selected_index",
        "level",
        "level_text",
        "position",
        "previous_click",
        "price",
        "price_text",
        "start_click",
        "surface",
        "unlock_list",
    )

    app_data: "Data"
    colors: tuple[ColorSelectorPartColor[T], ...]
    cost: int
    get_selected_index: Callable[[], int]
    level: Surface
    level_text: str
    position: Vector2
    previous_click: int | None
    price: Surface
    price_text: str
    start_click: int
    surface: Surface
    unlock_list: list[bool]

    def __init__(
        self,
        app_data: "Data",
        level_text: str,
        price_text: str,
        colors: Colors[T],
        unlock_list: list[bool],
        get_selected_index: Callable[[], int],
        position: Vector2,
        cost: int,
    ):
        self.app_data = app_data

        self.level_text = level_text
        self.price_text = price_text
        self.unlock_list = unlock_list
        self.get_selected_index = get_selected_index
        self.position = position
        self.cost = cost

        width = int(app_data.width - app_data.height * 0.32)
        height = int(app_data.height * 0.1)

        self.surface = Surface((width, height)).convert()
        self.previous_click = None
        self.start_click = -1

        padding = app_data.height * 0.05
        color_width = app_data.height * 0.06475

        visible_item_number = int((width - padding * 2) / color_width)
        max_scroll = color_width * (len(colors) - visible_item_number - 2)

        self.colors = tuple(
            ColorSelectorPartColor(
                app_data,
                index,
                color,
                unlock_list,
                get_selected_index,
                padding + color_width * i,
                padding + color_width * i - max(0, max_scroll),
            )
            for i, (index, color) in enumerate(colors)
        )

        self.redraw()

    def redraw(self):
        self.level = relative_scale(
            self.app_data.font.render(
                self.level_text,
                True,
                self.app_data.text_color,
            ),
            0.00015,
            self.app_data,
        )
        self.price = relative_scale(
            self.app_data.font.render(
                self.price_text,
                True,
                self.app_data.text_color,
            ),
            0.00015,
            self.app_data,
        )

    def update(
        self,
        mouse_position: Vector2,
        target_number: int,
        selected_target: "CustomScreenTarget",
        part_number: int,
        scroll_direction: ScrollDirection,
        click: bool,
    ) -> ColorSelectorPartColor[T] | None:
        position = (
            self.app_data.height * 0.155
            + self.app_data.height * 0.15 * part_number
            + self.app_data.height * target_number
            - self.app_data.height * selected_target
        )

        selected = None
        if position < mouse_position.y < position + int(self.app_data.height * 0.1):
            offset = scroll_direction * self.app_data.height * 0.1
            from_y = self.app_data.height * 0.3
            to_y = self.app_data.width - self.app_data.height * 0.02

            if click and from_y < mouse_position.x < to_y:
                if self.start_click == -1:
                    self.start_click = int(mouse_position.x)
                elif self.previous_click is not None:
                    offset += mouse_position.x - self.previous_click

                self.previous_click = int(mouse_position.x)
            else:
                if not (mouse_position.x - self.start_click):
                    for color in self.colors:
                        if color.check_click(mouse_position):
                            if not self.unlock_list[color.index]:
                                if self.cost <= self.app_data.money:
                                    self.app_data.sounds.buy.play()

                                    self.app_data.money -= self.cost
                                    self.unlock_list[color.index] = True

                                    selected = color
                                else:
                                    self.app_data.sounds.error.play()
                            elif self.get_selected_index() != color.index:
                                self.app_data.sounds.action.play()

                                selected = color

                            break

                self.previous_click = None
                self.start_click = -1

            for color in self.colors:
                color.update(offset)
        else:
            self.previous_click = None
            self.start_click = -1

        self.position.y = smooth(position, self.position.y, 0.5)

        return selected

    def draw(self, surface: Surface):
        self.surface.fill(BACKGROUND_COLOR)
        for color in self.colors:
            color.draw(self.surface)

        draw.rect(
            self.surface,
            self.app_data.text_color,
            (
                0,
                0,
                self.surface.get_width(),
                self.surface.get_height(),
            ),
            border_radius=self.app_data.height // 40,
            width=self.app_data.height // 200,
        )
        surface.blit(self.surface, self.position)

        text_y = self.position.y - self.app_data.height * 0.042

        surface.blit(
            self.level,
            self.level.get_rect(topleft=(self.app_data.height * 0.33, text_y)),
        )
        surface.blit(
            self.price,
            self.price.get_rect(topright=(self.app_data.width * 0.97, text_y)),
        )
