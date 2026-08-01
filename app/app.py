import ctypes

import pygame
from pygame import display, font, mixer

from app.data import Data


class App:
    __slots__ = ("data",)

    data: Data

    def __init__(self):
        font.init()
        mixer.init()

        user32 = getattr(getattr(ctypes, "windll", None), "user32", None)
        if hasattr(user32, "SetProcessDPIAware"):
            user32.SetProcessDPIAware()

        display_surface = display.set_mode((0, 0), pygame.DOUBLEBUF)
        display_surface.set_alpha(None)

        self.data = Data(display_surface)

        display.set_caption("Simple Arcade")
        display.set_icon(self.data.assets.get_image("icon.png"))

    def run(self):
        self.data.sounds.launch_music()

        while True:
            self.data.screen_manager.run()
