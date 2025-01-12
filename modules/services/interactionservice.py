from modules.services.uiservice import UiService
from modules.services.dataservice import DatastoreService

# Constants for file paths
DATA_FOLDER = "data"  # Folder where data is stored
SETTINGS_FILE = "app_settings.json"  # File for application settings
PW_FILE = "pw.dat"  # File for storing passwords

# Utility and service initialization
ui_service = UiService()
data_service = DatastoreService(DATA_FOLDER)

# Custom exception for user-requested quit
class QuitRequested(Exception):
    def __init__(self):
        ui_service.display("User Interruption", "Error")

        pass

class Abort(Exception):
    def __init__(self, action: str):
        ui_service.display(f"{action} aborted.", "Error")

        pass

class MissingReference(Exception):
    def __init__(self, reference, parent):
        ui_service.display(f"Reference '{reference}' does not exist in '{parent}'.", "Error")

        pass

# Class to handle user interactions
class InteractionService:
    def __init__(self):
        # Command to signal quit; currently unused
        self.quitCommand = None
        return

    @staticmethod
    def get_input_from_user(mess: str, expected_type: type = str, ask_once: bool=False) -> any:
        """
        Get input from the user with type validation.

        Parameters:
        - mess: Message to display to the user.
        - expected_type: Type to which the input should be converted.
        - ask_once: If True, don't re-prompt on invalid input.

        Returns:
        - Converted user input, or None if ask_once is True and input is invalid.
        """
        ui_service.prompt_user(mess)  # Show the message to the user

        while True:
            # Prompt the user for input
            user_input = input(f"\n >> Enter a value of type {expected_type.__name__} (or type '-quit' to exit): ")

            if user_input.lower() == "-quit":
                raise QuitRequested()  # Raise exception to signal quit

            if ask_once and user_input == "":
                ui_service.display("No input provided: Proceeding.", "Warning")
                return None  # No input provided when ask_once is True

            try:
                # Try converting the input to the expected type
                converted_input = expected_type(user_input)
                return converted_input
            except ValueError:
                if not ask_once:
                    ui_service.display(f"Invalid input. Please enter a value of type {expected_type.__name__}.", "LightError")

            if ask_once:
                # Handle invalid input when ask_once is True
                ui_service.display("Invalid input. Proceeding without valid input.", "Warning")
                return None

    def get_approval_user(self, mess: str, expected_type: type, ask_one: bool=False) -> bool:
        """
        Ask for user's approval (e.g., Y/N response).

        Parameters:
        - mess: Message to display to the user.
        - expected_type: Expected type of the response (e.g., str).
        - ask_one: If True, only ask once.

        Returns:
        - True if user approves (e.g., inputs 'y'), False otherwise.
        """
        answer = self.get_input_from_user(mess=mess, expected_type=expected_type, ask_once=ask_one)

        if answer is None:
            return False

        return answer.lower() == "y"  # Convert to lowercase and check for 'y'

    def get_credentials(self, parameters: list, listing_function: ()) -> any:
        """
        Retrieve credentials based on user input or parameters.

        Parameters:
        - parameters: List of command-line parameters (e.g., credential ID).
        - list_cred: Function to list credentials.

        Returns:
        - Tuple (exists, cred_id) if credentials exist, or calls list_cred().
        """
        if parameters and len(parameters) > 0:
            cred_id = parameters[0]  # Get credential ID from parameters
        else:
            listing_function([])  # List all credentials if no parameter is provided
            cred_id = self.get_input_from_user('Enter the credentials id you wish to see the details : ', str)

        # Check if the credential ID exists in the current logins
        current_logins = data_service.read_data_as_json(PW_FILE)
        exists = cred_id in current_logins

        if not exists:
            listing_function([])  # List all credentials if the provided ID does not exist

            raise MissingReference(cred_id, "Credentials")

        return exists, cred_id  # Return the existence status and credential ID
