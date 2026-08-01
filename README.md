# Simple Arcade

[![Steam](https://img.shields.io/badge/Steam-Available_on_Steam-1b2838?logo=steam)](https://store.steampowered.com/app/2333840)
[![Python](https://img.shields.io/badge/python-3.13-blue.svg?logo=python&logoColor=white)](https://www.python.org)
![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat&logo=opensourceinitiative&logoColor=white)
![Asset License](https://img.shields.io/badge/License-CC0_1.0-blue.svg?logo=creative-commons&logoColor=white)

A simple game that harkens back to the early arcade games.

---

## Usage

Download and play on [Steam](https://store.steampowered.com/app/2333840).

### From Source

To run the game from source, ensure you have **Python 3.13** and **uv** installed.

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
uv run pyinstaller build.spec
```

---

## License

This project uses a dual licensing model:

* **Code:** [MIT License](https://opensource.org/licenses/MIT)
  ([LICENSE-MIT](https://github.com/ZenKerr/Simple-Arcade/blob/HEAD/LICENSE-MIT))
* **Assets:** [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/legalcode)
  ([LICENSE-CC0-1.0](https://github.com/ZenKerr/Simple-Arcade/blob/HEAD/LICENSE-CC0-1.0))