import random
import uuid

from modules.commands import ls_crypto
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
    Add a new credential or update an existing one.
    """
    current_logins = data_service.read_data_as_json(PW_FILE)

    tag = None
    if parameters and parameters[0]:
        tag = parameters[0]
    else:
        tag = interaction_service.get_input_from_user(
            'Enter an ID for you to recognize the credentials: ', str
        )

    cred_id = tag
    already_exists = cred_id in current_logins
    is_active = True

    # If credential already exists, handle updates
    if already_exists:
        existing_entry = current_logins[cred_id]
        login = existing_entry.get('login', '')
        pws = existing_entry.get('pws', [])
        labels = existing_entry.get('labels', [])

        confirmation = interaction_service.get_approval_user(
            f"Entry for '{cred_id}' already exists. Do you want to modify it? (y/n): ", str, True
        )

        if not confirmation:
            raise Abort("Authentication")

        # Disable the current active password, if any
        for password in pws:
            if password.get("active", False):
                password["active"] = False
                is_active = True

                ui_service.display(
                    'If set, current password will be moved to history and replaced by the new entry. '
                    'You can still check history by entering {ls_pws}',
                    "Warning"
                )
                break
    else:
        # Initialize a new credential entry
        current_logins[cred_id] = {
            'login': "",
            'pws': [],
            'labels': []
        }
        login = ""
        pws = []
        labels = []

    # Prompt for login and password
    login = interaction_service.get_input_from_user('Enter your login: ', str, already_exists) or login
    feedback, password_secure = "", False
    pw = None

    while not password_secure:
        pw = interaction_service.get_input_from_user('Enter your password: ', str, already_exists)
        feedback, password_secure = security_service.password_strength(pw)
        pw_recommendation = security_service.generate_strong_password(desired_length=12)

        ui_service.display(f"Password Strength is {feedback}", "Info")

        if not password_secure:
            ui_service.display(f'Suggestion: {pw_recommendation}', 'enums')

    if pw:
        # Display available encryption methods
        ls_crypto.execute([])

        encryption_method = interaction_service.get_input_from_user(
            'Please enter the encryption type: ', int, False
        )

        if not encryption_service.is_cypher_valid(encryption_method):
            return ui_service.display(f"Error while getting encryption method. Could not find ID: {encryption_method}",
                                   "Error")

        key = encryption_service.get_encryption_keys(encryption_method)

        if not key:
            return ui_service.display("Error while getting encryption key.", "Error")

        encrypted_pw = encryption_service.encrypt_master(encryption_method, pw, key)

        # Generate a unique ID for the password, and append data

        uid = str(uuid.uuid4()).split("-")[0]
        pws.append({
            'id': uid,
            'key': key,
            'value': encrypted_pw,
            'crypto': encryption_method,
            'active': is_active
        })

    # Prompt for a label to tag the credentials
    label = interaction_service.get_input_from_user('Enter a label to register the auth: ', str, True)
    if label:
        labels.append(label)

    # Save updated credentials
    current_logins[cred_id] = {
        'login': login,
        'pws': pws,
        'labels': labels
    }

    data_service.save_data(current_logins, PW_FILE)
    ui_service.display(f"Data for '{cred_id}' successfully saved.", "Success")
