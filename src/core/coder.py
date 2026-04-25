"""
coder.py

Class for Data Coding (Encoding)

-This class will implement algorithm/method to Encode (code) the input text
using a codeword to transform it into a coded text file that is not humanreadable as plain text, but is fully reversible using the same software and the
correct codeword. Simple character substitution alone is not sufficient.

Current implementation is just caesar cipher as a placeholder as a placeholder

"""


class Coder:
    default_shift = 5
    def __init__(self):
        pass

    def encode(self, passkey: str, text : str) -> str:
        text = text.lower()

        encrypted_text = ""

        for char in text:
            if not char.isalpha():
                encrypted_text += char
                continue

            ascii_val = ord(char) + self.default_shift
            if ascii_val > ord("z"):
                ascii_val -= 26
            encrypted_text += chr(ascii_val)

        return encrypted_text




if __name__ == "__main__":
    coder = Coder()

    print("Start test")
    res = coder.encode("", "hello world")
    print("Encoded text", res)

    pass
