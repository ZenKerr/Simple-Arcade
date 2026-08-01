from math import copysign
from typing import TYPE_CHECKING

from pygame import Surface, Vector2, mouse, transform

from app.constants import FPS
from app.types import Color, ColorSource

if TYPE_CHECKING:
    from app.data import Data


def get_color(color_source: ColorSource) -> Color:
    return color_source if isinstance(color_source, tuple) else color_source()


def relative_scale(surface: Surface, scale: float, app_data: "Data") -> Surface:
    scaled_height = app_data.height * scale

    return transform.scale(surface, Vector2(surface.get_size()) * scaled_height)


def smooth(
    target: float,
    current: float,
    min_step: float,
    speed: float = 0.15,
) -> float:
    delta = target - current

    if abs(delta) <= min_step:
        return target
    else:
        step = delta * speed

        return current + (copysign(min_step, delta) if abs(step) < min_step else step)


def milliseconds_to_ticks(milliseconds: float) -> float:
    return milliseconds / 1000 * FPS


def get_mouse_position() -> Vector2:
    return Vector2(mouse.get_pos())
