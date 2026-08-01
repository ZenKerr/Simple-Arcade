from math import ceil, cos, pi
from random import uniform
from sys import exit
from typing import TYPE_CHECKING

import pygame
from pygame import Rect, Surface, Vector2, display
from pygame import event as events

from app.buttons import Button
from app.buttons.content import TextButtonContent
from app.constants import BACKGROUND_COLOR, FPS
from app.entities.groups import Enemies, Stars
from app.entities.star import Star
from app.screen_manager.screens import Screen
from app.screen_manager.screens.menu.level_selector import LevelSelector
from app.screen_manager.screens.menu.volume import Volume
from app.utils import milliseconds_to_ticks, relative_scale

if TYPE_CHECKING:
    from app.data import Data


class MenuScreen(Screen):
    __slots__ = (
        "app_data",
        "authors_button",
        "customization_button",
        "enemies",
        "exit_hint",
        "exit_hint_rect",
        "help_hint",
        "help_hint_rect",
        "level_selector",
        "play_button",
        "play_hint",
        "play_hint_rect",
        "stars",
        "title",
        "title_position_coefficient",
        "title_rect",
        "volume",
    )

    app_data: "Data"
    authors_button: Button
    customization_button: Button
    enemies: Enemies
    exit_hint: Surface
    exit_hint_rect: Rect
    help_hint: Surface
    help_hint_rect: Rect
    level_selector: LevelSelector
    play_button: Button
    play_hint: Surface
    play_hint_rect: Rect
    stars: Stars
    title: Surface
    title_position_coefficient: float
    title_rect: Rect
    volume: Volume

    def __init__(self, app_data: "Data"):
        self.app_data = app_data

        self.stars = Stars()
        self.enemies = Enemies(
            app_data,
            lambda: uniform(0, milliseconds_to_ticks(7500)),
        )
        self.title_position_coefficient = pi / 2

        self.level_selector = LevelSelector(app_data)
        self.volume = Volume(app_data)

        self.play_button = Button(
            app_data,
            TextButtonContent(app_data, "Play"),
            Vector2(app_data.half_width, app_data.height * 0.4),
        )
        self.customization_button = Button(
            app_data,
            TextButtonContent(app_data, "Customization"),
            Vector2(app_data.half_width, app_data.height * 0.55),
        )
        self.authors_button = Button(
            app_data,
            TextButtonContent(app_data, "Authors", 0.00015),
            Vector2(app_data.height * 0.145, app_data.height * 0.945),
            Vector2(0.25, 0.07),
        )

        self.redraw()

        self.title_rect = self.title.get_rect(
            midtop=(
                self.calculate_title_x(),
                self.app_data.height * 0.025,
            )
        )

        self.play_hint_rect = self.play_hint.get_rect(
            center=(
                self.app_data.half_width,
                self.app_data.height * 0.97,
            ),
        )
        self.exit_hint_rect = self.exit_hint.get_rect(
            topleft=(
                self.app_data.height * 0.025,
                self.app_data.height * 0.025,
            ),
        )
        self.help_hint_rect = self.help_hint.get_rect(
            center=(
                self.app_data.width - self.app_data.height * 0.09,
                self.app_data.height * 0.97,
            ),
        )

        self.reset()

    def reset(self):
        self.level_selector.reset()
        self.volume.reset()

        self.play_button.reset()
        self.customization_button.reset()
        self.authors_button.reset()

    def redraw(self):
        self.level_selector.redraw()
        self.volume.redraw()

        self.play_button.redraw()
        self.customization_button.redraw()
        self.authors_button.redraw()

        self.title = relative_scale(
            self.app_data.font.render(
                "Simple Arcade",
                True,
                self.app_data.text_color,
            ),
            0.0002,
            self.app_data,
        )

        self.play_hint = relative_scale(
            self.app_data.font.render(
                "Space to play",
                True,
                self.app_data.text_color,
            ),
            0.00009,
            self.app_data,
        )
        self.exit_hint = relative_scale(
            self.app_data.font.render(
                "ESC to exit",
                True,
                self.app_data.text_color,
            ),
            0.00009,
            self.app_data,
        )
        self.help_hint = relative_scale(
            self.app_data.font.render(
                "H for HELP",
                True,
                self.app_data.text_color,
            ),
            0.00009,
            self.app_data,
        )

    def draw(self, surface: Surface):
        surface.fill(BACKGROUND_COLOR)

        self.stars.draw(surface, Vector2(0))
        self.enemies.draw(surface)

        self.level_selector.draw(surface)
        self.volume.draw(surface)

        self.play_button.draw(surface)
        self.customization_button.draw(surface)
        self.authors_button.draw(surface)

        surface.blit(self.title, self.title_rect)

        surface.blit(self.play_hint, self.play_hint_rect)
        surface.blit(self.exit_hint, self.exit_hint_rect)
        surface.blit(self.help_hint, self.help_hint_rect)

        money_surface = relative_scale(
            self.app_data.font.render(
                f"Balance {self.app_data.money}$",
                True,
                self.app_data.text_color,
            ),
            0.00009,
            self.app_data,
        )
        last_score_surface = relative_scale(
            self.app_data.font.render(
                f"Last game score {self.app_data.last_score}",
                True,
                self.app_data.text_color,
            ),
            0.00009,
            self.app_data,
        )
        record_surface = relative_scale(
            self.app_data.font.render(
                f"Your record {self.app_data.max_score}",
                True,
                self.app_data.text_color,
            ),
            0.00009,
            self.app_data,
        )

        surface.blit(
            money_surface,
            money_surface.get_rect(
                topright=(
                    self.app_data.width - self.app_data.height * 0.025,
                    self.app_data.height * 0.025,
                ),
            ),
        )
        surface.blit(
            last_score_surface,
            last_score_surface.get_rect(
                topright=(
                    self.app_data.width - self.app_data.height * 0.025,
                    self.app_data.height * 0.056,
                ),
            ),
        )
        surface.blit(
            record_surface,
            record_surface.get_rect(
                topright=(
                    self.app_data.width - self.app_data.height * 0.025,
                    self.app_data.height * 0.085,
                ),
            ),
        )

    def run(self) -> tuple[Screen, bool]:
        while True:
            for event in events.get():
                if event.type == pygame.QUIT:
                    self.app_data.save()
                    exit()
                elif event.type == pygame.MOUSEMOTION:
                    mouse_position = Vector2(event.pos)

                    for level in self.level_selector.levels:
                        level.set_hover(mouse_position)

                    self.play_button.set_hover(mouse_position)
                    self.customization_button.set_hover(mouse_position)
                    self.authors_button.set_hover(mouse_position)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in (1, 3):
                        mouse_position = Vector2(event.pos)

                        if self.play_button.check_hover(mouse_position):
                            return self.app_data.screen_manager.play, False
                        elif self.customization_button.check_hover(mouse_position):
                            return self.app_data.screen_manager.custom, True
                        elif self.authors_button.check_hover(mouse_position):
                            return self.app_data.screen_manager.authors, True
                        elif self.level_selector.rect.collidepoint(mouse_position):
                            self.level_selector.on_click()
                        elif enemy := self.enemies.on_click(mouse_position):
                            for segment in enemy.tail.get_segments():
                                for _ in range(ceil(segment.radius / 1.5)):
                                    self.stars.add(
                                        Star(
                                            self.app_data,
                                            1,
                                            segment.position
                                            + Vector2(
                                                uniform(
                                                    -segment.radius, segment.radius
                                                ),
                                                uniform(
                                                    -segment.radius, segment.radius
                                                ),
                                            ),
                                            enemy.speed.rotate(uniform(-10, 10))
                                            * uniform(0.5, 1.5),
                                        )
                                    )

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        return self.app_data.screen_manager.play, False
                    elif event.key == pygame.K_ESCAPE:
                        self.app_data.save()

                        exit()
                    elif event.key == pygame.K_BACKSPACE:
                        return self.app_data.screen_manager.custom, True
                    elif event.key == pygame.K_h:
                        return self.app_data.screen_manager.help, True

            self.title_position_coefficient += 0.0075
            self.title_rect.centerx = self.calculate_title_x()

            self.level_selector.update()
            self.volume.update()

            self.play_button.update()
            self.customization_button.update()
            self.authors_button.update()

            enemies_target = Vector2(
                uniform(self.app_data.width * 0.1, self.app_data.width * 0.9),
                uniform(self.app_data.height * 0.1, self.app_data.height * 0.9),
            )

            self.stars.update()
            self.enemies.update(enemies_target, 1)

            self.draw(self.app_data.display_surface)

            display.update()

            self.app_data.clock.tick(FPS)

    def calculate_title_x(self) -> int:
        offset = cos(self.title_position_coefficient) * self.app_data.height * 0.1

        return int(self.app_data.half_width - offset)
