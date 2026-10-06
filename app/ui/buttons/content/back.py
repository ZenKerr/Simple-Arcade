from typing import TYPE_CHECKING

from app.ui.buttons.content.text import TextButtonContent

if TYPE_CHECKING:
    from app.services.app_data import AppData


class BackButtonContent(TextButtonContent):
    __slots__ = ()

    def __init__(self, app_data: "AppData"):
        super().__init__(app_data, "< Back", 0.00015)
