from modules.commands import ls_pws
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
    search_tile = None
    if parameters and len(parameters) > 0:
        search_tile = parameters[0]

    if not search_tile:
        search_tile = interaction_service.get_input_from_user('Enter the desired tile to search for: ', str, False)

    ## Search through logins, then passwords, then labels, in any case, return the entire data sorted.
    current_logins = data_service.read_data_as_json(PW_FILE)
    search_data = []

    for cred_id in current_logins:
        current_data = current_logins[cred_id]

        login = current_data['login']
        pws = current_data['pws']
        labels = current_data['labels']

        if search_tile == login:
            search_data.append({'ID': cred_id})

            ui_service.display(f"[italic]Found Login [cyan]'{login}'[/cyan] for credentials [bright_red]'{cred_id}'[/bright_red][/italic]\n")

        for pw_data in pws:
            pw_key = pw_data['key']
            pw_value = pw_data['value']
            pw_crypto = pw_data['crypto']

            search_pw = encryption_service.decrypt_master(pw_crypto, pw_value, pw_key)

            if search_pw and search_pw == search_tile:
                search_data.append({'ID': cred_id,})

                ui_service.display(f"[italic]Found Password [cyan]'{search_tile}'[/cyan] for credentials [bright_red]'{cred_id}'[/bright_red][/italic]\n")

        for label in labels:
            if label == search_tile:
                search_data.append({'ID': cred_id})

                ui_service.display(f"[italic]Found Label [cyan]'{label}'[/cyan] for credentials [bright_red]'{cred_id}'[/bright_red][/italic]\n")

                break

    if len(search_data) == 0:
        ui_service.display(f"[italic]No data found for search term [cyan]'{search_tile}'[/cyan][/italic]\n")
        return

    for data in search_data:
        _id = data['ID']

        ui_service.display_header(f"Associated Credential: {_id}")
        ls_pws.execute([_id])

        print('\n')
