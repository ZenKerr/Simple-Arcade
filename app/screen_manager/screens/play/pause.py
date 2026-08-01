from typing import TYPE_CHECKING

from pygame import Rect, Surface

from app.utils import relative_scale

if TYPE_CHECKING:
    from app.data import Data


class Pause:
    __slots__ = (
        "app_data",
        "bottom_line_rect",
        "line_surface",
        "text_rect",
        "text_surface",
        "top_line_rect",
    )

    app_data: "Data"
    bottom_line_rect: Rect
    line_surface: Surface
    text_rect: Rect
    text_surface: Surface
    top_line_rect: Rect

    def __init__(self, app_data: "Data"):
        self.app_data = app_data

        self.redraw()
        self.reset()

    def reset(self):
        self.set_alpha(0)

    def redraw(self):
        self.text_surface = relative_scale(
            self.app_data.font.render(
                "Pause",
                True,
                self.app_data.text_color,
            ),
            0.0006,
            self.app_data,
        )
        self.text_rect = self.text_surface.get_rect(
            center=(
                self.app_data.half_width,
                self.app_data.height / 3,
            ),
        )

        self.line_surface = relative_scale(
            self.app_data.font.render(
                "-----",
                True,
                self.app_data.text_color,
            ),
            0.001,
            self.app_data,
        )
        self.top_line_rect = self.line_surface.get_rect(
            center=(
                self.app_data.half_width,
                self.app_data.height / 2.3,
            ),
        )
        self.bottom_line_rect = self.line_surface.get_rect(
            center=(
                self.app_data.half_width,
                self.app_data.height / 3.85,
            ),
        )

        self.set_alpha(1)

    def draw(self, surface: Surface):
        surface.blit(self.text_surface, self.text_rect)
        surface.blit(self.line_surface, self.top_line_rect)
        surface.blit(self.line_surface, self.bottom_line_rect)

    def set_alpha(self, alpha: float):
        alpha = round(alpha)

        self.text_surface.set_alpha(alpha)
        self.line_surface.set_alpha(alpha)
