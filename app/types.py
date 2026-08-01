from collections.abc import Callable

type Color = tuple[int, int, int]
type ColorRange = Callable[[], Color]
type Colors[T] = tuple[tuple[int, T], ...]
type ColorSource = Color | ColorRange
