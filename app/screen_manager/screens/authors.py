from math import cos
from platform import python_version
from sys import exit
from typing import TYPE_CHECKING

import pygame
import PyInstaller
from pygame import Rect, Surface, Vector2, display
from pygame import event as events

from app.buttons import Button
from app.buttons.content import BackButtonContent
from app.constants import BACKGROUND_COLOR, FPS
from app.screen_manager.screens import Screen
from app.utils import relative_scale

if TYPE_CHECKING:
    from app.data import Data


class AuthorsScreen(Screen):
    __slots__ = (
        "app_data",
        "back_button",
        "code_author",
        "code_rect",
        "logo",
        "logo_position_coefficient",
        "logo_rect",
        "music_author",
        "pygame_version",
        "pygame_version_rect",
        "pyinstaller_version",
        "pyinstaller_version_rect",
        "python_version",
        "python_version_rect",
        "sound_rect",
    )

    app_data: "Data"
    back_button: Button
    code_author: Surface
    code_rect: Rect
    logo: Surface
    logo_position_coefficient: float
    logo_rect: Rect
    music_author: Surface
    pygame_version: Surface
    pygame_version_rect: Rect
    pyinstaller_version: Surface
    pyinstaller_version_rect: Rect
    python_version: Surface
    python_version_rect: Rect
    sound_rect: Rect

    def __init__(self, app_data: "Data"):
        self.app_data = app_data

        self.logo_position_coefficient = 1.25

        self.back_button = Button(
            app_data,
            BackButtonContent(app_data),
            Vector2(app_data.height * 0.12, app_data.height * 0.055),
            Vector2(0.2, 0.07),
        )

        self.redraw()

        self.code_rect = self.code_author.get_rect(
            center=(
                self.app_data.half_width,
                self.app_data.height / 2,
            ),
        )
        self.sound_rect = self.music_author.get_rect(
            center=(
                self.app_data.half_width,
                self.app_data.height / 1.7,
            ),
        )

        versions_x = self.app_data.width - self.app_data.height * 0.0075

        self.pygame_version_rect = self.pygame_version.get_rect(
            topright=(
                versions_x,
                self.app_data.height * 0.91,
            ),
        )
        self.python_version_rect = self.python_version.get_rect(
            topright=(
                versions_x,
                self.app_data.height * 0.94,
            ),
        )
        self.pyinstaller_version_rect = self.pyinstaller_version.get_rect(
            topright=(
                versions_x,
                self.app_data.height * 0.97,
            ),
        )

        self.logo = relative_scale(
            app_data.assets.get_image("studio_logo.png").convert_alpha(),
            0.0004,
            app_data,
        )
        self.logo_rect = self.logo.get_rect(
            center=(
                self.app_data.half_width,
                self.calculate_logo_y(),
            )
        )

        self.reset()

    def reset(self):
        self.back_button.reset()

    def redraw(self):
        self.back_button.redraw()

        self.code_author = relative_scale(
            self.app_data.font.render(
                "Code & Design: Ivan Sarnitskii",
                True,
                self.app_data.text_color,
            ),
            0.0002,
            self.app_data,
        )
        self.music_author = relative_scale(
            self.app_data.font.render(
                "Music & Sound: Another guy",
                True,
                self.app_data.text_color,
            ),
            0.0002,
            self.app_data,
        )

        self.pygame_version = relative_scale(
            self.app_data.font.render(
                f"PyGame: {pygame.version.ver}",
                True,
                self.app_data.text_color,
            ),
            0.0001,
            self.app_data,
        )
        self.python_version = relative_scale(
            self.app_data.font.render(
                f"Python: {python_version()}",
                True,
                self.app_data.text_color,
            ),
            0.0001,
            self.app_data,
        )
        self.pyinstaller_version = relative_scale(
            self.app_data.font.render(
                f"PyInstaller: {PyInstaller.__version__}",
                True,
                self.app_data.text_color,
            ),
            0.0001,
            self.app_data,
        )

    def draw(self, surface: Surface):
        surface.fill(BACKGROUND_COLOR)

        self.back_button.draw(surface)

        surface.blit(self.code_author, self.code_rect)
        surface.blit(self.music_author, self.sound_rect)

        surface.blit(self.pygame_version, self.pygame_version_rect)
        surface.blit(self.python_version, self.python_version_rect)
        surface.blit(self.pyinstaller_version, self.pyinstaller_version_rect)

        surface.blit(self.logo, self.logo_rect)

    def run(self) -> tuple[Screen, bool]:
        while True:
            for event in events.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEMOTION:
                    self.back_button.set_hover(Vector2(event.pos))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (event.button in (1, 3)) and self.back_button.check_hover(
                        Vector2(event.pos)
                    ):
                        return self.app_data.screen_manager.menu, False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return self.app_data.screen_manager.menu, False

            self.back_button.update()

            self.logo_position_coefficient += 0.0025
            self.logo_rect.centery = self.calculate_logo_y()

            self.draw(self.app_data.display_surface)

            display.update()

            self.app_data.clock.tick(FPS)

    def calculate_logo_y(self) -> int:
        offset = self.app_data.height * cos(self.logo_position_coefficient) / 20

        return int(self.app_data.height * 0.23 + offset)
