"""
CustomCipher.py

Author: Moxidus


"""
import numpy as np
import base64
import random

HASH_CONSTANTS = (0x243F6A88, 0x85A308D3, 0x13198A2E, 0x03707344, 0xA4093822, 0x299F31D0, 0x082EFA98, 0xEC4E6C89) # First hexadecimal digits of pi
SALT_CHAR_SET = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
MASK_32 = 0xFFFFFFFF
MAGIC_PRIME = 0x9e3779b1 # taken from https://stdlib.fortran-lang.org/sourcefile/stdlib_hash_32bit_nm.fypp.html
SIZE = 8

class WrongPassKeyException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class CustomCipher:
    """
    Class Custom Cipher symmetric encryption algorithm 
    * it encrypts text using a passkey by XOR-ing each byte against a key stream derived from the passkey and randomly generated salt
    * loosely inspired by ChaCha20
    * The cipher includes PKCS#7-style padding
    * checksum for passkey verification
    * and per-block key rotation for added diffusion.
    * Use encode() to encode
    * Use decode() to decode
    
    """


    def encode(self, passkey: str, text : str, custom_salt: str = None):
        """
        Custom Cipher encoder
        """
            
        if custom_salt:
            if len(custom_salt) != 8:
                raise Exception("Invalid salt length")
            
            salt_base = custom_salt
        else:
            salt_base = self.new_salt()

        hashed_key = self.heavy_text_hash(passkey)
        simple_salt = self.heavy_text_hash(salt_base)
        test_key_list = self.generate_lock(hashed_key, simple_salt)

        text_byte_array = bytearray(text, 'utf-8')


        # padding the text to round it to divisible by 64, borrowed from PKCS#7 padding
        #  otherwise my algorithm breaks because of the checksum
        text_byte_array_rest = 64 - (len(text_byte_array) % 64)
        padding = bytearray([text_byte_array_rest]*(text_byte_array_rest-1))
        padding.append(text_byte_array_rest)

        # add padding to make it divisible by 64
        text_byte_array += padding 
        # print(text_byte_array)

        # we are adding check sum of the original message at the end to check if the encryption was succesfull
        check_sum = self.heavy_byte_hash(text_byte_array)
        text_byte_array += check_sum

        # print(text_byte_array)

        byte_list = bytearray()


        # XOR ECRYPTION
        for index, x in enumerate(text_byte_array):

            # after every 64 bytes we refresh the lock to prevent repeating patterns
            if index % 64 == 0 and index != 0:
                text_sect = text_byte_array[index - 64:index]
                # print(f"text secret {index}:",text_sect)
                simple_salt = self.heavy_byte_hash(text_sect, 10) # take last 8 unencrypted bytes and use it to generate new key     
                # print("result salt",simple_salt)   
                test_key_list = self.generate_lock(hashed_key, simple_salt)

            
            locked = x^test_key_list[index % len(test_key_list)]
            byte_list.append(locked)

        # merge salt to the encoded result
        return base64.b64encode(bytes(byte_list)).decode('utf-8') + salt_base
    
    def new_salt(self):
        "Generates new random salt so that same password and content don't produce same encryption"
        salt_base = random.choices(SALT_CHAR_SET, k=8)
        return "".join(salt_base)

    def decode(self, passkey: str, encrypted_base64: str) -> str:
        """
        Custom Cipher encoder
        """

        salt_base = encrypted_base64[-8:]
        encrypted_base64 = encrypted_base64[:-8]
        

        hashed_key = self.heavy_text_hash(passkey)
        simple_salt = self.heavy_text_hash(salt_base)
        test_key_list = self.generate_lock(hashed_key, simple_salt)

        encrypted_byte_list = base64.b64decode(encrypted_base64)

        byte_list = bytearray()

        for index, x in enumerate(encrypted_byte_list):
            
            # after every 64 bytes we refresh the lock to prevent repeating patterns
            if index % 64 == 0 and index != 0:
                text_sect = byte_list[index - 64:index]
                # print(text_sect)
                simple_salt = self.heavy_byte_hash(text_sect, 10) # take last 8 unencrypted bytes and use it to generate new key 
                test_key_list = self.generate_lock(hashed_key, simple_salt)

            # XORING
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

        # if check sum is wrong the decryption failed most likely because of wrong password
        if check_sum != new_check_sum:
            raise WrongPassKeyException("check sum failed")

        return plain_text.decode("utf-8")

    def generate_lock(self, passkey , salt):
        """
        Generates lock array of size 64 bytes, this lock is used t encrypt the data.
        Lock is regenerated with last unencrypted data section as a input.
        This way even if attacker knew the part of the message they could't use it to decode rest of the message
        """
        passkey_list = passkey

        # this section is slightly inspired by CHACHA20 it uses matrix of data that is arithmetically mixed until its hard to predict what kind of out put input produces
        lock_structure = np.matrix(
            [list(bytearray("SafePass", 'utf-8')),
             [5,9,7,8,74,6,7,4],
             [9,120,154,12,9,10,11,12],
             [13,111,125,16,45,54,215,136],
             [174,114,47,56,17,18,65,46],
             passkey_list,[13,14,15,16,43,14,195,16],
             salt], dtype=np.uint32)

        # mixing
        for _ in range(4):
            # we module by a prime number to prevent repeating numbers
            lock_structure = (lock_structure @ lock_structure) % 251

        lock = lock_structure.flatten().tolist()[0]

        return lock
  
    def heavy_byte_hash(self, data: bytearray, iterations: int = 100_000):
        """Heavy hash that supports Byte array"""
        result = self.hash_key(data)
        for _ in range(iterations):
            result = self.hash_key(result)
        return result


    def heavy_text_hash(self, text: str, iterations: int = 100_000):
        """For security purposes hash functions should be difficult to calculate so as a simple fix we recalculate it 100_000 times"""
        data = bytearray(text.encode('utf-8'))
        result = self.hash_key(data)
        for _ in range(iterations):
            result = self.hash_key(result)
        return result


    def hash_key(self, data: bytearray):
        """
        simple hashing function
        * initializes list of digits of PI in hexadecimal
        * mixes in the key data while rotating the binary numbers
        * it uses diffusing to distribute and blur the values from each list element into each other
        * at the end we fold the state data into desired byte size which is currently set to 8
        """
        # initial state 
        state = list(HASH_CONSTANTS)

        # mixing
        for index, byte in enumerate(data):
            state_index = index % len(state)

            state[state_index] ^= byte
            state[state_index] = (((state[state_index] << 3) & ~0b111) | ((state[state_index] >> 29) & 0b111)) & MASK_32 # rotating via left and right shift
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




# test part
if __name__ == "__main__":
    coder = CustomCipher()
    original = "Why did you make me do this? You're fighting so you can watch everyone around you die! Think, Mark!"*5000
    print("Start test")
    print("origin  text:", original)
    encoded_result = coder.encode("secure password", original, custom_salt="abcdefgh")

    print("Encoded text:", encoded_result)

    try:
        res2 = coder.decode("secure password", encoded_result)
    except:
        print("Wrong password!")
    else:
        print("Decoded text:", res2)
        
        print(f"size compare ORIG {len(original)} ENC {len(encoded_result)}")
