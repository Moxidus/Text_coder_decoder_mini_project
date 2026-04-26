"""
fileHandler.py

Class for text file handling: class FileHandler
o Responsible to read a plaintext .txt file (original message).
o Read a coded file (for decoding).
o Write the coded output file and the decoded output file.

"""

from pathlib import Path
from enum import Enum

class FileType(Enum):
    UNKNOWN = 0
    TEXT = 1
    ENCRYPTED = 2


class FileHandler:


    def open(self, file_path) -> tuple[FileType, str]:
        # check file extension and treat it as plain or encrypted file
        suffix = Path(file_path).suffix

        if suffix == "sect":
            raise NotImplementedError("sect files are not supported yet")
        else: # treat as a
            file_text = self.open_plain_text(file_path)
            return FileType.TEXT, file_text


    def open_plain_text(self, file_path):
        with open(file_path) as f:
            content = f.read()

            return content

    def open_coded_file(self, file_path):
        raise NotImplementedError()