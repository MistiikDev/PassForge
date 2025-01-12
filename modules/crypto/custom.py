import string
from math import sqrt
from random import choice
from time import time
from base64 import urlsafe_b64encode, urlsafe_b64decode


class CustomEncryption:
    def __init__(self, max_length):
        self.signature = "Custom Encryption"
        self.messageMaxLength = max_length

    @staticmethod
    def pad_message(message, padding, padding_entity=None):
        assert type(message) == str
        assert type(padding) == int

        if padding_entity is None:
            padding_entity = choice(string.ascii_letters)

        if len(message) > padding:
            return message, 0
        else:
            _missingChar = padding - len(message)
            padded_message = message + (padding_entity * _missingChar)
            return padded_message, _missingChar

    def encrypt(self, message, key):
        message = str(message)
        assert type(message) == str, "Something went wrong, message must be a string"

        padded_message, added_zeros = self.pad_message(message, self.messageMaxLength)
        # There will always be a difference between time when key was set and current time
        _previous_now = key[0]
        _now = time()

        _timeStamp = sqrt(_now * _now + _previous_now * _previous_now)
        split = str(_timeStamp).split(".")
        _saltBase = int(split[1])

        _processedSalt = str(((_saltBase % 10 + (_saltBase % 100 - _saltBase % 10))**2) % 100)

        first_round = f"{_processedSalt[-1]}{padded_message}{_processedSalt[0]}{added_zeros:02}"
        second_round = urlsafe_b64encode(bytes(first_round, "utf-8"))

        return second_round.decode("utf-8")

    @staticmethod
    def decrypt(_hash, key):
        decoded64 = urlsafe_b64decode(_hash)
        original_data = list(decoded64.decode("utf-8"))

        # Extract padding metadata
        added_zeros = int("".join(original_data[-2:]))
        del original_data[-2:]  # Remove padding metadata

        # Remove salt
        del original_data[0]  # Remove leading salt
        del original_data[-1]  # Remove trailing salt

        # Remove padding
        original_data = original_data[:-added_zeros]

        # Reconstruct original message
        original = "".join(original_data)

        return original

    def close(self):
        return