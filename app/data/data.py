from itertools import chain

from pygame import Rect, Surface, Vector2
from pygame.font import Font
from pygame.time import Clock

from app.assets import Assets
from app.constants import PATH_TO_SAVE, PATH_TO_SAVE_DIRECTORY
from app.data.constants import (
    LEVEL_1_COLOR_RANGES,
    LEVEL_1_COLORS,
    LEVEL_1_PRICE,
    LEVEL_2_COLOR_RANGES,
    LEVEL_2_COLORS,
    LEVEL_2_PRICE,
    LEVEL_3_COLOR_RANGES,
    LEVEL_3_COLORS,
    LEVEL_3_PRICE,
    LEVEL_4_COLOR_RANGES,
    LEVEL_4_COLORS,
    LEVEL_4_PRICE,
    LEVEL_5_COLOR_RANGES,
    LEVEL_5_COLORS,
    LEVEL_5_PRICE,
)
from app.data.utils import get_colors
from app.screen_manager import ScreenManager
from app.sounds import Sounds
from app.types import Color, ColorRange, Colors


class Data:
    __slots__ = (
        "assets",
        "clock",
        "color_ranges",
        "colors",
        "display_rect",
        "display_surface",
        "enemy_color",
        "enemy_color_index",
        "font",
        "half_height",
        "half_size",
        "half_width",
        "height",
        "last_score",
        "level",
        "max_score",
        "money",
        "player_color",
        "player_color_index",
        "screen_manager",
        "size",
        "sounds",
        "text_color",
        "text_color_index",
        "unlock_enemy_colors",
        "unlock_player_colors",
        "unlock_text_colors",
        "width",
    )

    assets: Assets
    clock: Clock
    color_ranges: Colors[ColorRange]
    colors: Colors[Color]
    display_rect: Rect
    display_surface: Surface
    enemy_color: ColorRange
    enemy_color_index: int
    font: Font
    half_height: float
    half_size: Vector2
    half_width: float
    height: int
    last_score: int
    level: int
    max_score: int
    money: int
    player_color: Color
    player_color_index: int
    screen_manager: ScreenManager
    size: Vector2
    sounds: Sounds
    text_color: Color
    text_color_index: int
    unlock_enemy_colors: list[bool]
    unlock_player_colors: list[bool]
    unlock_text_colors: list[bool]
    width: int

    def __init__(self, display_surface: Surface):
        self.colors = get_colors(
            {
                LEVEL_1_PRICE: LEVEL_1_COLORS,
                LEVEL_2_PRICE: LEVEL_2_COLORS,
                LEVEL_3_PRICE: LEVEL_3_COLORS,
                LEVEL_4_PRICE: LEVEL_4_COLORS,
                LEVEL_5_PRICE: LEVEL_5_COLORS,
            }
        )
        self.color_ranges = get_colors(
            {
                LEVEL_1_PRICE: LEVEL_1_COLOR_RANGES,
                LEVEL_2_PRICE: LEVEL_2_COLOR_RANGES,
                LEVEL_3_PRICE: LEVEL_3_COLOR_RANGES,
                LEVEL_4_PRICE: LEVEL_4_COLOR_RANGES,
                LEVEL_5_PRICE: LEVEL_5_COLOR_RANGES,
            }
        )

        volume = self.load()

        self.display_surface = display_surface
        self.display_rect = display_surface.get_rect()

        self.clock = Clock()

        self.width = display_surface.get_width()
        self.height = display_surface.get_height()
        self.size = Vector2(self.width, self.height)

        self.half_width = self.width / 2
        self.half_height = self.height / 2
        self.half_size = Vector2(self.half_width, self.half_height)

        self.assets = Assets()
        self.font = self.assets.get_font("font.ttf")

        self.text_color = self.colors[self.text_color_index][1]
        self.player_color = self.colors[self.player_color_index][1]
        self.enemy_color = self.color_ranges[self.enemy_color_index][1]

        self.sounds = Sounds(self, volume)
        self.screen_manager = ScreenManager(self)

    def save(self):
        with open(PATH_TO_SAVE, "w") as save_file:
            for value in (
                self.max_score,
                self.money,
                self.last_score,
                self.text_color_index,
                self.player_color_index,
                self.enemy_color_index,
                self.level,
            ):
                save_file.writelines(f"{value}\n")

            for value in chain(
                self.unlock_player_colors,
                self.unlock_enemy_colors,
                self.unlock_text_colors,
            ):
                save_file.writelines(f"{int(value)}\n")

            save_file.writelines(f"{self.sounds.volume}\n")

    def load(self) -> float:
        PATH_TO_SAVE_DIRECTORY.mkdir(parents=True, exist_ok=True)

        with open(PATH_TO_SAVE, "a+") as save_file:
            save_file.seek(0)

            lines = iter(save_file.readlines())

            self.max_score = int(next(lines, 0))
            self.money = int(next(lines, 0))
            self.last_score = int(next(lines, 0))
            self.text_color_index = int(next(lines, 0))
            self.player_color_index = int(next(lines, 0))
            self.enemy_color_index = int(next(lines, 0))
            self.level = int(next(lines, 3))

            self.unlock_player_colors = [
                bool(int(next(lines, not i))) for i in range(len(self.colors))
            ]
            self.unlock_enemy_colors = [
                bool(int(next(lines, not i))) for i in range(len(self.color_ranges))
            ]
            self.unlock_text_colors = [
                bool(int(next(lines, not i))) for i in range(len(self.colors))
            ]

            return float(next(lines, 0.5))
