from modules.services.dataservice import DatastoreService
from modules.services.uiservice import UiService
from modules.services.cypherservice import CypherService
from modules.services.interactionservice import InteractionService, Abort
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
    force = 'force' in kwargs
    force and ui_service.display('Forcing deletion.', "LightError")

    """
    Remove a password by its ID.
    """
    current_logins = data_service.read_data_as_json(PW_FILE)
    exists, cred_id = interaction_service.get_credentials(parameters, list_credentials)

    if exists:
        passwords = current_logins[cred_id]['pws']

        if parameters and len(parameters) > 1:
            cred_id = parameters[0]  # Get credential ID from parameters
            pw_id = parameters[1]
        else:
            pw_id = interaction_service.get_input_from_user('Enter the password ID you wish to delete (ls_pws to check): ',str)

        active_pw = [pw for pw in passwords if pw['active']]

        if pw_id:
            for pw in passwords:
                if str(pw['id']) == pw_id:
                    if force:
                        passwords.remove(pw)
                    else:
                        if pw in active_pw:
                            confirmation = interaction_service.get_approval_user("[yellow]Warning[/yellow]: The selected password is already active. Removing it will archive it. Are you sure you want to proceed? (y/n)", str, ask_one=False)

                            if confirmation:
                                pw['active'] = False
                            else:
                                raise Abort("Erasure")
                        else:
                            confirmation = interaction_service.get_approval_user("[yellow]Warning[/yellow]: The selected password is archived. Removing it will [red]DELETE IT PERMANENTLY[/red]. Are you sure you want to proceed? (y/n)", str, ask_one=False)

                            if confirmation:
                                passwords.remove(pw)
                            else:
                                raise Abort("Erasure")
                    break
            else:
                return ui_service.display('Password ID not found.', "LightError")

            current_logins[cred_id]['pws'] = passwords
            data_service.save_data(current_logins, PW_FILE)

            ui_service.display(f"Password ID {pw_id} successfully removed.", "Success")
