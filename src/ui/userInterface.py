"""
This is the main UI file build by using NiceGui
It contains all the main functions that call core and other utilities.
like fileHandler, coder decoder and PerformanceEvaluator


"""

from ui.localFilePicker import localFilePicker
from ui.localFileSaver import localFileSaver
from core.fileHandler import FileHandler, FileType
from core.coder import Coder, EncryptionType
from core.performanceEvaluator import PerformanceEvaluator, PerformanceStats
from core.decoder import Decoder
from nicegui import ui, run, events
import pyperclip

class State:
    "state file contacting current state variables used to bind to labels and buttons to update their values"
    key = ""
    salt = ""
    file_source_path = ""
    file_content = ""
    file_type = FileType.UNKNOWN
    file_ready = False
    file_output = ""
    selected_cipher = EncryptionType.CUSTOM_CIPHER
    plain_text_size = None
    coded_text_size = None
    plain_text_length = None
    coded_text_length = None
    fer = None


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
        self.perf_eval = PerformanceEvaluator()
        ui.page("/")(self.index)
    
    async def pick_file(self) -> None:
        picked_file = await localFilePicker()

        if picked_file == None:
            return
        
        self.state.file_source_path = picked_file
        ui.notify(f"Opening {self.state.file_source_path}")
        file_type, file_content = self.fileHandler.open(self.state.file_source_path)

        # check for file type
        if file_type == FileType.TEXT:
            self.state.file_type = file_type
            self.state.file_content = file_content

        else:
            self.state.file_type = file_type
            self.state.file_content = file_content
        
        
        self.state.file_ready = False # disable save button
        self.state.file_output = None
        


    def index(self):
        
        ui.colors(primary="#B166B9")

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
                ui.label("").bind_text(self.state, "file_source_path")
                ui.textarea(label="File preview" ).props("readonly").classes("w-full h-full").bind_value(self.state, "file_content")
                with ui.column():
                    ui.label("Output path:")
                    with ui.row():
                        ui.label("None").bind_text(self.state, "file_output")
                        ui.button(icon="content_copy", on_click=self.handle_copy).bind_enabled(self.state, "output_ready")
                with ui.row():
                    ui.label("plain text size: ")
                    ui.label("").bind_text(self.state, "plain_text_size")
                with ui.row():
                    ui.label("plain text length: ")
                    ui.label("").bind_text(self.state, "plain_text_length")
                with ui.row():
                    ui.label("coded text size: ")
                    ui.label("").bind_text(self.state, "coded_text_size")
                with ui.row():
                    ui.label("coded text length: ")
                    ui.label("").bind_text(self.state, "coded_text_length")
                with ui.row():
                    ui.label("File expansion ratio: ")
                    ui.label("").bind_text(self.state, "fer")


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

        # Adapt colors to password strength
        if passwd_strength == 0:
            self.password_strength_bar.classes(add="bg-red-500")
        elif passwd_strength < 0.5:
            self.password_strength_bar.classes(remove="bg-red-500")
            self.password_strength_bar.props("color=red")
        elif passwd_strength < 0.8:
            self.password_strength_bar.classes(remove="bg-red-500")
            self.password_strength_bar.props("color=yellow")
        elif passwd_strength >= 1.0:
            self.password_strength_bar.classes(remove="bg-red-500")
            self.password_strength_bar.props("color=green")

        
        self.password_strength_bar.value = passwd_strength


    async def handle_encode(self, e: events.GenericEventArguments):

        if not self.state.key or len(self.state.key) == 0:
            ui.notify(f"Password can't be empty", color="red")
            return

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
        ui.notify("Successfully encrypted content", color="green")

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
            ui.notify(f"Successfully decrypted content", color="green")
        except:
            ui.notify(f"Wrong password!", color="red")
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
            self.update_stats()

    def update_stats(self):
        if self.state.file_type == FileType.ENCRYPTED:
            result = self.perf_eval.get_performance(self.state.file_output, self.state.file_source_path)
        else:
            result = self.perf_eval.get_performance(self.state.file_source_path, self.state.file_output)

        self.state.plain_text_size = result.plain_text_size
        self.state.coded_text_size = result.coded_text_size
        self.state.plain_text_length = result.plain_text_length
        self.state.coded_text_length = result.coded_text_length
        self.state.fer = result.fer




if __name__ in {"__main__", "__mp_main__"}:
      UserInterface()
      ui.run(native=True, dark= True, reload=False, window_size=(1300, 800))


