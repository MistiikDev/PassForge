from modules.services.dataservice import DatastoreService
from modules.services.uiservice import UiService
from modules.services.cypherservice import CypherService
from modules.services.interactionservice import InteractionService
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
    Calculate the strength of a given password.
    """
    pw = None

    if parameters and len(parameters) > 0:
        pw = parameters[0]

    if not pw:
        pw = interaction_service.get_input_from_user("Enter the password to calculate its strength: ", str, False)

    strength, can_be_used = security_service.password_strength(pw)
    ui_service.display(f"Result: {strength}", "Info")
    ui_service.display(f"==> Password is {can_be_used and 'usable' or 'unusable'}", (can_be_used and 'Success' or 'Warning'))
