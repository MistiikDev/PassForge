import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from modules.services.uiservice import UiService
ui_util = UiService()

class DatastoreService:
    def __init__(self, target_directory):
        self.target_directory = target_directory

    def save_data(self, data, target_filename) -> bool:
        try:
            json_data = json.dumps(data, indent=4)
            target_path = os.path.join(os.path.dirname(__file__), f"../{self.target_directory}/{target_filename}")

            with open(target_path, "w") as target_file:
                target_file.write(json_data)

                ui_util.display(f"Data successfully written to {target_filename}", "success")
                return True

        except IOError as e:
            ui_util.display(f"An error occurred while writing to {target_filename}: {str(e)}", "error")
            return False

    def read_data_as_json(self, target_filename) -> any:
        target_path = os.path.join(os.path.dirname(__file__), f"../{self.target_directory}/{target_filename}")
        
        try:
            # Open the file and read the content
            with open(target_path, "r") as target_file:
                decrypted_data = target_file.read()

                return json.loads(decrypted_data)
        except (IOError, json.JSONDecodeError) as e:
            ui_util.display(f"An error occurred while reading {target_filename}: {str(e)}", "error")
            return None
        
    def read_data_as_txt(self, target_filename):
        target_path = os.path.join(os.path.dirname(__file__), f"../{self.target_directory}/{target_filename}")
        
        try:
            # Open the file and read the content
            with open(target_path, "r") as target_file:
                decrypted_data = set(target_file.read().splitlines())

                return decrypted_data
            
        except Exception as e:
            ui_util.display(f"An error occurred while reading {target_filename}: {str(e)}", "error")
            return None

