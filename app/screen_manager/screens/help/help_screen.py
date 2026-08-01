from sys import exit
from typing import TYPE_CHECKING

import pygame
from pygame import Rect, Surface, Vector2, display, draw
from pygame import event as events

from app.buttons import Button
from app.buttons.content import BackButtonContent
from app.constants import BACKGROUND_COLOR, FPS
from app.screen_manager.screens import Screen
from app.screen_manager.screens.help.hint import Hint
from app.utils import relative_scale

if TYPE_CHECKING:
    from app.data import Data


class HelpScreen(Screen):
    __slots__ = (
        "all_back_hint",
        "all_title",
        "all_title_rect",
        "app_data",
        "back_button",
        "menu_customization_hint",
        "menu_exit_hint",
        "menu_help_hint",
        "menu_play_hint",
        "menu_title",
        "menu_title_rect",
        "play_arrows",
        "play_arrows_rect",
        "play_move_hint",
        "play_pause_hint",
        "play_title",
        "play_title_rect",
        "play_w_a_s_d",
        "play_w_a_s_d_rect",
    )

    all_back_hint: Hint
    all_title: Surface
    all_title_rect: Rect
    app_data: "Data"
    back_button: Button
    menu_customization_hint: Hint
    menu_exit_hint: Hint
    menu_help_hint: Hint
    menu_play_hint: Hint
    menu_title: Surface
    menu_title_rect: Rect
    play_arrows: Surface
    play_arrows_rect: Rect
    play_move_hint: Hint
    play_pause_hint: Hint
    play_title: Surface
    play_title_rect: Rect
    play_w_a_s_d: Surface
    play_w_a_s_d_rect: Rect

    def __init__(self, app_data: "Data"):
        self.app_data = app_data

        self.back_button = Button(
            app_data,
            BackButtonContent(app_data),
            Vector2(self.app_data.height * 0.12, self.app_data.height * 0.055),
            Vector2(0.2, 0.07),
        )

        self.menu_play_hint = Hint(
            app_data,
            "SPACE OR ENTER",
            "Play",
            self.app_data.height * 0.15,
        )
        self.menu_customization_hint = Hint(
            app_data,
            "BACKSPACE",
            "Customization",
            self.app_data.height * 0.21,
        )
        self.menu_exit_hint = Hint(app_data, "ESC", "Exit", self.app_data.height * 0.27)
        self.menu_help_hint = Hint(app_data, "H", "Help", self.app_data.height * 0.33)
        self.play_pause_hint = Hint(
            app_data,
            "SPACE OR ESC",
            "Pause",
            self.app_data.height * 0.54,
        )
        self.play_move_hint = Hint(app_data, "OR", "Move", self.app_data.height * 0.66)
        self.all_back_hint = Hint(
            app_data,
            "ESC",
            "Back",
            self.app_data.height * 0.9225,
        )

        self.redraw()
        self.reset()

    def reset(self):
        self.back_button.reset()

    def redraw(self):
        self.back_button.redraw()

        self.menu_play_hint.redraw()
        self.menu_customization_hint.redraw()
        self.menu_exit_hint.redraw()
        self.menu_help_hint.redraw()
        self.play_pause_hint.redraw()
        self.play_move_hint.redraw()
        self.all_back_hint.redraw()

        self.menu_title = relative_scale(
            self.app_data.font.render(
                "Menu Screen",
                True,
                self.app_data.text_color,
            ),
            0.00022,
            self.app_data,
        )
        self.play_title = relative_scale(
            self.app_data.font.render(
                "Play Screen",
                True,
                self.app_data.text_color,
            ),
            0.00022,
            self.app_data,
        )
        self.play_w_a_s_d = relative_scale(
            self.app_data.font.render(
                "W A S D",
                True,
                self.app_data.text_color,
            ),
            0.0002,
            self.app_data,
        )
        self.play_arrows = relative_scale(
            self.app_data.font.render(
                "UP LEFT DOWN RIGHT",
                True,
                self.app_data.text_color,
            ),
            0.0002,
            self.app_data,
        )
        self.all_title = relative_scale(
            self.app_data.font.render(
                "All Screens",
                True,
                self.app_data.text_color,
            ),
            0.00022,
            self.app_data,
        )

        self.menu_title_rect = self.menu_title.get_rect(
            center=(
                self.app_data.half_width,
                self.app_data.height * 0.055,
            ),
        )
        self.play_title_rect = self.play_title.get_rect(
            center=(
                self.app_data.half_width,
                self.app_data.height * 0.445,
            ),
        )
        self.play_w_a_s_d_rect = self.play_w_a_s_d.get_rect(
            midright=(
                self.play_move_hint.left_rect.right,
                self.app_data.height * 0.60,
            ),
        )
        self.play_arrows_rect = self.play_arrows.get_rect(
            midright=(
                self.play_move_hint.left_rect.right,
                self.app_data.height * 0.72,
            ),
        )
        self.all_title_rect = self.all_title.get_rect(
            center=(
                self.app_data.half_width,
                self.app_data.height * 0.835,
            ),
        )

    def draw(self, surface: Surface):
        surface.fill(BACKGROUND_COLOR)

        self.back_button.draw(surface)

        line_width = int(self.app_data.height * 0.01)
        first_line_y = self.app_data.height * 0.385
        second_line_y = self.app_data.height * 0.775

        draw.line(
            surface,
            self.app_data.text_color,
            (self.app_data.half_width - self.app_data.half_height, first_line_y),
            (self.app_data.half_width + self.app_data.half_height, first_line_y),
            line_width,
        )
        draw.line(
            surface,
            self.app_data.text_color,
            (self.app_data.half_width - self.app_data.half_height, second_line_y),
            (self.app_data.half_width + self.app_data.half_height, second_line_y),
            line_width,
        )

        for surface_, rect in (
            (self.menu_title, self.menu_title_rect),
            (self.play_title, self.play_title_rect),
            (self.play_w_a_s_d, self.play_w_a_s_d_rect),
            (self.play_arrows, self.play_arrows_rect),
            (self.all_title, self.all_title_rect),
        ):
            surface.blit(surface_, rect)

        self.menu_play_hint.draw(surface)
        self.menu_customization_hint.draw(surface)
        self.menu_exit_hint.draw(surface)
        self.menu_help_hint.draw(surface)
        self.play_pause_hint.draw(surface)
        self.play_move_hint.draw(surface)
        self.all_back_hint.draw(surface)

    def run(self) -> tuple[Screen, bool]:
        while True:
            for event in events.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEMOTION:
                    self.back_button.set_hover(Vector2(event.pos))
                elif (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                    or event.type == pygame.MOUSEBUTTONDOWN
                    and event.button in (1, 3)
                    and self.back_button.check_hover(Vector2(event.pos))
                ):
                    return self.app_data.screen_manager.menu, False

            self.back_button.update()

            self.draw(self.app_data.display_surface)

            display.update()

            self.app_data.clock.tick(FPS)
