from random import uniform
from sys import exit
from typing import TYPE_CHECKING

import pygame
from pygame import Surface, display
from pygame import event as events

from app.constants import BACKGROUND_COLOR, FPS
from app.entities import Player
from app.entities.groups import Enemies
from app.screen_manager.screens import Screen
from app.screen_manager.screens.play.background import Background
from app.screen_manager.screens.play.pause import Pause
from app.utils import milliseconds_to_ticks, relative_scale, smooth

if TYPE_CHECKING:
    from app.data import Data


class PlayScreen(Screen):
    __slots__ = (
        "app_data",
        "background",
        "enemies",
        "pause",
        "player",
        "progress",
        "score",
        "time_coefficient",
        "time_coefficient_base",
    )

    app_data: "Data"
    background: Background
    enemies: Enemies
    pause: Pause
    player: Player
    progress: float
    score: int
    time_coefficient: float
    time_coefficient_base: float

    def __init__(self, app_data: "Data"):
        self.app_data = app_data

        self.time_coefficient = 1
        self.progress = 1
        self.score = 0

        def reset_timer():
            max_milliseconds = 800 - (5 - self.app_data.level) * 85 * self.progress
            min_ticks = milliseconds_to_ticks(max_milliseconds - 50)
            max_ticks = milliseconds_to_ticks(max_milliseconds)

            return uniform(min_ticks, max_ticks)

        self.enemies = Enemies(app_data, reset_timer)

        self.player = Player(app_data, self)
        self.pause = Pause(app_data)
        self.background = Background(app_data, self.player)

        self.reset()

    def reset(self):
        self.enemies.reset()

        self.player.reset()
        self.pause.reset()
        self.background.reset()

        self.progress = 1
        self.time_coefficient_base = 0
        self.score = 0

    def redraw(self):
        self.pause.redraw()

    def draw(self, surface: Surface):
        surface.fill(BACKGROUND_COLOR)

        self.background.draw(surface)
        self.player.draw(surface)

        self.enemies.draw(surface)

        self.pause.draw(surface)

        score_position = self.app_data.height * 0.025

        score_surface = relative_scale(
            self.app_data.font.render(
                f"Score: {self.score}",
                True,
                self.app_data.text_color,
            ),
            0.00009,
            self.app_data,
        )
        surface.blit(
            score_surface,
            score_surface.get_rect(topleft=(score_position, score_position)),
        )

    def run(self):
        self.enemies.reset()

        on_pause = False

        while True:
            for event in events.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_ESCAPE,
                    pygame.K_SPACE,
                ):
                    self.app_data.sounds.pause.play()

                    on_pause = not on_pause

            self.progress = min(self.progress + 0.00025 * self.time_coefficient, 2)

            self.player.update()
            self.pause.set_alpha(self.time_coefficient_base)

            self.score += self.enemies.update(
                self.player.position,
                self.time_coefficient,
            )

            if self.enemies.check_player_collision(self.player):
                self.app_data.max_score = max(self.app_data.max_score, self.score)
                self.app_data.money += self.score
                self.app_data.last_score = self.score

                self.app_data.save()

                return self.app_data.screen_manager.menu, True
            else:
                self.time_coefficient_base = smooth(
                    255 if on_pause else 0,
                    self.time_coefficient_base,
                    0.025,
                    0.1,
                )
                self.time_coefficient = 1 - self.time_coefficient_base / 255

                self.draw(self.app_data.display_surface)

                display.update()

                self.app_data.clock.tick(FPS)
