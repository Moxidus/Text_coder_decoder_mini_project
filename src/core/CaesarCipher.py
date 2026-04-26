"""
CaesarCipher.py

Author: Moxidus
"""



class caesarCipher:
    """
    Class implementing simple Caesar cypher.
    * Use encode() to encode
    * Use decode() to decode
    * Use string_to_shift() to get shift from passkey
    """

    def encode(self, shift: int, text : str) -> str:
        """
        Simple Caesar cypher with custom shift
        * Non alphabetical characters are untouched
        * Capitalization is ignored
        Args:
            shift (int): Caesar shift value.
            text (str): text 
        Returns:
            str: Caesar cypher of the original text
        """
        # input validation
        if not self.is_valid_shift(shift):
            raise Exception("Shift can not be divisible by 26")

        # input formatting
        shift_normalized = self.normalize_shift(shift)
        text = text.lower()

        encrypted_text = ""

        for char in text:
            if not char.isalpha():
                encrypted_text += char
                continue

            ascii_val = ord(char) + shift_normalized
            if ascii_val < ord("a"):
                ascii_val += 26
            if ascii_val > ord("z"):
                ascii_val -= 26
            encrypted_text += chr(ascii_val)

        return encrypted_text
    
    def decode(self, shift: int, text : str) -> str:
        """
        Simple Caesar cypher with custom shift, non alpha characters are untouched
        Args:
            shift (int): Caesar shift value.
            text (str): text 
        Returns:
            str: Caesar cypher of the original text
        """
        return self.encode(-shift, text)
    
    def string_to_shift(self, passkey : str) -> int:
        """
        gives you a valid shift from passkey
        Args:
            passkey (str): passkey
        Returns:
            int: Normalized shift
        """
        shift = 0
        for letter in passkey:
            shift += ord(letter) & 0xFF

        if not self.is_valid_shift(shift):
            shift += 3 # magic number
        
        return self.normalize_shift(shift)
    
    def is_valid_shift(self, shift : int) -> bool:
        """
        Makes sure the shift is not divisible by 26
        Args:
            shift (int): Caesar shift value.
        Returns:
            bool: false if divisible by 26
        """
        return self.normalize_shift(shift) != 0
    
    def normalize_shift(self, shift : int) -> bool:
        """
        Normalizes shift to 0 - 26
        Args:
            shift (int): Caesar shift value.
        Returns:
            int: Normalized shift
        """
        return shift % 26
    
if __name__ == "__main__":
    cipher = caesarCipher()

    print(cipher.string_to_shift("0adsasdassdfghsfd gdfgsdf gsdfg sdfgsdfsd"))

    result = cipher.encode(5,"hello world")
    resultDec = cipher.decode(5,result)

    print(result)
    print("mjqqt btwqi") # expected
    print(result == "mjqqt btwqi")
    print(resultDec == result) # expected 
