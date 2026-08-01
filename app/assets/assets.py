import sys
from functools import reduce
from io import BytesIO
from operator import getitem
from pathlib import Path
from zipfile import ZIP_LZMA, ZipFile

from pygame import Surface, image
from pygame.font import Font
from pygame.mixer import Sound

from app.assets.types import AssetDirectory
from app.assets.utils import read_directory, read_zip, write_zip


class Assets:
    __slots__ = ("directory",)

    directory: AssetDirectory

    def __init__(self):
        self.directory = (
            read_zip(Path(getattr(sys, "_MEIPASS", "."), "build_assets.zip"))
            if getattr(sys, "frozen", False)
            else read_directory(Path(".", "assets"))
        )

    def __getitem__(self, path: Path) -> BytesIO:
        result = reduce(getitem, path.parts, self.directory)

        if isinstance(result, BytesIO):
            return result
        else:
            raise FileNotFoundError(f"Asset not found: {path}")

    def get_font(self, name: str) -> Font:
        return Font(self[Path("fonts", name)], 255)

    def get_image(self, name: str) -> Surface:
        return image.load(self[Path("images", name)])

    def get_sound(self, name: str) -> Sound:
        return Sound(self[Path("sounds", name)])

    def get_music(self, name: str) -> BytesIO:
        return self[Path("music", name)]

    def zip(self) -> Path:
        path = Path(".", "build", "build_assets.zip")
        path.parent.mkdir(parents=True, exist_ok=True)

        with ZipFile(path, "w", ZIP_LZMA) as zip_file:
            write_zip(zip_file, self.directory)

        return path
