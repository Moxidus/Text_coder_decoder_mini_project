"""
decoder.py

Class for Data Decoding: class Decoder
o This class will recover the original message from the coded file using the
supplied codeword.
o The coded file must include a code verification value that is checked during
decoding to confirm the codeword is correct.
o If a wrong codeword is supplied, decoding must fail clearly, must not generate
a decoded output file, and must display an appropriate error status in the UI

Currently example Caesar cipher implemented
"""

from core.CaesarCipher import caesarCipher
from core.CustomCipher import customCipher
from core.coder import EncryptionType


class Decoder:
    def __init__(self):
        self.caesarCoder = caesarCipher()
        self.customCoder = customCipher()

    def decode(self, passkey: str, encrypted_base64, encryption_type: EncryptionType = EncryptionType.CUSTOM_CIPHER) -> str:

        if encryption_type == EncryptionType.CAESAR_CIPHER:
            shift = self.caesarCoder.string_to_shift(passkey)
            result = self.caesarCoder.decode(shift, encrypted_base64)
            return result
        else:
            result = self.customCoder.decode(passkey, encrypted_base64)
            return result



