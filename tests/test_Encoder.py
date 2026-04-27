
from core.coder import Coder, EncryptionType

def test_encoding_caesar():
    coder = Coder()
    result = coder.encode("password 1","hello world", EncryptionType.CAESAR_CIPHER)

    assert result == "jgnnq yqtnf"

def test_encoding_custom():
    coder = Coder()
    result = coder.encode("password 1","hello world", EncryptionType.CUSTOM_CIPHER, custom_salt="abcdef") # TODO: need a way to force constant salt

    assert result == 'qiAgG10TXfvzJd5oliiRWWyZ3v8hnYgdSGzgGrhzmSexje1KKc8qiB76WENHCTjEct/XbiHWZfUvPGiui12n4FN7l0zsh9ijabcdef'
