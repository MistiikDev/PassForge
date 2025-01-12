
from modules.services.dataservice import DatastoreService
from modules.services.uiservice import UiService
from modules.services.cypherservice import CypherService
from modules.services.interactionservice import InteractionService, Abort
from modules.services.securityservice import SecurityService

# Constants for file paths and environment variable
PW_FILE = "pw.dat"  # File to store password data
ENUMS_FILE = "enumerators.json"  # File for enumerators (e.g., algorithms)
COMMANDS_FILE = "commands_list.json"  # File for command configurations

DATA_FOLDER = "data"  # Folder where data files are located

# Initialize services and utilities
data_service = DatastoreService(DATA_FOLDER)
security_service = SecurityService()
ui_service = UiService()
encryption_service = CypherService()
interaction_service = InteractionService()

def execute(parameters, kwargs=None):
    """
    Generate a strong password of desired length.
    """
    length = None

    only_lowercase = 'lowercase' in kwargs
    only_uppercase = 'uppercase' in kwargs
    no_digits = 'no_digits' in kwargs
    no_special = 'no_special' in kwargs

    overwrite_settings = {
        'only_lowercase': only_lowercase,
        'only_uppercase': only_uppercase,
        'no_digits': no_digits,
        'no_special': no_special
    }

    if parameters and len(parameters) > 0:
        if parameters:
            try:
                length = int(parameters[0])  # Attempt to convert the first parameter to an integer
            except (ValueError, TypeError):
                raise Abort("Could not convert length to a valid integer.")

    if not length:
        length = interaction_service.get_input_from_user("Enter the desired password length: ", int, True) or 12

    pw = security_service.generate_strong_password(desired_length=length, overwrite_settings=overwrite_settings)
    ui_service.display("Generated password:", "Info")
    ui_service.display(str(pw))
