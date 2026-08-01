from typing import TYPE_CHECKING

from pygame.mixer import Sound, music

if TYPE_CHECKING:
    from app.data import Data


class Sounds:
    __slots__ = (
        "action",
        "app_data",
        "buy",
        "classic",
        "death",
        "error",
        "hard",
        "hover",
        "inferno",
        "light",
        "pause",
        "primitive",
        "volume",
    )

    action: Sound
    app_data: "Data"
    buy: Sound
    classic: Sound
    death: Sound
    error: Sound
    hard: Sound
    hover: Sound
    inferno: Sound
    light: Sound
    pause: Sound
    primitive: Sound
    volume: float

    def __init__(self, app_data: "Data", volume: float):
        self.app_data = app_data

        self.hover = app_data.assets.get_sound("hover.wav")
        self.action = app_data.assets.get_sound("action.wav")
        self.pause = app_data.assets.get_sound("pause.wav")
        self.death = app_data.assets.get_sound("death.wav")
        self.error = app_data.assets.get_sound("error.wav")
        self.buy = app_data.assets.get_sound("buy.wav")

        self.inferno = app_data.assets.get_sound("inferno.wav")
        self.hard = app_data.assets.get_sound("hard.wav")
        self.classic = app_data.assets.get_sound("classic.wav")
        self.light = app_data.assets.get_sound("light.wav")
        self.primitive = app_data.assets.get_sound("primitive.wav")

        self.set_volume(volume)

    def set_volume(self, volume: float):
        self.volume = volume

        music.set_volume(volume)

        for sound in (
            self.hover,
            self.action,
            self.pause,
            self.death,
            self.error,
            self.buy,
            self.inferno,
            self.hard,
            self.classic,
            self.light,
            self.primitive,
        ):
            sound.set_volume(volume)

    def launch_music(self):
        music.load(self.app_data.assets.get_music("music.mp3"))
        music.play(-1)
