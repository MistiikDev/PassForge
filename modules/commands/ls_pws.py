from modules.services.dataservice import DatastoreService
from modules.services.uiservice import UiService
from modules.services.cypherservice import CypherService
from modules.services.interactionservice import InteractionService
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
    List all passwords for a specific credential.
    """
    current_logins = data_service.read_data_as_json(PW_FILE)
    exists, cred_id = interaction_service.get_credentials(parameters, list_credentials)

    if exists:
        data = current_logins[cred_id]

        login = data['login']

        active_pws = [pw for pw in data['pws'] if pw.get('active', False)]
        inactive_pws = [pw for pw in data['pws'] if not pw.get('active', False)]

        ui_service.display(f"[bright_yellow]   ==> Login: {login}[/bright_yellow]\n")

        ui_service.display_passwords("Active Passwords", active_pws, encryption_service)
        ui_service.display_passwords("Passwords History", inactive_pws, encryption_service)

        labels = [label for label in data['labels']]
        entries = len(labels)
        if entries > 0:
            ui_service.display(f"[bright_yellow]   ==> Labels: {str(entries)}[/bright_yellow]")

            for label in labels:
                ui_service.display(f'[italic]     -> ID: [bright_green]{label}[/bright_green][/italic]')
