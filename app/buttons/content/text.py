from typing import TYPE_CHECKING

from pygame import Surface, Vector2

from app.buttons.content import ButtonContent
from app.utils import relative_scale

if TYPE_CHECKING:
    from app.data import Data


class TextButtonContent(ButtonContent):
    __slots__ = ("app_data", "font_size", "text")

    app_data: "Data"
    font_size: float
    text: str

    def __init__(self, app_data: "Data", text: str, font_size: float = 0.0002):
        self.app_data = app_data

        self.text = text
        self.font_size = font_size

    def update(self):
        pass

    def draw(self, surface: Surface, size: Vector2):
        text = relative_scale(
            self.app_data.font.render(
                self.text,
                True,
                self.app_data.text_color,
            ),
            self.font_size,
            self.app_data,
        )
        surface.blit(
            text,
            text.get_rect(center=size * self.app_data.half_height),
        )
