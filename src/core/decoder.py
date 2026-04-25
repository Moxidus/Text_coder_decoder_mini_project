"""
decoder.py

Class for Data Decoding: class Decoder
o This class will recover the original message from the coded file using the
supplied codeword.
o The coded file must include a code verification value that is checked during
decoding to confirm the codeword is correct.
o If a wrong codeword is supplied, decoding must fail clearly, must not generate
a decoded output file, and must display an appropriate error status in the UI

Curretly example Ceasar cypher implemented
"""

class Decoder:
    default_shift = 5
    def __init__(self):
        pass
    

    def decode(self, passkey: str, text : str) -> str:
        text = text.lower()

        encrypted_text = ""

        for char in text:
            
            if not char.isalpha():
                encrypted_text += char
                continue

            ascii_val = ord(char) - self.default_shift
            if ascii_val < ord("a"):
                ascii_val += 26
            encrypted_text += chr(ascii_val)

        return encrypted_text



