
from core.coder import Coder, EncryptionType

def test_encoding_caesar():
    coder = Coder()
    result = coder.encode("password 1","hello world", EncryptionType.CAESAR_CIPHER)

    assert result == "jgnnq yqtnfCAES"

def test_encoding_custom():
    coder = Coder()
    result = coder.encode("password 1","hello world", EncryptionType.CUSTOM_CIPHER, custom_salt="abcdefgh") # TODO: need a way to force constant salt

    assert result == "3LIT0VjSogGTnydfZlz9hmuAoDiPDNFucny0E6J8Pnput1b+rTW1u/GcC9TdOaU/PBOhpFJ6RRItwCEE5MVe01N7l0zsh9ijabcdefghCUST"
