"""
Class for user interface (UI) functionalities: class UserInterface
Minimum GUI requirements:

3
▪ A Browse feature to select a plaintext .txt file
    o A Codeword input field
    o Separate actions:
        ▪ Encode (Code) button/option
        ▪ Decode button/option

o Display useful status information:
    ▪ selected file name/path
    ▪ copyable output file path.
    
o operation status (success/failure + reason)

"""

from ui.localFilePicker import localFilePicker
from nicegui import events, ui


class UserInterface:

    def __init__(self):
        ui.page('/')(self.index)
    
    async def pick_file(self) -> None:
        result = await localFilePicker()
        ui.notify(f'Opening {result}')
        
    def index(self):
        with ui.header():
            ui.label("Text Coder and Decoder").classes("text-white text-2xl text-center w-full")

        with ui.row().classes("w-full flex-nowrap"):
            with ui.column():
                ui.button('Choose file', on_click=self.pick_file, icon='folder')
                with ui.column():
                    self.password_field = ui.input('Code word', on_change=self.update_password)
                    self.password_strength_bar = ui.linear_progress(value=0, show_value=False)
                with ui.row():
                    ui.button('Encode')
                    ui.button('Decode')
                ui.label("Selected file: <lorem>")
                with ui.row():
                    ui.label("Output path: <lorem>")
                    ui.button(icon="content_copy")

            ui.textarea(label="File preview" ).props("readonly").classes("flex-grow")
        
        with ui.footer():
            pass

    def update_password(self,e: events.GenericEventArguments):

        # update password strength bar
        passwd_strength = 0
        if len(self.password_field.value) >= 10:
            passwd_strength = 1
        else:
            passwd_strength = len(self.password_field.value) / 10
        self.password_strength_bar.value = passwd_strength





if __name__ in {"__main__", "__mp_main__"}:
      UserInterface()
      ui.run(native=True)


