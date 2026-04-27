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
from core.coder import Coder, EncryptionType
from core.decoder import Decoder
from nicegui import ui, run, events
import pyperclip

class State:
    key = ""
    salt = ""
    file_path = ""
    file_content = ""
    file_type = FileType.UNKNOWN
    file_ready = False
    file_output = ""
    selected_cipher = EncryptionType.CUSTOM_CIPHER

    @property
    def selected_cipher_name(self):
        return "Custom Cipher" if self.selected_cipher == EncryptionType.CUSTOM_CIPHER else "Caesar Cipher"
    
    @property
    def can_encode(self):
        return self.file_type == FileType.TEXT

    @property
    def can_decode(self):
        return self.file_type == FileType.ENCRYPTED
    
    @property
    def output_ready(self):
        return self.file_output != None and self.file_output != ""

class UserInterface:

    def __init__(self):
        self.state = State()
        self.fileHandler = FileHandler()
        self.coder = Coder()
        self.decoder = Decoder()
        ui.page("/")(self.index)
    
    async def pick_file(self) -> None:
        picked_file = await localFilePicker()

        if picked_file == None:
            return
        
        self.state.file_path = picked_file
        ui.notify(f"Opening {self.state.file_path}")
        file_type, file_content = self.fileHandler.open(self.state.file_path)

        # check for file type
        if file_type == FileType.TEXT:
            self.state.file_type = file_type
            self.state.file_content = file_content

        else:
            self.state.file_type = file_type
            self.state.file_content = file_content
        
        # disable save button
        self.state.file_ready = False
        


    def index(self):
        with ui.header():
            ui.label("Text Coder and Decoder").classes("text-white text-2xl text-center w-full")

        with ui.row().classes("w-full flex-nowrap"):
            with ui.column().classes("shrink-0"):
                ui.button("Choose file", on_click=self.pick_file, icon="folder").classes("w-full")
                with ui.column().classes("w-full"):
                    ui.input("Code word", on_change=self.handle_password_update).bind_value(self.state, "key").classes("w-full")
                    self.password_strength_bar = ui.linear_progress(value=0, show_value=False).classes("w-full")

                with ui.row().classes("w-full"):
                    ui.button("Encode", on_click=self.handle_encode).classes("w-full") \
                        .bind_enabled(self.state, "can_encode") # Disable if selected file is not text
                    ui.button("Decode", on_click=self.handle_decode).classes("w-full") \
                        .bind_enabled(self.state, "can_decode") # Disable if selected file is not encrypted
                
                ui.button("Save", on_click=self.handle_save).classes("w-full") \
                    .bind_enabled(self.state, "file_ready") # Disable if selected file is not encrypted

                ui.label("Cipher Encoding file:")
                with ui.dropdown_button("Cipher selection", auto_close=True).bind_text(self.state, "selected_cipher_name").classes("w-full") \
                        .bind_enabled(self.state, "can_encode"):  # Disable if selected file is not text
                    ui.item("Custom Cipher", on_click=self.handle_Cipher_select_custom)
                    ui.item("Caesar Cipher", on_click=self.handle_Cipher_select_caesar)
                                

            with ui.column().classes("flex-grow w-full"):
                ui.label("Selected file:")
                ui.label("").bind_text(self.state, "file_path")
                ui.textarea(label="File preview" ).props("readonly").classes("w-full h-full").bind_value(self.state, "file_content")
                with ui.column():
                    ui.label("Output path:")
                    with ui.row():
                        ui.label("None").bind_text(self.state, "file_output")
                        ui.button(icon="content_copy", on_click=self.handle_copy).bind_enabled(self.state, "output_ready")

        
        with ui.footer():
            pass


    def handle_Cipher_select_custom(self, e: events.GenericEventArguments):
        self.state.selected_cipher = EncryptionType.CUSTOM_CIPHER

    def handle_Cipher_select_caesar(self, e: events.GenericEventArguments):
        self.state.selected_cipher = EncryptionType.CAESAR_CIPHER

    def handle_password_update(self, e: events.GenericEventArguments):
        # update password strength bar
        passwd_strength = 0
        if len(self.state.key) >= 10:
            passwd_strength = 1
        else:
            passwd_strength = len(self.state.key) / 10
        self.password_strength_bar.value = passwd_strength


    async def handle_encode(self, e: events.GenericEventArguments):
        ui.notify(f"Encrypting please wait...")

        result = await run.cpu_bound( # prevents UI from getting stuck plus it can be slow at times
            self.coder.encode,
            self.state.key,
            self.state.file_content,
            self.state.selected_cipher,
        )

        self.state.file_content = result
        self.state.file_ready = True
        self.state.file_type = FileType.ENCRYPTED
        ui.notify("Successfully encrypted content")

    async def handle_decode(self, e: events.GenericEventArguments):
        ui.notify(f"Decrypting please wait...")

        
        try:
            result = await run.cpu_bound( # prevents UI from getting stuck plus it can be slow at times
                self.decoder.decode,
                self.state.key, 
                self.state.file_content
            )
            
            self.state.file_content = result
            self.state.file_ready = True
            self.state.file_type = FileType.TEXT
            ui.notify(f"Successfully decrypted content")
        except:
            ui.notify(f"Wrong password!")
            return

    def handle_copy(self, e: events.GenericEventArguments):
        ui.notify(f"Copied path to clipboard")
        pyperclip.copy(self.state.file_output)

    async def handle_save(self, e: events.GenericEventArguments):
        save_path = await localFileSaver(self.state.file_type)
        
        if save_path == None:
            return
        
        ui.notify(f"Saving to {save_path}")

        try:
            if self.state.file_type == FileType.ENCRYPTED:
                self.fileHandler.save_encrypted_text(save_path, self.state.file_content, "")
            else:
                self.fileHandler.save_text(save_path, self.state.file_content)
        except Exception as e:
            ui.notify(f"Failed to save to {save_path} \n Error: {repr(e)}")
        finally:
            self.state.file_output = str(save_path)




if __name__ in {"__main__", "__mp_main__"}:
      UserInterface()
      ui.run(native=True, dark= True, reload=False, window_size=(1300, 800))


