from io import BytesIO
from os import scandir
from pathlib import Path
from zipfile import ZipFile

from app.assets.types import AssetDirectory


def read_directory(path: Path) -> AssetDirectory:
    directory = {}

    for item in scandir(path):
        item_path = Path(item.path)

        directory[item.name] = (
            read_directory(item_path)
            if item.is_dir()
            else BytesIO(item_path.read_bytes())
        )

    return directory


def write_zip(
    zip_file: ZipFile,
    directory: AssetDirectory,
    directory_path: Path = Path("."),
):
    for name, item in directory.items():
        path = directory_path / name

        if isinstance(item, dict):
            write_zip(zip_file, item, path)
        else:
            zip_file.writestr(str(path), item.getvalue())


def read_zip(path: Path) -> AssetDirectory:
    directory = {}

    with ZipFile(path, "r") as zip_file:
        for item in zip_file.infolist():
            if not item.is_dir():
                parts = Path(item.filename).parts
                current_directory = directory

                for part in parts[:-1]:
                    if isinstance(current_directory, dict):
                        current_directory = current_directory.setdefault(part, {})

                if isinstance(current_directory, dict):
                    current_directory[parts[-1]] = BytesIO(zip_file.read(item))

    return directory
