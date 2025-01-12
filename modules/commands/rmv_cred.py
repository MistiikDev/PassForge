from modules.services.dataservice import DatastoreService
from modules.services.uiservice import UiService
from modules.services.cypherservice import CypherService
from modules.services.interactionservice import InteractionService, QuitRequested
from modules.services.securityservice import SecurityService
from modules.commands.ls_cred import execute as list_credentials

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
    Remove a credential by its ID.
    """
    current_logins = data_service.read_data_as_json(PW_FILE)
    exists, cred_id = interaction_service.get_credentials(parameters, list_credentials)

    if exists:
        confirmation = interaction_service.get_approval_user("[yellow]Warning[/yellow]: Deleting a credential is [red]PERMANENT[/red]. Are you sure you want to proceed? (y/n)", str,ask_one=False)

        if confirmation:
            del current_logins[cred_id]
            data_service.save_data(current_logins, PW_FILE)

            return ui_service.display('Credentials successfully deleted from database.', "Success")
        else:
            raise QuitRequested
