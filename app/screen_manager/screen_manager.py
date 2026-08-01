from sys import exit
from typing import TYPE_CHECKING

import pygame
from pygame import Surface, display
from pygame import event as events

from app.constants import BACKGROUND_COLOR, FPS
from app.screen_manager.screens import (
    AuthorsScreen,
    CustomScreen,
    HelpScreen,
    MenuScreen,
    PlayScreen,
    Screen,
)
from app.utils import smooth

if TYPE_CHECKING:
    from app.data import Data


class ScreenManager:
    __slots__ = (
        "app_data",
        "authors",
        "current_screen",
        "custom",
        "help",
        "menu",
        "play",
        "previous_screen",
    )

    app_data: "Data"
    authors: AuthorsScreen
    current_screen: Screen
    custom: CustomScreen
    help: HelpScreen
    menu: MenuScreen
    play: PlayScreen
    previous_screen: Screen

    def __init__(self, data: "Data"):
        self.app_data = data

        self.play = PlayScreen(data)
        self.menu = MenuScreen(data)
        self.authors = AuthorsScreen(data)
        self.help = HelpScreen(data)
        self.custom = CustomScreen(data)

        self.current_screen = self.menu

    def run(self):
        self.previous_screen = self.current_screen

        self.current_screen, animation_is_reverse = self.previous_screen.run()

        self.change_screen(animation_is_reverse)

        self.previous_screen.reset()

    def change_screen(self, animation_is_reverse: bool):
        if self.previous_screen == self.play:
            self.app_data.sounds.death.play()
        else:
            self.app_data.sounds.action.play()

        previous_surface = Surface(self.app_data.size).convert()
        current_surface = Surface(self.app_data.size).convert()

        self.previous_screen.draw(previous_surface)
        self.current_screen.draw(current_surface)

        previous_rect = previous_surface.get_rect(topleft=(0, 0))
        current_rect = previous_surface.get_rect(topleft=(0, 0))

        animation_step = self.app_data.height // 75
        if animation_is_reverse:
            animation_step *= -1

        alpha = 255
        while alpha > 0:
            for event in events.get():
                if event.type == pygame.QUIT:
                    exit()

            previous_rect.y += animation_step

            int_alpha = int(alpha)

            previous_surface.set_alpha(int_alpha)
            current_surface.set_alpha(255 - int_alpha)

            alpha = smooth(0, alpha, 7.5, 0.1)

            self.app_data.display_surface.fill(BACKGROUND_COLOR)
            self.app_data.display_surface.blit(previous_surface, previous_rect)
            self.app_data.display_surface.blit(current_surface, current_rect)

            display.update()

            self.app_data.clock.tick(FPS)
