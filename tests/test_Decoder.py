
from core.decoder import Decoder

def test_decoding():
    coder = Decoder()
    result = coder.decode("","mjqqt btwqi")

    assert result == "hello world"
