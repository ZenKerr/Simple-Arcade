from typing import TYPE_CHECKING

from pygame import Rect, Surface, draw

from app.constants import BACKGROUND_COLOR
from app.screen_manager.screens.menu.level_selector.level import Level
from app.utils import relative_scale

if TYPE_CHECKING:
    from app.data import Data


class LevelSelector:
    __slots__ = ("app_data", "levels", "rect", "surface")

    app_data: "Data"
    levels: tuple[Level, ...]
    rect: Rect
    surface: Surface

    def __init__(self, app_data: "Data"):
        self.app_data = app_data

        size = (app_data.height * 0.3, app_data.height * 0.59)

        self.surface = Surface(size).convert()
        self.rect = self.surface.get_rect(
            topright=(
                app_data.width,
                app_data.height * 0.15,
            )
        )

        level_names = ("inferno", "hard", "classic", "light", "primitive")

        self.levels = tuple(
            Level(app_data, level_name, i) for i, level_name in enumerate(level_names)
        )

        self.redraw()

    def reset(self):
        for level in self.levels:
            level.reset()

    def redraw(self):
        self.surface.fill(BACKGROUND_COLOR)

        title = relative_scale(
            self.app_data.font.render(
                "Difficulty",
                True,
                self.app_data.text_color,
            ),
            0.000165,
            self.app_data,
        )
        self.surface.blit(
            title,
            title.get_rect(
                center=(
                    self.app_data.height * 0.16,
                    self.app_data.height * 0.045,
                ),
            ),
        )

        draw.rect(
            self.surface,
            self.app_data.text_color,
            (
                0,
                0,
                self.app_data.height * 0.4,
                self.app_data.height * 0.59,
            ),
            border_radius=self.app_data.height // 40,
            width=self.app_data.height // 200,
        )

        for level in self.levels:
            level.redraw()

    def update(self):
        for level in self.levels:
            level.update()

    def draw(self, surface: Surface):
        surface.blit(self.surface, self.rect)

        for level in self.levels:
            level.draw(surface)

    def on_click(self):
        for i, level in enumerate(self.levels):
            if level.is_hover:
                match i:
                    case 0:
                        self.app_data.sounds.inferno.play()
                    case 1:
                        self.app_data.sounds.hard.play()
                    case 2:
                        self.app_data.sounds.classic.play()
                    case 3:
                        self.app_data.sounds.light.play()
                    case 4:
                        self.app_data.sounds.primitive.play()

                self.app_data.level = i + 1

                self.app_data.save()

                break
