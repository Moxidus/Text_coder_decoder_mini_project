
import platform
from pathlib import Path
from nicegui import events, ui
from core.fileHandler import FileType




class popUpYesNo(ui.dialog):

    def __init__(self, display_text: str) -> bool:
        """popUpYesNo dialog
            returns yes if confirmed
        """
        super().__init__()

        with self, ui.card():
            ui.label(display_text)
            with ui.row():
                ui.button('Yes', on_click=lambda: self.submit(True))
                ui.button('No', on_click=lambda: self.submit(False))