
from core.coder import Coder

def test_encoding():
    coder = Coder()
    result = coder.encode("","hello world")

    assert result == "mjqqt btwqi"
