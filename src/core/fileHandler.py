"""
fileHandler.py

Class for text file handling: class FileHandler
o Responsible to read a plaintext .txt file (original message).
o Read a coded file (for decoding).
o Write the coded output file and the decoded output file.

"""

from pathlib import Path
from enum import Enum
import os

class FileType(Enum):
    UNKNOWN = 0
    TEXT = 1
    ENCRYPTED = 2


class FileHandler:


    def open(self, file_path) -> tuple[FileType, str]:
        # check file extension and treat it as plain or encrypted file
        suffix = Path(file_path).suffix

        print(suffix)
        if suffix == ".sect":
            file_text = self.open_coded_file(file_path)
            return FileType.ENCRYPTED, file_text
        else: # treat as a
            file_text = self.open_plain_text(file_path)
            return FileType.TEXT, file_text


    def open_plain_text(self, file_path):
        with open(file_path) as f:
            content = f.read()
            return content

    def open_coded_file(self, file_path):
        with open(file_path) as f:
            content = f.read()
            return content
    
    def save_text(self, file_path, content):
        "Saves file as a plain text file"
        with open(file_path, "w") as f:
            f.write(content)
    
    def save_encrypted_text(self, file_path, content, salt):
        "Saves file with additional data like salt"
        with open(file_path, "w") as f:
            f.write(content)

    def get_file_size(self, file_path) -> int:
        return os.path.getsize(file_path)