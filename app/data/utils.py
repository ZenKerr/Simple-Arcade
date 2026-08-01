from app.types import Colors


def get_colors[T](levels: dict[int, tuple[T, ...]]) -> Colors[T]:
    return tuple((price, color) for price, colors in levels.items() for color in colors)
