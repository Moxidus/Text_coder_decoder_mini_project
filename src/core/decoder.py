"""
decoder.py
"""

from core.CaesarCipher import CaesarCipher
from core.CustomCipher import CustomCipher


class Decoder:
    """
    Class for Data Decoding: class Decoder
    * This class calls the appropriate decoder based on the file type
    * Automatically removes file type designator CAES for caesar and CUST for custom
    """
    def __init__(self):
        self.caesarCoder = CaesarCipher()
        self.customCoder = CustomCipher()

    def decode(self, passkey: str, encrypted_base64) -> str:
        ""
        encryption_type = encrypted_base64[-4:]
        encrypted_base64 = encrypted_base64[:-4]
        if encryption_type == "CAES":
            shift = self.caesarCoder.string_to_shift(passkey)
            result = self.caesarCoder.decode(shift, encrypted_base64)
            return result
        elif encryption_type == "CUST":
            result = self.customCoder.decode(passkey, encrypted_base64)
            return result
        else:
            Exception("Unknown Encryption type")


