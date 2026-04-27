"""
POP up dialog that lets you save files in windows.

Based on https://github.com/zauberzeug/nicegui/blob/main/examples/local_file_picker/local_file_picker.py
but customized
"""

import platform
from pathlib import Path
from nicegui import events, ui
from core.fileHandler import FileType
from ui.PopUpYesNo import popUpYesNo


# windows only dependencies
IS_WINDOWS = platform.system() == 'Windows'
if IS_WINDOWS:
    import winreg
    import win32api


class localFileSaver(ui.dialog):
    """
    This is a simple file Saver that allows you to save a file to the local filesystem where NiceGUI is running.
    """
    def __init__(self, file_type: FileType) -> None:
        super().__init__()
        self.path = self.get_desktop_path()
        self.file_suffix = "sect" if file_type == FileType.ENCRYPTED else "txt"

        with self, ui.card():

            self.add_drives_toggle()
            self.grid = ui.aggrid({
                'columnDefs': [{'field': 'name', 'headerName': 'File'}],
                'rowSelection': {
                    'mode': 'singleRow', # allow only one file to be selected
                    'checkboxes': False,
                    'hideDisabledCheckboxes': True,
                    }
                }, html_columns=[0] # allows html tags to be rendered 
                ).classes('w-96').on('cellDoubleClicked', self.handle_double_click).on('cellClicked', self.handle_click)


            with ui.row().classes('w-full justify-end'):
                self.input_field = ui.input(label="file name:", suffix=self.file_suffix)
                ui.button('Cancel', on_click=self.close).props('outline')
                ui.button('Ok', on_click=self._handle_ok)
        
        self.update_grid()

    def get_desktop_path(self) -> Path:
        if IS_WINDOWS: # I love how unevenly complicated this is :]
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
            desktop = winreg.QueryValueEx(key, 'Desktop')[0]
            return Path(desktop)

    def add_drives_toggle(self):
        "Adds windows drives as buttons"
        if IS_WINDOWS: #  TODO: implement linux and mac support
            drives = win32api.GetLogicalDriveStrings().split('\000')[:-1] # lists all drives
            self.drives_toggle = ui.toggle(drives, value=drives[0], on_change=self.update_drive)

    def update_drive(self):
        "Handles drive change"
        self.path = Path(self.drives_toggle.value).expanduser() # expands ~ to actually directory
        self.update_grid()

    def update_grid(self) -> None:
        paths = list(self.path.glob("*." + self.file_suffix)) # returns all files of supported file type
        dirs = [p for p in self.path.iterdir() if p.is_dir()] # returns all folders 
        paths += dirs

        paths.sort(key=lambda p: p.name.lower()) # sort by name
        paths.sort(key=lambda p: not p.is_dir()) # show directories first

        # render folders and files
        self.grid.options['rowData'] = [
            {
                'name': f'📁 <strong>{p.name}</strong>' if p.is_dir() else p.name, # using emojis as icons
                'path': str(p),
            }
            for p in paths
        ]
        self.grid.update() # force update

    async def handle_double_click(self, e: events.GenericEventArguments) -> None:
        selected = Path(e.args['data']['path'])
        if selected.is_dir():
            self.path = selected
            self.update_grid() # dive into folder
        else:
            # check if file exists
            if Path(selected).exists():
                ok = await popUpYesNo(f"File '{selected.name}' already exists, do you you want to overwrite it?")
                if not ok:
                    return

                self.submit(selected) # submit selected

    def handle_click(self, e: events.GenericEventArguments) -> None:
        selected = Path(e.args['data']['path'])
        if not selected.is_dir():
            file_name = selected.name.removesuffix(selected.suffix)
            self.input_field.value = file_name

    async def _handle_ok(self):
        file_name = self.input_field.value + "." + self.file_suffix # build file name + suffix
        full_path = self.path.joinpath(file_name) # build full file path

        # check if file exists
        if full_path.exists():
            ok = await popUpYesNo(f"File '{file_name}' already exists, do you you want to overwrite it?")
            if not ok:
                return
            
        self.submit(full_path) # submit selected
    