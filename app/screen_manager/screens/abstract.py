from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from pygame import Surface

if TYPE_CHECKING:
    from app.data import Data


class Screen(ABC):
    __slots__ = ()

    @abstractmethod
    def __init__(self, app_data: "Data"): ...

    @abstractmethod
    def reset(self): ...

    @abstractmethod
    def redraw(self): ...

    @abstractmethod
    def draw(self, surface: Surface): ...

    @abstractmethod
    def run(self) -> tuple["Screen", bool]: ...
