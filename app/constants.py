from os import environ
from pathlib import Path

PATH_TO_SAVE_DIRECTORY = Path(environ["USERPROFILE"], "Documents", "Sarni Studio")
PATH_TO_SAVE = PATH_TO_SAVE_DIRECTORY / "arcade.save"

BACKGROUND_COLOR = (8, 8, 8)

FPS = 75
