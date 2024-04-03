# Project 0: RSA-based Public-key Certification Authority (CA)
# Contributors: Shubham Sharma (2021099), Parveen (2021079)

from math import gcd
from sympy import mod_inverse
from base64 import b64encode, b64decode
from Crypto.Util.number import getPrime
from Crypto.Util.Padding import pad, unpad


class RSA:
    def __init__(self, key_size):

        self.p = 0
        self.q = 0
        self.n = 0
        self.e = 0
        self.d = 0
        self.phi = 0
        self.key_size = key_size
        self.block_size_map = {128: 8, 256: 16, 512: 32, 1024: 64, 2048: 128}
        self.block_length = self.block_size_map[self.key_size]


    def generate_key_pair(self):

        '''Generating the public and private key pair.'''

        self.p, self.q = self.generate_p_q()

        '''Calculating the modulus and 
            Euler's totient function phi(n).'''

        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)

        '''Generating the public and 
            private exponents e and d.'''

        self.e = self.generate_e()
        self.d = mod_inverse(self.e, self.phi)

        return (self.e, self.n), (self.d, self.n)
    

    def encrypt(self, public_key, message):

        '''Extracting the exponent and modulus from the public key.'''

        e, n = public_key
        encrypted_message = ""

        '''Encrypting the message block by block and encoding it in base64 format.'''

        for i in range(0, len(message), self.block_length):

            '''Padding the message to make it of the same length as the block size.
                Converting the padded message to integer and then encrypting it using the public key.'''

            power_raised = pow(int.from_bytes(pad(message[i : i + self.block_length].encode("utf-8"), self.block_length), "big"), e, n)

            '''Converting the encrypted integer to bytes and then encoding it in base64 format.
                Appending the encoded message to the encrypted message.'''
            
            encrypted_message += b64encode(power_raised.to_bytes(power_raised.bit_length() // 8 + 1, "big")).decode("ascii") + " "
     
        return encrypted_message
    

    def decrypt(self, private_key, encrypted_message):
        
        '''Extracting the exponent and modulus from the private key.'''

        d, n = private_key
        decrypted_message = ""
    
        '''Decrypting the message block by block and decoding it from base64 format.'''

        for message in encrypted_message.split(" ")[0 : -1]:

            '''Decoding the message from base64 format and then converting it to integer.'''

            power_raised = pow(int.from_bytes(b64decode(message), "big"), d, n)

            '''Converting the decrypted integer to bytes and then unpadding it to get the original message.
                Decoding the original message to utf-8 format and appending it to the decrypted message.'''

            decrypted_message += unpad(power_raised.to_bytes(power_raised.bit_length() // 8 + 1, "big"), self.block_length).decode("utf-8")

        return decrypted_message
    

    def generate_p_q(self):

        '''Generating two prime numbers p and q of the specified key size.'''

        p = getPrime(self.key_size)
        q = getPrime(self.key_size)

        '''Checking if the generated prime numbers are equal or not. 
            If equal, then generating new prime numbers.'''

        return p, q if p != q else self.generate_p_q()
    

    def generate_e(self):

        '''Generating the public exponent e 
            such that it is coprime with phi(n).'''

        e = 2

        while gcd(e, self.phi) != 1:
            e += 1

        return e
