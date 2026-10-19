# Simple Arcade

[![Steam](https://img.shields.io/badge/Steam-Available_on_Steam-3572a5?logo=steam&logoColor=white)](https://store.steampowered.com/app/2333840)
[![Python](https://img.shields.io/badge/Python-3.13-3572a5?logo=python&logoColor=white)](https://www.python.org)
[![PyInstaller](https://img.shields.io/badge/Built_with-PyInstaller-3572a5?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjMgMyAxOCAxOCI%2BPHBhdGggZmlsbD0iI2ZmZiIgZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNMyAzaDE0bDQgNHYxNEgzek03IDRoOHY0SDd6TTYgMTNoMTJ2N0g2eiIvPjwvc3ZnPg%3D%3D)](https://pyinstaller.org)
[![uv](https://img.shields.io/badge/Package_manager-uv-3572a5?logo=uv&logoColor=white)](https://github.com/astral-sh/uv)
[![ty](https://img.shields.io/badge/Type_checker-ty-3572a5?logo=astral&logoColor=white)](https://github.com/astral-sh/ty)
[![Ruff](https://img.shields.io/badge/Linter-Ruff-3572a5?logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
[![License](https://img.shields.io/badge/License-MIT-3572a5?logo=opensourceinitiative&logoColor=white)](https://github.com/ZenKerr/Simple-Arcade/blob/HEAD/LICENSE-MIT)
[![Asset License](https://img.shields.io/badge/Asset_license-CC0_1.0-3572a5?logo=creative-commons&logoColor=white)](https://github.com/ZenKerr/Simple-Arcade/blob/HEAD/LICENSE-CC0-1.0)

A simple game that harkens back to the early arcade games.

---

## Usage

Download and play on [Steam](https://store.steampowered.com/app/2333840).

### From Source

To run the game from source, ensure you have **uv** installed.

1. Clone the repository:

   ```shell
   git clone https://github.com/ZenKerr/Simple-Arcade.git
   cd Simple-Arcade
   ```

2. Install dependencies:

   ```shell
   uv sync
   ```

3. Run the game:

   ```shell
   uv run main.py
   ```

Also, you can build a standalone executable using PyInstaller:

```shell
uv sync --group build

uv run pyinstaller build.spec
```

---

## License

This project uses a dual licensing model:

* **Code:** [MIT License](https://opensource.org/licenses/MIT)
  ([LICENSE-MIT](https://github.com/ZenKerr/Simple-Arcade/blob/HEAD/LICENSE-MIT))
* **Assets:** [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/legalcode)
  ([LICENSE-CC0-1.0](https://github.com/ZenKerr/Simple-Arcade/blob/HEAD/LICENSE-CC0-1.0))