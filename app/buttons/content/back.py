from typing import TYPE_CHECKING

from app.buttons.content.text import TextButtonContent

if TYPE_CHECKING:
    from app.data import Data


class BackButtonContent(TextButtonContent):
    __slots__ = ()

    def __init__(self, app_data: "Data"):
        super().__init__(app_data, "< Back", 0.00015)
