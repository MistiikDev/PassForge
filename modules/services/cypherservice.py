from time import *

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from modules.crypto.ceasar import CesarEncryption
from modules.crypto.rsa import RSAEncryption
from modules.crypto.custom import CustomEncryption

from modules.services.dataservice import DatastoreService
from modules.services.uiservice import UiService
from modules.services.securityservice import SecurityExceptions

ENUMS_FILE = "enumerators.json"
DATA_FOLDER = "data"  # Folder inside "modules"

data_util = DatastoreService(DATA_FOLDER)
ui_util = UiService()

class CypherService:
    def __init__(self):
        self.messageMaxLength = 20
        self.messageMinLength = 8

        self.encryptionMethods = {
            "1" : CesarEncryption(self.messageMaxLength),
            "2": RSAEncryption(self.messageMaxLength),
            "3": CustomEncryption(self.messageMaxLength)
        }

    ## Check if given code is linked to an encryption method.
    def is_cypher_valid(self, algo_code: int | str) -> bool:
        algo_code = str(algo_code)

        if not algo_code:
            return False

        if not algo_code in self.encryptionMethods:
            return False
        
        return True


    ## Generate keys based off of encryption method.
    def get_encryption_keys(self, encryption_method: int | str) -> any:
        ## If the algorithm has a method to generate its own keys, then retrieve them.

        generate_key_attribute = self.cypher_get_attr(encryption_method, "generate_keys")
        key_generation_generic = generate_key_attribute is None

        if key_generation_generic:
            key = [int(time())] ## Most generate key is the timestamp of generation time.
        else:
            try:
                private, public = generate_key_attribute()
                key = [private, public]

            except Exception as e:
                return ui_util.display(f"Error while retrieving encryption keys. Could not save credentials: {e}", "Error")
        return key


    ## Encrypt given message based off of given algorithm code.
    def encrypt_master(self, algo_code: int, message: str, key: any) -> any:
        algo_code = str(algo_code)
        is_valid = self.is_cypher_valid(algo_code)

        if not is_valid:
            raise ValueError("Cypher method not identified.")

        if (len(message) > self.messageMaxLength) or (len(message) < self.messageMinLength):
            raise SecurityExceptions.PasswordLength(self.messageMinLength, self.messageMaxLength)

        return self.encryptionMethods[algo_code].encrypt(message, key)

        ##try:
        ##    return self.encryptionMethods[algo_code].encrypt(message, key)
        
        ##except Exception as e:
        ##    return ui_util.display(f"Encryption Error: {e}", "Error")


    ## Decrypt given message based off of given algorithm code.
    def decrypt_master(self, algo_code: int, _hash: str, key: any) -> any:
        algo_code = str(algo_code)
        is_valid = self.is_cypher_valid(algo_code)

        if not is_valid:
            raise ValueError("Cypher method is not valid.")
        try:
            return self.encryptionMethods[algo_code].decrypt(_hash, key)
        except Exception as e:
            return ui_util.display(f"Decryption Error: {e}", "Error")


   ## Check if given algorithm has a certain attribute, if so, return it.
    def cypher_get_attr(self, algo_code: int, attr: str) -> any:
        algo_code = str(algo_code)
        is_valid = self.is_cypher_valid(algo_code)

        if not is_valid:
            raise ValueError("Cypher method is not valid.")

        if not hasattr(self.encryptionMethods[algo_code], attr):
            return None

        return getattr(self.encryptionMethods[algo_code], attr)

    
    def close_master(self):
        for encrypter_id in self.encryptionMethods:
            encrypter = self.encryptionMethods[encrypter_id]

            encrypter.close()
