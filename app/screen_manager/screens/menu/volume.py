from typing import TYPE_CHECKING

from pygame import Rect, Surface, draw, mouse

from app.constants import BACKGROUND_COLOR
from app.utils import get_mouse_position

if TYPE_CHECKING:
    from app.data import Data


class Volume:
    __slots__ = ("app_data", "inner_surface", "previous_clicked", "rect", "surface")

    app_data: "Data"
    inner_surface: Surface
    previous_clicked: bool
    rect: Rect
    surface: Surface

    def __init__(self, app_data: "Data"):
        self.app_data = app_data

        size = (app_data.height * 0.05, app_data.half_height)

        self.surface = Surface(size).convert_alpha()
        self.inner_surface = Surface(size).convert()

        self.rect = self.surface.get_rect(
            topleft=(
                app_data.height * 0.02,
                app_data.height * 0.25,
            )
        )

        self.reset()

    def reset(self):
        self.previous_clicked = False

    def redraw(self):
        self.surface.fill(BACKGROUND_COLOR)
        self.inner_surface.fill(BACKGROUND_COLOR)

        width = self.app_data.height * 0.05
        border_radius = self.app_data.height // 40

        draw.rect(
            self.surface,
            (0, 0, 0, 0),
            (
                0,
                0,
                width,
                self.app_data.half_height,
            ),
            border_radius=border_radius,
        )
        draw.rect(
            self.surface,
            self.app_data.text_color,
            (
                0,
                0,
                width,
                self.app_data.half_height,
            ),
            border_radius=border_radius,
            width=self.app_data.height // 200,
        )
        draw.rect(
            self.inner_surface,
            self.app_data.text_color,
            (
                0,
                self.app_data.half_height * (1 - self.app_data.sounds.volume),
                width,
                self.app_data.half_height * self.app_data.sounds.volume,
            ),
            border_radius=border_radius,
        )

    def draw(self, surface: Surface):
        surface.blit(self.inner_surface, self.rect)
        surface.blit(self.surface, self.rect)

    def update(self):
        pressed_buttons = mouse.get_pressed()

        if pressed_buttons[0] or pressed_buttons[2]:
            mouse_position = get_mouse_position()

            if self.rect.collidepoint(mouse_position):
                self.previous_clicked = True

                corrected_mouse_y = mouse_position.y - self.app_data.height * 0.25
                volume = 1 - corrected_mouse_y / self.app_data.half_height

                self.app_data.sounds.set_volume(volume)

                self.redraw()
            elif self.previous_clicked:
                self.app_data.sounds.action.play()

                self.previous_clicked = False
        elif self.previous_clicked:
            self.app_data.sounds.action.play()

            self.previous_clicked = False
