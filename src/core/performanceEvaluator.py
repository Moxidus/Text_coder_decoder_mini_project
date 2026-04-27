"""
Class for performance evaluation: class PerformanceEvaluator
To evaluate system performance and provide numerical evidence such as:
o Original message length (characters)
o Coded file size vs original file size (overhead)
o Decode success/failure indicator (and any additional metric you propose)
o A minimum recommended metric is File Expansion Ratio (FER):
FER (%) = (Coded file size / Original file size) × 100

"""
from core.fileHandler import FileHandler
from dataclasses import dataclass

@dataclass
class PerformanceStats:
    """Statistics on encoding performance"""
    plain_text_size: int
    plain_text_length: int
    coded_text_size: int
    coded_text_length: int
    fer: float


class PerformanceEvaluator:
    def __init__(self):
        self.file_handler = FileHandler()


    def get_performance(self, encoded_path, decoded_path) -> PerformanceStats:
        """Method that calculates and returns basic stats about the encoding"""
        
        plain_text_size = self.file_handler.get_file_size(decoded_path)
        coded_text_size = self.file_handler.get_file_size(encoded_path)


        plain_text_length = self.file_handler.open_plain_text(decoded_path)
        coded_text_length = self.file_handler.open_coded_file(encoded_path)

        fer = (coded_text_size / plain_text_size) * 100

        print("Stats:")
        print("plain text size:", plain_text_size)
        print("plain text length:", plain_text_length)
        print("coded text size:", coded_text_size)
        print("plain text length:", coded_text_length)
        print("File expansion ratio:", fer)

        stats = PerformanceStats(plain_text_size, plain_text_length, coded_text_size, coded_text_length, fer)

        return stats

