
from core.decoder import Decoder
from core.coder import EncryptionType



def test_decoding_caesar():
    coder = Decoder()
    result = coder.decode("password 1","jgnnq yqtnf", EncryptionType.CAESAR_CIPHER)

    assert result == "hello world"

def test_decoding_custom():
    coder = Decoder()
    result = coder.decode("password 1","3LIT0VjSogGTnydfZlz9hmuAoDiPDNFucny0E6J8Pnput1b+rTW1u/GcC9TdOaU/PBOhpFJ6RRItwCEE5MVe01N7l0zsh9ijabcdefgh", EncryptionType.CUSTOM_CIPHER)

    assert result == "hello world"
