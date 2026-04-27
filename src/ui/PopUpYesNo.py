from nicegui import ui


class popUpYesNo(ui.dialog):
    """
    Simple pop up window dialog object
    """

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