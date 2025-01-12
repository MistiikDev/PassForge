import os
import sys
import json

import builtins

from modules.services.commandservice import CommandService

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_SETTINGS = os.path.join(BASE_DIR, "./modules/data/app_settings.json")

class AppMaster:
    def __init__(self):
        self.app_ver = 0
        self.app_command_prefix = None
        self.is_running = False

        ## Open Application settings
        ## Setup helpers and parameters for classes

        try:
            with open(APP_SETTINGS) as setting_file:
                app_settings = json.load(setting_file)

                if app_settings:
                    app_ver = app_settings['version']
                    app_command_prefix = app_settings['command_prefix']

                    ## Inform user of running version of the Application
                    ## Set up the prefix if any (command access)

                    print(f'RUNNING VERSION : {app_ver}')

                    if app_command_prefix and app_command_prefix != "":
                        print(f'ACCESS COMMANDS WITH PREFIX : {app_command_prefix} \n')

                    self.app_ver = app_ver
                    self.app_command_prefix = app_command_prefix

        except Exception as e:
            print(f'Could not retrieve application settings : {e}')


        print("Type the command 'help' to see available commands")


        ## Initiate command handler
        self.command_handler = CommandService(self.app_command_prefix)

    def run(self) -> None:
        self.is_running = True

        ## While the app is running, listen to user commands and inputs
        while self.is_running:
            _input = input("Enter command: ")

            if _input.lower() == "quit":
                self.is_running = False
                break

            print("\n")

            try:
                self.command_handler.execute(_input)
            except Exception as e:
                if e.__class__.__module__ != builtins.__name__:
                    print(f"Error while handling command '{_input}': {e}")

            print("\n")



if __name__ == "__main__":
    App = AppMaster()
    App.run()