from number_theory import generate_probable_prime, fast_lcm, iter_fast_gcd, power_mod, mod_inverse
import random

class RSA_Encrypt():

    __BIT_DIFF = 256

    def __init__(self, bit_leng):
        self.__prime1 = 0
        self.__prime2 = 0
        self.__public_key = 0
        self.__private_key = 0
        self.__number = 0
        self.__bits = bit_leng//2
        self.__generated = False

    # Generate the primes, public and private key, and N
    def generate_encryption(self):
        # Generate first probable prime
        self.__prime1 = generate_probable_prime(self.__bits)
        # Generate sencond probable prime, but assign it only if its 
        # far apart from the first one. If the primes are close, N can be factored
        # using Fermat factorization.
        temp_prime = generate_probable_prime(self.__bits)
        while (self.__prime1 - temp_prime).bit_length() < self.__BIT_DIFF:
            temp_prime = generate_probable_prime(self.__bits)
        self.__prime2 = temp_prime
        # __number is the multiple of two primes. __number would 
        # be extremely difficult to factor if we didn't know the primes.
        self.__number = self.__prime1 * self.__prime2
        self.__publ_priv()
        self.__generated = True
    
    #Generate the public and private keys
    def __publ_priv(self):
        # Find the universal exponent of unit group mod __number
        univ_exp = fast_lcm(self.__prime1 - 1,self.__prime2 - 1)
        # Get a random number in range of univ_exp. Only assign to
        # the public_key if it is relatively prime to univ_exp
        temp_key = random.randrange(random.getrandbits(self.__BIT_DIFF), univ_exp)
        while iter_fast_gcd(univ_exp,temp_key) != 1:
            temp_key = random.randrange(random.getrandbits(self.__BIT_DIFF), self.__number)
        self.__public_key = temp_key
        # The private key is the inverse of public key mod univ_exp
        self.__private_key = mod_inverse(self.__public_key, univ_exp)

    # If the values are generated we only want to send the public key and 
    # __number (the product of both primes)
    def send_public_key(self):
        if self.__generated:
            return {'public_key': self.__public_key, 'mod': self.__number}
        else:
            return None

    # Encrypts message being passed in
    def encrypt_message(self, message, public_key, mod_num):
        message = message.encode('utf-8')
        return [power_mod(x, public_key, mod_num) for x in message]

    # Decrypte message with your private key
    def decrypt_message(self, enc_message):
        if self.__generated:
            return ''.join(chr(power_mod(x, self.__private_key, self.__number)) for x in enc_message)
        else: 
            return None
