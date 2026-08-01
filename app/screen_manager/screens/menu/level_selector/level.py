from typing import TYPE_CHECKING

from pygame import Rect, Surface, Vector2, draw

from app.constants import BACKGROUND_COLOR
from app.utils import relative_scale, smooth

if TYPE_CHECKING:
    from app.data import Data


class Level:
    __slots__ = (
        "app_data",
        "is_hover",
        "name",
        "number",
        "previous_is_hover",
        "rect",
        "rect_x",
        "text_rect",
        "text_surface",
    )

    app_data: "Data"
    is_hover: bool
    name: str
    number: int
    previous_is_hover: bool
    rect: Rect
    rect_x: float
    text_rect: Rect
    text_surface: Surface

    def __init__(self, app_data: "Data", name: str, number: int):
        self.app_data = app_data

        self.name = name
        self.number = number

        self.rect_x = self.app_data.width - self.app_data.height * 0.285

        self.rect = Rect(
            self.rect_x,
            self.app_data.height * (0.2325 + 0.1 * self.number),
            self.app_data.height * 0.335,
            self.app_data.height * 0.085,
        )

        self.redraw()

        self.text_rect = self.text_surface.get_rect(
            topleft=(
                self.app_data.width - self.app_data.height * 0.265,
                self.app_data.height * (0.255 + 0.1 * self.number),
            ),
        )

        self.reset()

        if self.check_selected():
            last_rect_x = None

            while self.rect_x != last_rect_x:
                last_rect_x = self.rect_x

                self.update()

    def reset(self):
        self.previous_is_hover = False
        self.is_hover = False

    def redraw(self):
        self.text_surface = relative_scale(
            self.app_data.font.render(
                self.name,
                True,
                self.app_data.text_color,
            ),
            0.00018,
            self.app_data,
        )

    def draw(self, surface: Surface):
        border_radius = self.app_data.height // 40

        draw.rect(
            surface,
            BACKGROUND_COLOR,
            self.rect,
            border_radius=border_radius,
        )
        draw.rect(
            surface,
            self.app_data.text_color,
            self.rect,
            border_radius=border_radius,
            width=self.app_data.height // 200,
        )

        surface.blit(self.text_surface, self.text_rect)

    def update(self):
        if self.is_hover and not self.previous_is_hover:
            self.app_data.sounds.hover.play()

        width = 0.3125 if self.check_selected() else 0.29875 if self.is_hover else 0.285
        target_x = self.app_data.width - self.app_data.height * width

        self.rect_x = smooth(target_x, self.rect_x, 1)

        self.rect.x = int(self.rect_x)
        self.text_rect.topleft = (
            round(self.rect_x + self.app_data.height * 0.02),
            self.rect.y + (self.rect.height - self.text_rect.height) // 2,
        )

        self.previous_is_hover = self.is_hover

    def set_hover(self, mouse_position: Vector2):
        self.is_hover = self.check_hover(mouse_position)

    def check_hover(self, mouse_position: Vector2) -> bool:
        return self.rect.collidepoint(mouse_position)

    def check_selected(self) -> bool:
        return self.app_data.level - 1 == self.number
