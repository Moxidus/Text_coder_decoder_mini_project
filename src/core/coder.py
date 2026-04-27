"""
coder.py

Class for Data Coding (Encoding)

-This class will implement algorithm/method to Encode (code) the input text
using a codeword to transform it into a coded text file that is not human readable as plain text, but is fully reversible using the same software and the
correct codeword. Simple character substitution alone is not sufficient.

"""
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

    def encode(self, passkey: str, text: str, encryption_type: EncryptionType = EncryptionType.CUSTOM_CIPHER, custom_salt: str = None) -> str:

        print(f"Starting {encryption_type} Encryption:", text)

        if encryption_type == EncryptionType.CAESAR_CIPHER:
            shift = self.caesarCoder.string_to_shift(passkey)
            result = self.caesarCoder.encode(shift, text)
            result += "CAES" # append encryption type label
            return result
        else:
            result = self.customCoder.encode(passkey, text, custom_salt)
            result += "CUST" # append encryption type label
            self.last_result = result # for multi threading
            return result
        



if __name__ == "__main__":
    coder = Coder()
