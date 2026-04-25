from pathlib import Path
from core.fileHandler import FileHandler

TEST_DIR = Path(__file__).parent
DATA_DIR = TEST_DIR / "data"



def test_reading_from_plain_file():
    input_file = DATA_DIR / "plainTextSample.txt"

    fileHandler = FileHandler()

    content = fileHandler.open_plain_text(input_file)
    
    assert content == "test data"