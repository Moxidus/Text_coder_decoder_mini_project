"""
fileHandler.py

Class for text file handling: class FileHandler
o Responsible to read a plaintext .txt file (original message).
o Read a coded file (for decoding).
o Write the coded output file and the decoded output file.

"""



class FileHandler:


    def open_plain_text(self, file_path):
        with open(file_path) as f:
            content = f.read()

            return content

    
    def open_coded_file(self, file_path):
        raise NotImplementedError()