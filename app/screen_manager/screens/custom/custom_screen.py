from sys import exit
from typing import TYPE_CHECKING

import pygame
from pygame import Surface, Vector2, display, mouse
from pygame import event as events

from app.buttons import Button, SwitchButton
from app.buttons.content import (
    BackButtonContent,
    EntityButtonContent,
    LabeledButtonContent,
    TextButtonContent,
)
from app.constants import BACKGROUND_COLOR, FPS
from app.screen_manager.screens import Screen
from app.screen_manager.screens.custom.color_selector import ColorSelector
from app.screen_manager.screens.custom.custom_screen_target import CustomScreenTarget
from app.scroll_direction import ScrollDirection
from app.utils import relative_scale

if TYPE_CHECKING:
    from app.data import Data


class CustomScreen(Screen):
    __slots__ = (
        "app_data",
        "back_button",
        "color_selectors",
        "enemy_button",
        "interface_button",
        "player_button",
        "target",
    )

    app_data: "Data"
    back_button: Button
    color_selectors: tuple[ColorSelector, ...]
    enemy_button: SwitchButton
    interface_button: SwitchButton
    player_button: SwitchButton
    target: CustomScreenTarget

    def __init__(self, app_data: "Data"):
        self.app_data = app_data

        self.target = CustomScreenTarget.PLAYER

        self.back_button = Button(
            app_data,
            BackButtonContent(app_data),
            Vector2(0.12, 0.055) * app_data.height,
            Vector2(0.2, 0.07),
        )

        switch_target_button_x = app_data.height * 0.15
        switch_button_size = Vector2(0.25)

        self.player_button = SwitchButton(
            app_data,
            LabeledButtonContent(
                app_data,
                EntityButtonContent(
                    app_data,
                    lambda: app_data.player_color,
                    0.25,
                    0.2875,
                ),
                "Player",
            ),
            Vector2(switch_target_button_x, app_data.height * 0.25),
            switch_button_size,
            CustomScreenTarget.PLAYER,
            lambda: self.target,
        )
        self.enemy_button = SwitchButton(
            app_data,
            LabeledButtonContent(
                app_data,
                EntityButtonContent(
                    app_data,
                    lambda: app_data.enemy_color,
                    0.25,
                    0.2875,
                ),
                "Enemy",
            ),
            Vector2(switch_target_button_x, app_data.height * 0.55),
            switch_button_size,
            CustomScreenTarget.ENEMY,
            lambda: self.target,
        )
        self.interface_button = SwitchButton(
            app_data,
            LabeledButtonContent(
                app_data,
                TextButtonContent(
                    app_data,
                    "Example",
                    0.00015,
                ),
                "Interface",
            ),
            Vector2(switch_target_button_x, app_data.height * 0.85),
            switch_button_size,
            CustomScreenTarget.INTERFACE,
            lambda: self.target,
        )

        self.color_selectors = (
            ColorSelector(app_data, app_data.colors, CustomScreenTarget.PLAYER),
            ColorSelector(app_data, app_data.color_ranges, CustomScreenTarget.ENEMY),
            ColorSelector(app_data, app_data.colors, CustomScreenTarget.INTERFACE),
        )

        self.reset()

    def reset(self):
        self.back_button.reset()

        self.player_button.reset()
        self.enemy_button.reset()
        self.interface_button.reset()

    def redraw(self):
        self.back_button.redraw()

        self.player_button.redraw()
        self.enemy_button.redraw()
        self.interface_button.redraw()

        for color_selector in self.color_selectors:
            color_selector.redraw()

    def draw(self, surface: Surface):
        surface.fill(BACKGROUND_COLOR)

        self.back_button.draw(surface)

        self.player_button.draw(surface)
        self.enemy_button.draw(surface)
        self.interface_button.draw(surface)

        for color_selector in self.color_selectors:
            color_selector.draw(surface)

        balance_surface = relative_scale(
            self.app_data.font.render(
                f"Balance {self.app_data.money}$",
                True,
                self.app_data.text_color,
            ),
            0.0002,
            self.app_data,
        )
        surface.blit(
            balance_surface,
            balance_surface.get_rect(
                topright=(
                    self.app_data.width - self.app_data.height * 0.025,
                    self.app_data.height * 0.025,
                ),
            ),
        )

    def run(self) -> tuple[Screen, bool]:
        while True:
            scroll_direction = ScrollDirection.NO

            for event in events.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.app_data.save()

                        return self.app_data.screen_manager.menu, False
                elif event.type == pygame.MOUSEMOTION:
                    mouse_position = Vector2(event.pos)

                    self.back_button.set_hover(mouse_position)
                    self.player_button.set_hover(mouse_position)
                    self.enemy_button.set_hover(mouse_position)
                    self.interface_button.set_hover(mouse_position)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in (1, 3):
                        mouse_position = Vector2(event.pos)

                        if self.player_button.check_hover(mouse_position):
                            if self.target != CustomScreenTarget.PLAYER:
                                self.app_data.sounds.action.play()

                                self.target = CustomScreenTarget.PLAYER
                        elif self.enemy_button.check_hover(mouse_position):
                            if self.target != CustomScreenTarget.ENEMY:
                                self.app_data.sounds.action.play()

                                self.target = CustomScreenTarget.ENEMY
                        elif self.interface_button.check_hover(mouse_position):
                            if self.target != CustomScreenTarget.INTERFACE:
                                self.app_data.sounds.action.play()

                                self.target = CustomScreenTarget.INTERFACE
                        elif self.back_button.check_hover(mouse_position):
                            self.app_data.save()

                            return self.app_data.screen_manager.menu, False
                    elif event.button == 4:
                        scroll_direction = ScrollDirection.UP
                    elif event.button == 5:
                        scroll_direction = ScrollDirection.DOWN

            self.back_button.update()

            self.player_button.redraw()
            self.enemy_button.redraw()

            self.player_button.update()
            self.enemy_button.update()
            self.interface_button.update()

            pressed_buttons = mouse.get_pressed()
            click = pressed_buttons[0] or pressed_buttons[2]

            for color_selector in self.color_selectors:
                selected = color_selector.update(
                    self.target,
                    scroll_direction,
                    click,
                )

                if selected:
                    match self.target:
                        case CustomScreenTarget.PLAYER:
                            self.app_data.player_color_index = selected.index
                            self.app_data.player_color = selected.color
                        case CustomScreenTarget.ENEMY:
                            self.app_data.enemy_color_index = selected.index
                            self.app_data.enemy_color = selected.color
                        case CustomScreenTarget.INTERFACE:
                            self.app_data.text_color_index = selected.index
                            self.app_data.text_color = selected.color

                            self.redraw()
                            self.app_data.screen_manager.menu.redraw()
                            self.app_data.screen_manager.play.redraw()
                            self.app_data.screen_manager.authors.redraw()
                            self.app_data.screen_manager.help.redraw()

            self.draw(self.app_data.display_surface)

            display.update()

            self.app_data.clock.tick(FPS)
