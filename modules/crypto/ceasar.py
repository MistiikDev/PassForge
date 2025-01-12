alphabet = [
    'a', 'b', 'c', 'd', 'e', 'f', 
    'g', 'h', 'i', 'j', 'k', 'l', 
    'm', 'n', 'o', 'p', 'q', 'r', 
    's', 't', 'u', 'v', 'w', 'x', 
    'y', 'z'
]

numbers = [
    '0',
    '1', '2', '3',
    '4', '5', '6',
    '7', '8', '9'
]

def get_letter_shift(letter, shift):
    assert type(letter) == str
    assert type(shift) == int

    i_letter_index = alphabet.index(letter)
    o_letter_index = i_letter_index

    if i_letter_index:
        o_letter_index = i_letter_index + shift
        o_letter_index %= 26

    return alphabet[o_letter_index]

def get_integer_shift(integer, shift):
    assert type(integer) == int
    assert type(shift) == int

    return (integer + shift) % 10


class CesarEncryption:
    def __init__(self, max_length):
        self.signature = "Caesar Encryption"
        self.messageMaxLength = max_length

        return

    @staticmethod
    def encrypt(message, key):
        if not key:
            raise ValueError("Missing the key in cypher")

        key = key[0]

        if not key:
            raise Exception("Error while unpacking key!")

        message = str(message)
        assert type(message) == str, "Something went wrong, message must be a string"

        ## First Encryption Caesar
        final_hash = ""
        first_hash = list(message)
        j = 0

        for element in list(message):
            overwrite = ""

            l_element = element.lower()
            is_letter = (l_element in alphabet)
            is_number = (l_element in numbers)

            if is_letter:
                overwrite = get_letter_shift(l_element, key)
            elif is_number:
                overwrite = get_integer_shift(int(l_element), key)
            else:
                overwrite = str(l_element)
            
            first_hash[j] = element.isupper() and str(overwrite).upper() or str(overwrite).lower()
            j += 1

        for element in first_hash:
            final_hash += element

        return final_hash


    @staticmethod
    def decrypt(_hash, key):
        if not key:
            raise ValueError("Missing the key in cypher")

        key = key[0]

        if not key:
            raise Exception("Error while unpacking key!")

        original = []
        j = 0

        for element in list(_hash):
            overwrite = ""

            l_element = element.lower()
            is_letter = (l_element in alphabet)
            is_number = (l_element in numbers)

            if is_letter:
                overwrite = get_letter_shift(l_element, -key)
            elif is_number:
                overwrite = get_integer_shift(int(l_element), -key)
            else:
                overwrite = str(l_element)
            
            original.insert(j,  element.isupper() and str(overwrite).upper() or str(overwrite).lower())
            j += 1

        final_original = ""

        for element in original:
            final_original += str(element)

        return final_original

    def close(self):
        return

