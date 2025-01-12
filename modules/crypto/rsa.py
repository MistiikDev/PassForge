import random

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1


def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def generate_prime(min_value, max_value):
    while True:
        num = random.randint(min_value, max_value)
        if is_prime(num):
            return num


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def number_to_word(num):
    """Convert a number to a 'word' using base-26 encoding (A-Z)."""
    result = []
    while num > 0:
        num -= 1  # Shift to make it 0-based
        result.append(chr(num % 26 + 65))  # Map to A-Z
        num //= 26
    return ''.join(reversed(result))  # Reverse the list to get the correct order


def word_to_number(word):
    """Convert a 'word' back to a number."""
    result = 0
    for char in word:
        result = result * 26 + (ord(char) - 65 + 1)  # Reverse the mapping
    return result


class RSAEncryption:
    def __init__(self, max_length):
        self.messageMaxLength = max_length

        return

    @staticmethod
    def generate_keys():
        p = generate_prime(100, 200)
        q = generate_prime(100, 200)

        n = p * q
        phi_n = (p - 1) * (q - 1)

        e = 3
        while gcd(e, phi_n) != 1:
            e += 2

        d = mod_inverse(e, phi_n)

        return (e, n), (d, n)

    @staticmethod
    def encrypt(message, key):
        if not key:
            raise ValueError("Missing the key in cypher")

        public_key = key[0]

        if not public_key:
            raise Exception("Error while unpacking key!")

        e, n = public_key
        ## Transform the int array into a string of characters

        encrypted_array = [pow(ord(char), e, n) for char in message]
        encrypted_message = ''.join(number_to_word(num) + '.' for num in encrypted_array).strip('.')

        return encrypted_message

    @staticmethod
    def decrypt(encrypted_message, key):
        if not key:
            raise ValueError("Missing the key in cypher")

        private_key = key[1]

        if not private_key:
            raise Exception("Error while unpacking key!")

        d, n = private_key

        decrypted_array = [word_to_number(word) for word in encrypted_message.split('.')]
        decrypted_message = ''.join([chr(pow(char, d, n)) for char in decrypted_array])
        
        return decrypted_message
