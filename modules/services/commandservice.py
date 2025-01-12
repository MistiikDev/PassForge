import json
import os
import importlib.util
import builtins


# Avoid using sys.path.append by ensuring the relative imports are correct
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Base directory for this file
COMMANDS_LIST_PATH = os.path.join(BASE_DIR, "../data/commands_list.json")  # Path to the commands list JSON
COMMANDS_FOLDER = os.path.join(BASE_DIR, "../commands")  # Path to the commands folder

from modules.services.uiservice import UiService  # Utility class for user interactions

class CommandService:
    """
    A service to manage and execute user commands from individual files. Handles:
    - Command parsing and validation
    - Dynamic loading of command modules
    - Displaying help and error messages
    """
    def __init__(self, prefix=None):
        """
        Initialize the CommandService.

        :param prefix: Optional prefix for command validation
        """
        self.prefix = prefix
        self.command_data = {}  # Dictionary to store loaded command definitions
        self.loaded_commands = {}  # Cache for dynamically loaded commands
        self.ui = UiService()  # Utility instance for displaying messages

        self._preload_commands()  # Load available commands on initialization

    def _preload_commands(self):
        """
        Load command definitions from the JSON file specified by COMMANDS_LIST_PATH.
        Handles JSON decode errors gracefully.
        """
        try:
            with open(COMMANDS_LIST_PATH, "r") as file:
                self.command_data = json.load(file)  # Parse JSON into a dictionary
        except json.JSONDecodeError:
            self.ui.display(f"Error: Failed to decode JSON from '{COMMANDS_LIST_PATH}'.", "error")

    def _load_command_module(self, command):
        """
        Dynamically load the module for a given command from the commands folder.

        :param command: The name of the command (corresponding to the file name)
        :return: The loaded module or None if an error occurs
        """
        module_path = os.path.join(COMMANDS_FOLDER, f"{command}.py")
        if not os.path.exists(module_path):
            return None

        try:
            spec = importlib.util.spec_from_file_location(command, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            self.ui.display(f"Error loading command '{command}': {e}", "error")
            return None

    def execute(self, args):
        """
        Main execution logic for commands.

        :param args: Command-line style input string
        :return: True if a valid command is executed; otherwise, False
        """
        # Split the input arguments into a list
        args = args.split(" ")

        if len(args) < 1:
            return False

        # Handle prefixed commands by separating prefix, command, and parameters
        if self.prefix and self.prefix != "":
            prefix, command = args[0], args[1]
            parameters = args[2:]
        else:
            command, parameters = args[0], args[1:]

        # Verify that the provided prefix matches the expected prefix
        if (self.prefix and self.prefix != "") and (prefix and prefix != self.prefix):
            return False

        # Check if the command exists in the JSON data
        if command not in self.command_data["commands"]:
            found = False

            # Attempt to match the command with its synonyms
            for _command in self.command_data["commands"]:
                command_data = self.command_data["commands"][_command]

                if command in command_data['synonyms']:
                    self.ui.display(f'Executing {command} (did you mean << {_command} >> ?)', "enums")

                    command = _command  # Correct to the matched command
                    found = True
                    break

            if not found:
                # Command not found; notify the user
                return self.ui.display(f'Could not find command {command} in command list!', "warning")

        # Load the command module dynamically
        module = self._load_command_module(command)

        if not module or not hasattr(module, "execute"):
            return self.ui.display(f"Command '{command}' could not be loaded or is missing 'execute' function.", "error")

        # Retrieve command metadata from the JSON
        data = self.command_data["commands"].get(command.lower(), {})

        # Check for special arguments (e.g., --help)
        args = []
        command_kwargs = []

        for argument in parameters:
            if argument.startswith("--"):
                kwarg = argument.lstrip("-").lower()
                if kwarg in data:
                    self.ui.display(data[kwarg])  # Display special command information

                    return True
                else:
                    command_kwargs.append(kwarg) # Add kwarg to command parameters (command special ?)
            else:
                args.append(argument)

        # Validate required and optional arguments
        tot_arg = data.get("parameters", "")
        tot_arg = [arg.strip().strip("'") for arg in tot_arg.split(",") if arg.strip()]  # Parse parameters

        req_arg = [arg for arg in tot_arg if not "?" in arg]  # Identify required arguments

        # Check if the required arguments are provided
        if len(args) < len(req_arg):
            return self.ui.display("Arguments missing, add '--parameters' or '--help' for more info.", "warning")

        # Execute the command with the provided parameters
        try:
            module.execute(args, command_kwargs or [])
            return True
        except Exception as e:
            if e.__class__.__module__ == builtins.__name__:
                self.ui.display(f"Error executing command '{command}': {e}", "error")

            return False