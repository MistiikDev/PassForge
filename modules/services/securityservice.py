import re
import random
import string

COMMON_PW = "common_pw.txt"
COMMON_WORDS = "common_words.txt"
DATA_FOLDER = "data"

from modules.services.dataservice import DatastoreService
from modules.services.uiservice import UiService

data_service = DatastoreService(DATA_FOLDER)
ui_service = UiService()

common_passwords = data_service.read_data_as_txt(COMMON_PW)

def is_common_password(password: str) -> bool:
    """Check if the password is in the list of common passwords."""
    return password in common_passwords

def has_uppercase(password: str) -> bool:
    """Check for at least one uppercase letter."""
    return bool(re.search(r'[A-Z]', password))

def has_lowercase(password: str) -> bool:
    """Check for at least one lowercase letter."""
    return bool(re.search(r'[a-z]', password))

def has_digit(password: str) -> bool:
    """Check for at least one digit."""
    return bool(re.search(r'\d', password))

def has_special_char(password: str) -> bool:
    """Check for at least one special character."""
    return bool(re.search(r'[^A-Za-z0-9]', password))

def calculate_password_score(password: str) -> int:
    """Calculate a score based on password characteristics."""
    score = 0
    if len(password) >= 10: score += 1
    if has_uppercase(password) and has_lowercase(password): score += 1
    if has_digit(password): score += 1
    if has_special_char(password): score += 1
    return score

class SecurityExceptions:
    class PasswordLength(Exception):
        def __init__(self, min_length: int, max_length: int):
            min_length, max_length = str(min_length), str(max_length)

            ui_service.display(f"Password length is not matching requirements ({min_length} < ... < {max_length})", "error")

    class PasswordSecurity(Exception):
        def __init__(self):
            ui_service.display("Password is not matching any security requirements", "error")

    class Vulnerability(Exception):
        pass

class SecurityService:
    def __init__(self):
        self.lettersToSpecCharacters = {
            'a': '@', 'e': '3', 'i': '!',
            'l': '|', 'o': '0', 'q': '?', 's': '$',
            'u': 'µ',

            'A': '@', 'E': '€', 'I': '!',
            'L': '|', 'O': '0', 'Q': '?', 'S': '5',
            'U': 'µ',
        }

        self.default_overwrite_settings = {
            'only_lowercase': False,
            'only_uppercase': False,
            'no_digits': False,
            'no_special': False
        }

        return
    
    @staticmethod

    def password_strength(password: str) -> (str, bool):
        """Evaluate password strength."""
        feedback = []

        # Common password check
        if is_common_password(password):
            return "[red]Weak ✘: Password is too common.[/red]", False

        # Length check
        if len(password) < 8:
            feedback.append("Password length should be between 8 and 20 characters.\n")

        # Character checks
        if not has_uppercase(password):
            feedback.append("Add at least one uppercase letter.\n")
        if not has_lowercase(password):
            feedback.append("Add at least one lowercase letter.\n")
        if not has_digit(password):
            feedback.append("Add at least one digit.\n")
        if not has_special_char(password):
            feedback.append("Add at least one special character (e.g., !@#$%^&*).\n")

        if feedback:
            return f"[red]Weak ✘: {' '.join(feedback)}[/red]", False

        # Score evaluation
        score = calculate_password_score(password)
        if score == 4:
            return "[green]Strong ✔[/green]", True
        elif score == 3:
            return "[yellow]Ok ∼[/yellow]", True
        else:
            return "[red]Weak ✘[/red]", False


    ## Help me improve this generate password function

    def generate_strong_password(self, desired_length: int = 12, length_range=(8, 20), overwrite_settings=None) -> str:
        """
        Generates a strong password based on a dictionary of real words and adds complexity.

        Parameters:
        - desired_length: The length of the generated password
        - length_range: Tuple indicating the range of password length

        Returns:
        A string representing the strong password.
        """

        if overwrite_settings is None:
            overwrite_settings = self.default_overwrite_settings


        # Ensure words are not too long (to prevent overly long passwords)
        words = data_service.read_data_as_txt(COMMON_WORDS)
        words = [word for word in words if 2 <= len(word) <= 10]
        password_base = ""

        desired_length = int(desired_length)

        if desired_length < length_range[0]:
            desired_length = length_range[0]

            ui_service.display(f"Password length too short, generating {desired_length} character password", "warning")

        elif desired_length > length_range[1]:
            desired_length = length_range[1]

            ui_service.display(f"Password length too long, generating {desired_length} character password", "warning")


        # Start creating the password by adding words
        while len(password_base) < desired_length:
            selected_word = random.choice(words)
            password_base += selected_word

        # Trim or adjust the password to the desired length
        password_base = password_base[:desired_length]

        # Add a number and special character to increase complexity
        if not overwrite_settings['no_digits']:
            password_base += str(random.randint(10, 99))  # Add a random number

        if not overwrite_settings['no_special']:
            special_char = random.choice(string.punctuation)  # Choose a random special character
            password_base += special_char

        final_password = password_base

        # Make sure the password is within the length range
        if len(final_password) < length_range[0]:
            additional_chars = random.choices(string.ascii_letters + string.digits + string.punctuation, k=length_range[0] - len(final_password))
            final_password = final_password + ''.join(additional_chars)

        elif len(final_password) > length_range[1]:
            final_password = final_password[:length_range[1]]

        final_password = final_password[:desired_length]
        final_password = list(final_password)  # Convert to list to modify the characters

        has_integers = False

        # Modify the characters in the password
        for i in range(len(final_password)):
            character = final_password[i]
            new_character = character
            if isinstance(character, int):
                has_integers = True

            # Check if the character exists in the lettersToSpecCharacters dictionary
            if character in self.lettersToSpecCharacters:
                randomness = random.randint(1, 4)

                # Randomly change case
                if randomness % 2 == 0:
                    # Flip the case of the character
                    if character.isupper():
                       new_character = character.lower()
                    else:
                        new_character = character.upper()
                else:
                    # Map the letter to a special character
                    if not overwrite_settings['no_special'] and not overwrite_settings['no_digits']:
                        new_character = self.lettersToSpecCharacters[character.lower()]

            # Replace the character in the list
            final_password[i] = new_character

        ## If there are no digits, add one
        if not has_integers and not overwrite_settings['no_digits']:
            final_password[-1] = str(random.randint(0, 9))

        if overwrite_settings['only_lowercase']:
            final_password = [char.lower() for char in final_password]
        elif overwrite_settings['only_uppercase']:
            final_password = [char.upper() for char in final_password]

        return ''.join(final_password)

    