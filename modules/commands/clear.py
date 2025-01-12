from os import system, name

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
    Clear the terminal screen.
    """
    if name == 'nt':
        system('cls')
    else:
        system('execute')
