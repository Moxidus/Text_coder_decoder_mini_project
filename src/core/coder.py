"""
coder.py

Class for Data Coding (Encoding)

-This class will implement algorithm/method to Encode (code) the input text
using a codeword to transform it into a coded text file that is not human readable as plain text, but is fully reversible using the same software and the
correct codeword. Simple character substitution alone is not sufficient.

"""

import numpy as np
import base64
from enum import Enum
from core.CaesarCipher import caesarCipher
from core.CustomCipher import customCipher

class EncryptionType(Enum):
    CAESAR_CIPHER = 1
    CUSTOM_CIPHER = 2


class Coder:
    def __init__(self):
        self.caesarCoder = caesarCipher()
        self.customCoder = customCipher()

    def encode(self, passkey: str, text : str, encryption_type: EncryptionType = EncryptionType.CUSTOM_CIPHER, custom_salt: str = None) -> str:
        if encryption_type == EncryptionType.CAESAR_CIPHER:
            shift = self.caesarCoder.string_to_shift(passkey)
            result = self.caesarCoder.encode(shift, text)
            return result
        else:
            result = self.customCoder.encode(passkey, text, custom_salt)
            return result

    def decode(self, passkey: str, encrypted_base64, encryption_type: EncryptionType = EncryptionType.CUSTOM_CIPHER) -> str:

        if encryption_type == EncryptionType.CAESAR_CIPHER:
            shift = self.caesarCoder.string_to_shift(passkey)
            result = self.caesarCoder.decode(shift, encrypted_base64)
            return result
        else:
            result = self.customCoder.decode(passkey, encrypted_base64, None)
            return result


if __name__ == "__main__":
    coder = Coder()
