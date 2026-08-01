from typing import TYPE_CHECKING

from pygame import Rect, Surface

from app.utils import relative_scale

if TYPE_CHECKING:
    from app.data import Data


class Hint:
    __slots__ = (
        "app_data",
        "delimiter_rect",
        "delimiter_surface",
        "left_rect",
        "left_surface",
        "left_text",
        "right_rect",
        "right_surface",
        "right_text",
        "y",
    )

    app_data: "Data"
    delimiter_rect: Rect
    delimiter_surface: Surface
    left_rect: Rect
    left_surface: Surface
    left_text: str
    right_rect: Rect
    right_surface: Surface
    right_text: str
    y: float

    def __init__(self, app_data: "Data", left_text: str, right_text: str, y: float):
        self.app_data = app_data

        self.left_text = left_text
        self.right_text = right_text
        self.y = y

    def redraw(self):
        self.delimiter_surface = relative_scale(
            self.app_data.font.render(
                "-",
                True,
                self.app_data.text_color,
            ),
            0.0002,
            self.app_data,
        )
        self.left_surface = relative_scale(
            self.app_data.font.render(
                self.left_text,
                True,
                self.app_data.text_color,
            ),
            0.0002,
            self.app_data,
        )
        self.right_surface = relative_scale(
            self.app_data.font.render(
                self.right_text,
                True,
                self.app_data.text_color,
            ),
            0.0002,
            self.app_data,
        )

        text_x_offset = self.app_data.height * 0.0175

        self.delimiter_rect = self.delimiter_surface.get_rect(
            center=(
                self.app_data.half_width,
                self.y,
            ),
        )
        self.left_rect = self.left_surface.get_rect(
            midright=(
                self.delimiter_rect.left - text_x_offset,
                self.y,
            ),
        )
        self.right_rect = self.right_surface.get_rect(
            midleft=(
                self.delimiter_rect.right + text_x_offset,
                self.y,
            ),
        )

    def draw(self, surface: Surface):
        surface.blit(self.delimiter_surface, self.delimiter_rect)
        surface.blit(self.left_surface, self.left_rect)
        surface.blit(self.right_surface, self.right_rect)
