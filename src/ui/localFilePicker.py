"""


Based on https://github.com/zauberzeug/nicegui/blob/main/examples/local_file_picker/local_file_picker.py
"""

import platform
from pathlib import Path
from nicegui import events, ui

IS_WINDOWS = platform.system() == 'Windows'

if IS_WINDOWS:
    import winreg
    import win32api


class localFilePicker(ui.dialog):

    def __init__(self) -> None:
        """Local File Picker

        This is a simple file picker that allows you to select a file from the local filesystem where NiceGUI is running.

        :param directory: The directory to start in.
        """
        super().__init__()
        self.path = self.get_desktop_path()

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
                ).classes('w-96').on('cellDoubleClicked', self.handle_double_click)


            with ui.row().classes('w-full justify-end'):
                ui.button('Cancel', on_click=self.close).props('outline')
                ui.button('Ok', on_click=self._handle_ok)
        
        self.update_grid()

    def get_desktop_path(self) -> Path:
        if IS_WINDOWS: # I love how unnecerly complicated this is :]
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
        self.path = Path(self.drives_toggle.value).expanduser() # expands ~ to actually dirrectory
        self.update_grid()

    def update_grid(self) -> None:
        paths = list(self.path.glob("*")) # returns all files in current directory
        paths.sort(key=lambda p: p.name.lower()) # sort by name
        paths.sort(key=lambda p: not p.is_dir()) # show directories first

        # render folders and files
        self.grid.options['rowData'] = [
            {
                'name': f'📁 <strong>{p.name}</strong>' if p.is_dir() else p.name,
                'path': str(p),
            }
            for p in paths
        ]
        self.grid.update() # force update

    def handle_double_click(self, e: events.GenericEventArguments) -> None:
        self.path = Path(e.args['data']['path'])
        if self.path.is_dir():
            self.update_grid() # dive into folder
        else:
            self.submit(str(self.path)) # open file

    async def _handle_ok(self):
        row = await self.grid.get_selected_row()
        self.submit(row) # submit selected