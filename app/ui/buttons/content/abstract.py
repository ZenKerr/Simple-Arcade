from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from pygame import Surface, Vector2

if TYPE_CHECKING:
    from app.services.app_data import AppData


class ButtonContent(ABC):
    __slots__ = ()

    @abstractmethod
    def __init__(self, app_data: "AppData", *args, **kwargs): ...

    @abstractmethod
    def update(self): ...

    @abstractmethod
    def draw(self, surface: Surface, size: Vector2): ...
