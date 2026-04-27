"""
CustomCipher.py

Author: Moxidus

"""
import numpy as np
import base64
import random


class WrongPassKeyException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class customCipher:
    """
    Class implementing simple Custom cipher that is little bit inspired by ChaCha20.
    * Use encode() to encode
    * Use decode() to decode
    """
    HASH_CONSTANTS = (0x243F6A88, 0x85A308D3, 0x13198A2E, 0x03707344, 0xA4093822, 0x299F31D0, 0x082EFA98, 0xEC4E6C89) # First hexadecimal digits of pi

    def encode(self, passkey: str, text : str):


        hashed_key = self.heavy_text_hash(passkey)
        salt_base = self.new_salt()
        simple_salt = self.heavy_text_hash(salt_base)
        test_key_list = self.generate_lock(hashed_key, simple_salt)

        text_byte_array = bytearray(text, 'utf-8')


        # padding the text to round it to divisible by 64, borrowed from PKCS#7 padding
        text_byte_array_rest = 64 - (len(text_byte_array) % 64)
        # print("padding_size", text_byte_array_rest)
        padding = bytearray([text_byte_array_rest]*(text_byte_array_rest-1))
        padding.append(text_byte_array_rest)


        text_byte_array += padding # add padding to make it divisible by 64
        # print(text_byte_array)

        check_sum = self.heavy_byte_hash(text_byte_array)

        text_byte_array += check_sum

        # print(text_byte_array)

        byte_list = bytearray()

        for index, x in enumerate(text_byte_array):

            if index % 64 == 0 and index != 0:
                text_sect = text_byte_array[index - 64:index]
                # print(f"text secret {index}:",text_sect)
                simple_salt = self.heavy_byte_hash(text_sect, 10) # take last 8 unencrypted bytes and use it to generate new key     
                # print("result salt",simple_salt)   
                test_key_list = self.generate_lock(hashed_key, simple_salt)

            
            locked = x^test_key_list[index % len(test_key_list)]
            byte_list.append(locked)

        return base64.b64encode(bytes(byte_list)).decode('utf-8'), salt_base
    
    def new_salt(self):
        salt_base = random.randbytes(8)
        salt_base = bytearray([(x % 106) + 21  for x in salt_base])
        return salt_base.decode("utf-8")

    def decode(self, passkey: str, encrypted_base64, salt_base) -> str:

        hashed_key = self.heavy_text_hash(passkey)
        simple_salt = self.heavy_text_hash(salt_base)
        test_key_list = self.generate_lock(hashed_key, simple_salt)

        encrypted_byte_list = base64.b64decode(encrypted_base64)

        byte_list = bytearray()

        for index, x in enumerate(encrypted_byte_list):
            if index % 64 == 0 and index != 0:
                text_sect = byte_list[index - 64:index]
                # print(text_sect)
                simple_salt = self.heavy_byte_hash(text_sect, 10) # take last 8 unencrypted bytes and use it to generate new key 
                test_key_list = self.generate_lock(hashed_key, simple_salt)

            locked = x^test_key_list[index % len(test_key_list)]
            byte_list.append(locked)

        # print("Decrypted byte List:",byte_list)

        check_sum = byte_list[-8:]
        text_plus_padding = byte_list[:-8]

        # print("check sum:",check_sum)
        # print("payload with padding:", text_plus_padding)
        
        decoded_payload_plus_padding = text_plus_padding
        new_check_sum = self.heavy_byte_hash(decoded_payload_plus_padding)
        # print("new check sum:", new_check_sum)

        padding_size = text_plus_padding[-1:][0]
        # print("padding_size", padding_size)
        plain_text = text_plus_padding[:-padding_size]

        if check_sum != new_check_sum:
            raise WrongPassKeyException("check sum failed")

        return plain_text.decode("utf-8")

    def generate_lock(self, passkey , salt):
        passkey_list =passkey

        lock_structure = np.matrix([list(bytearray("SafePass", 'utf-8')),[5,9,7,8,74,6,7,4],[9,120,154,12,9,10,11,12],[13,111,125,16,45,54,215,136],[174,114,47,56,17,18,65,46],passkey_list,[13,14,15,16,43,14,195,16],salt], dtype=np.uint32)

        for i in range(4):
            lock_structure = (lock_structure @ lock_structure) % 251

        lock = lock_structure.flatten().tolist()[0]

        return lock
  
    def heavy_byte_hash(self, data: bytearray, iterations: int = 100_000):
        result = self.hash_key(data)
        for _ in range(iterations):
            result = self.hash_key(result)
        return result


    def heavy_text_hash(self, text: str, iterations: int = 100_000):
        data = bytearray(text.encode('utf-8'))
        result = self.hash_key(data)
        for _ in range(iterations):
            result = self.hash_key(result)
        return result


    def hash_key(self, data: bytearray):
        MASK_32 = 0xFFFFFFFF
        MAGIC_PRIME = 0x9e3779b1 # taken from https://stdlib.fortran-lang.org/sourcefile/stdlib_hash_32bit_nm.fypp.html
        SIZE = 8

        # initial state 
        state = list(self.HASH_CONSTANTS)

        # mixing
        for index, byte in enumerate(data):
            state_index = index % len(state)

            state[state_index] ^= byte
            state[state_index] = (((state[state_index] << 3) & ~0b111) | ((state[state_index] >> 29) & 0b111)) & MASK_32 # rotate
            state[state_index] = (state[state_index] * MAGIC_PRIME) & MASK_32
            state[(state_index+1) % 8] ^= state[state_index]  
        
        # diffusing 
        for index, byte in enumerate(state):
            state[(index+1) % 8] ^= byte  
            state[index] = (byte * MAGIC_PRIME) & MASK_32
            state[(index-1) % 8] ^= byte  


        output = bytearray([0] * SIZE)

        # minimizing state to desired size
        for byte_shift in range(4):
            for index, byte in enumerate(state):
                output_index = index % len(output)
                output[output_index] ^= (byte >> (byte_shift*8)) & 0xFF

        return output





if __name__ == "__main__":
    coder = customCipher()
    # simple_salt = coder.heavy_text_hash("salt_base")
    # hashed_key = coder.heavy_text_hash("passkey")
    # lock = coder.generate_lock(hashed_key, simple_salt)
    # print(lock)
    # print(len(lock))


    original = "Why did you make me do this? You're fighting so you can watch everyone around you die! Think, Mark! You'll outlast every fragile, insignificant being on this planet. You'll live to see this world crumble to dust and blow away! Everyone and everything you know will be gone! What will you have after 500 years?"*5000
    print("Start test")
    print("origin  text:", original)
    res, salt_base = coder.encode("secure password", original)
    print("Encoded text:", res)
    print()
    try:
        res2 = coder.decode("secure password", res, salt_base)
    except:
        print("Wrong password!")
    else:
        print("Decoded text:", res2)
