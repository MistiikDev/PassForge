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
    """
    Recover a password by its ID and set it to active.
    """
    force_recover = 'force' in kwargs

    current_logins = data_service.read_data_as_json(PW_FILE)
    exists, cred_id = interaction_service.get_credentials(parameters, list_credentials)


    if not exists:
        return ui_service.display('Credentials not found, please try again.')

    passwords = current_logins[cred_id].get('pws', [])

    if not passwords:
        return ui_service.display('Could not retrieve passwords. Try again.', "LightError")

    if parameters and len(parameters) > 1:
        cred_id = parameters[0]  # Get credential ID from parameters
        pw_id = parameters[1]
    else:
        pw_id = interaction_service.get_input_from_user('Enter the password ID you wish to recover (ls_pws to check): ', str)

    if not pw_id:
        return ui_service.display('The password ID is not set properly, try again', "LightError")

    active_pws = [pw for pw in passwords if pw['active']]

    if force_recover:
        ui_service.display('Forcing recovering.', "LightError")

    # Find and activate the specified password
    for pw in passwords:
        if str(pw['id']) == pw_id:
            ## if the password is already active, no need to recover.
            if pw in active_pws:
                return ui_service.display('Selected password is already active.', "LightError")

            ## If there are already active passwords, notify user.
            if len(active_pws) > 0:
                ## if we proceed, deactivate current password
                confirmation = force_recover or interaction_service.get_approval_user("[yellow]Warning[/yellow]: There is already one active password. Proceeding will archive it. Are you sure you want to proceed? (y/n)",str, ask_one=False)

                if confirmation:
                    for active_pw in active_pws:
                        active_pw_id = str(active_pw['id'])

                        ui_service.display(f'Password ID {active_pw_id} is now deactivated.', "LightError")
                        active_pw['active'] = False
                else:
                    raise Abort("Recover")

            pw['active'] = True
            current_logins[cred_id]['pws'] = passwords
            data_service.save_data(current_logins, PW_FILE)

            return ui_service.display(f'Password ID {pw_id} is now active.', "Success")

    return ui_service.display('The password ID could not be found, try again.', "LightError")
