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
from nicegui import ui


class UserInterface:
    pass

async def pick_file() -> None:
    result = await localFilePicker()
    ui.notify(f'You chose {result}')


@ui.page('/')
def index():
    with ui.header():
         ui.label("Text Coder and Decoder").classes("text-white text-2xl text-center w-full")

    ui.button('Choose file', on_click=pick_file, icon='folder')
    
    with ui.column():
        ui.input('Code word')
        ui.slider(min=0, max=1)
    with ui.row():
        ui.button('Encode')
        ui.button('Decode')
    ui.label("Selected file: <lorem>")
    with ui.row():
        ui.label("Output path: <lorem>")
        ui.button(icon="content_copy")

    
    with ui.footer():
        pass




if __name__ in {"__main__", "__mp_main__"}:
      ui.run(native=True)


