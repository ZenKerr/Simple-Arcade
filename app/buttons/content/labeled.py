from typing import TYPE_CHECKING

from pygame import Surface, Vector2

from app.buttons.content import ButtonContent
from app.utils import relative_scale

if TYPE_CHECKING:
    from app.data import Data


class LabeledButtonContent[T: ButtonContent](ButtonContent):
    __slots__ = ("app_data", "content", "label")

    app_data: "Data"
    content: T
    label: str

    def __init__(self, app_data: "Data", content: T, label: str):
        self.app_data = app_data

        self.content = content
        self.label = label

    def update(self):
        self.content.update()

    def draw(self, surface: Surface, size: Vector2):
        text = relative_scale(
            self.app_data.font.render(
                self.label,
                True,
                self.app_data.text_color,
            ),
            0.00014,
            self.app_data,
        )
        surface.blit(
            text,
            text.get_rect(
                center=Vector2(size.x / 2, size.y * 0.15) * self.app_data.height,
            ),
        )

        self.content.draw(surface, Vector2(size.x, size.y * 1.15))
