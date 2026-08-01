from typing import TYPE_CHECKING

from pygame import Rect, Surface, Vector2, draw, transform

from app.buttons.content import ButtonContent
from app.constants import BACKGROUND_COLOR
from app.utils import smooth

if TYPE_CHECKING:
    from app.data import Data


class Button[T: ButtonContent]:
    __slots__ = (
        "app_data",
        "content",
        "is_hover",
        "position",
        "previous_is_hover",
        "rect",
        "scale",
        "size",
        "source_surface",
        "surface",
    )

    app_data: "Data"
    content: T
    is_hover: bool
    position: Vector2
    previous_is_hover: bool
    rect: Rect
    scale: float
    size: Vector2
    source_surface: Surface
    surface: Surface

    def __init__(
        self,
        app_data: "Data",
        content: T,
        position: Vector2,
        size: Vector2 | None = None,
    ):
        self.app_data = app_data

        self.content = content
        self.position = position
        self.size = Vector2(0.55, 0.09) if size is None else size

        self.scale = 1

        self.redraw()

        self.surface = self.source_surface

    def reset(self):
        self.scale = 1
        self.previous_is_hover = False
        self.is_hover = False

        self.surface = transform.scale(
            self.source_surface,
            self.source_surface.get_size(),
        )
        self.rect = self.surface.get_rect(center=self.position)

    def redraw(self):
        source_surface_size = self.size * self.app_data.height

        self.source_surface = Surface(source_surface_size).convert()
        self.source_surface.fill(BACKGROUND_COLOR)

        draw.rect(
            self.source_surface,
            self.app_data.text_color,
            (
                0,
                0,
                source_surface_size.x,
                source_surface_size.y,
            ),
            border_radius=self.app_data.height // 40,
            width=self.app_data.height // 200,
        )

        self.content.draw(self.source_surface, self.size)

        self.surface = transform.scale(
            self.source_surface,
            source_surface_size * self.scale,
        )

    def draw(self, surface: Surface):
        surface.blit(self.surface, self.rect)

    def update(self):
        if self.is_hover and not self.previous_is_hover:
            self.app_data.sounds.hover.play()

        self.scale = smooth(self.scale_target(), self.scale, 0.005)

        self.surface = transform.scale(
            self.source_surface,
            Vector2(self.source_surface.get_size()) * self.scale,
        )
        self.rect = self.surface.get_rect(center=self.position)

        self.previous_is_hover = self.is_hover

        self.content.update()

    def set_hover(self, mouse_position: Vector2):
        self.is_hover = self.check_hover(mouse_position)

    def check_hover(self, mouse_position: Vector2) -> bool:
        return self.rect.collidepoint(mouse_position)

    def scale_target(self) -> float:
        return 1.1 if self.is_hover else 1.0
