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
from ui.localFileSaver import localFileSaver
from core.fileHandler import FileHandler, FileType
from core.coder import Coder
from nicegui import events, ui


class State:
    password = ""
    salt = ""
    file_path = ""
    file_content = ""
    file_type = FileType.UNKNOWN
    file_ready = False

    @property
    def can_encode(self):
        return self.file_type == FileType.TEXT

    @property
    def can_decode(self):
        return self.file_type == FileType.ENCRYPTED

class UserInterface:

    def __init__(self):
        self.state = State()
        self.fileHandler = FileHandler()
        self.coder = Coder()
        ui.page("/")(self.index)
    
    async def pick_file(self) -> None:
        self.state.file_path = await localFilePicker()
        ui.notify(f'Opening {self.state.file_path}')


        file_type, file_content = self.fileHandler.open(self.state.file_path)

        # check for file type
        if file_type == FileType.TEXT:
            self.state.file_type = file_type
            self.state.file_content = file_content

        else:
            self.state.file_type = file_type
            raise NotImplementedError()
        
        # disable save button
        self.state.file_ready = False
        


    def index(self):
        with ui.header():
            ui.label("Text Coder and Decoder").classes("text-white text-2xl text-center w-full")

        with ui.row().classes("w-full flex-nowrap"):
            with ui.column().classes("shrink-0"):
                ui.button('Choose file', on_click=self.pick_file, icon='folder').classes("w-full")
                with ui.column().classes("w-full"):
                    ui.input('Code word', on_change=self.handle_password_update).bind_value(self.state, "password").classes("w-full")
                    self.password_strength_bar = ui.linear_progress(value=0, show_value=False).classes("w-full")

                with ui.row().classes("w-full"):
                    ui.button('Encode', on_click=self.handle_encode).classes("w-full") \
                        .bind_enabled(self.state, 'can_encode') # Disable if selected file is not text
                    ui.button('Decode', on_click=self.handle_decode).classes("w-full") \
                        .bind_enabled(self.state, 'can_decode') # Disable if selected file is not encrypted
                
                ui.button('Save', on_click=self.handle_save).classes("w-full") \
                    .bind_enabled(self.state, 'file_ready') # Disable if selected file is not encrypted
                
                with ui.row():
                    ui.label("Output path: <lorem>")
                    ui.button(icon="content_copy")

            with ui.column().classes("flex-grow w-full"):
                ui.label("Selected file:")
                ui.label("").bind_text(self.state, "file_path")
                ui.textarea(label="File preview" ).props("readonly").classes("w-full h-full").bind_value(self.state, "file_content")
        
        with ui.footer():
            pass

    def handle_password_update(self, e: events.GenericEventArguments):
        # update password strength bar
        passwd_strength = 0
        if len(self.state.password) >= 10:
            passwd_strength = 1
        else:
            passwd_strength = len(self.state.password) / 10
        self.password_strength_bar.value = passwd_strength


    def handle_encode(self, e: events.GenericEventArguments):
        ui.notify(f'Creating encrypted version of {self.state.file_path}')

        result = self.coder.encode(self.state.password, self.state.file_content)

        self.state.file_content = result
        self.state.file_ready = True
        self.state.file_type = FileType.ENCRYPTED

    def handle_decode(self, e: events.GenericEventArguments):
        ui.notify(f'Decrypting {self.state.file_path}')

    async def handle_save(self, e: events.GenericEventArguments):
        save_path = await localFileSaver(FileType.ENCRYPTED)
        ui.notify(f'Saving to {save_path}')



if __name__ in {"__main__", "__mp_main__"}:
      UserInterface()
      ui.run(native=True)


