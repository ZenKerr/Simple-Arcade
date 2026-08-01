from collections.abc import Callable
from typing import TYPE_CHECKING

from pygame import Surface, Vector2

from app.entities.tail.segment import TailSegment
from app.types import ColorSource

if TYPE_CHECKING:
    from app.data import Data


class Tail:
    __slots__ = (
        "add_counter",
        "app_data",
        "fade_rate",
        "get_color_source",
        "head",
        "head_radius",
        "segments",
    )

    add_counter: float
    app_data: "Data"
    fade_rate: float
    get_color_source: Callable[[], ColorSource]
    head: Vector2
    head_radius: float
    segments: list[TailSegment]

    def __init__(
        self,
        app_data: "Data",
        get_color_source: Callable[[], ColorSource],
        head_radius: float,
    ):
        self.app_data = app_data

        self.get_color_source = get_color_source
        self.head_radius = head_radius
        self.fade_rate = app_data.height * 0.0007
        self.segments = []

        self.reset(Vector2(0))

    def __len__(self) -> int:
        return len(self.segments)

    def reset(self, position: Vector2):
        self.add_counter = 0
        self.head = position

        self.segments.clear()

    def update(self, time_coefficient: float, add_to_tail: bool, position: Vector2):
        for i in range(len(self.segments) - 1, -1, -1):
            if self.segments[i].update(self.fade_rate * time_coefficient):
                del self.segments[i]

        if add_to_tail:
            self.add_counter += time_coefficient

            if self.add_counter >= 1:
                self.segments.append(
                    TailSegment(
                        self.app_data,
                        self.head_radius,
                        position,
                        self.get_color_source(),
                    ),
                )

                self.add_counter -= 1

        self.head = position

    def draw(self, surface: Surface):
        for segment in self.get_segments():
            segment.draw(surface)

    def get_segments(self) -> tuple[TailSegment, ...]:
        return (
            TailSegment(
                self.app_data,
                self.head_radius,
                self.head,
                self.get_color_source(),
            ),
            *self.segments,
        )
