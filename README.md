## 1. General Overview

**Password Manager** allows you to centralize the storage of your login data locally while encrypting it, ensuring a certain level of security.  

⚠️ **Warning:**  
- **Each file mentioned below must not be renamed.** Any modification to file names could compromise the proper functioning of the application.  
- This also includes a risk of permanent loss of encrypted data, as the application relies on direct links between these files.  

### Main Files  

- **`app.py`**:  
  Contains the core functionality of the application. This file:  
  - Performs various checks and initializations necessary before launching the modules.  
  - Then executes the user's command request.  

### Module Files  

The **`MODULE`** folder groups the main components of the application:  

- **`containers`**:  
  Contains files (Python or others) that include the necessary information for the functioning of other modules, such as:  
  - Functions  
  - Variables  
  - Imports  

- **`crypto`**:  
  Includes the various cryptographic methods supported by the application. *(These mechanisms will be detailed later.)*  

- **`data`**:  
  Contains the files storing the login data.  

- **`services`**:  
  Contains Python files that:  
  - Are independent of the main features of the application.  
  - Allow greater modularity and flexibility.  

### Overall Functionality  

Each login data entry is saved under an identifier (unique, chosen by the user), which makes it easier to retrieve the login details.  
For each identifier, the following is stored: login, password (encrypted, using encryption chosen by the user), and label (one or more tags, which also help retrieve login details).  

## 2. Command Documentation

This documentation lists all available commands in the **Password Manager**, grouped by categories, with their descriptions, parameters, and usage examples.  

---

## Table of Contents  

- [General Commands](#general-commands)  
- [Listing Commands](#listing-commands)  
- [Modification Commands](#modification-commands)  
- [Search and Analysis Commands](#search-and-analysis-commands)  

---

## General Commands  

### 0. `quit`
- Exits the command prompt directly.

### 1. `clear`  
**Description:** Clears the display.  
- **Parameters:** _None_  
- **Usage:** `clear`  
- **Help:** Clears previous commands and messages when the display becomes too cluttered.  
- **Synonyms:** `cls`, `c`, `empty`  

---

### 2. `helper`  
**Description:** Provides information on available commands and their usage.  
- **Parameters:** `[command_name?]` (_optional_)  
- **Usage:** `helper` or `helper <command_name>`  
- **Help:** Lists all commands or shows specific details for a given command.  
- **Synonyms:** `assist`, `info`, `help`, `h`  

---

### 3. `restart_shell`  
**Description:** Restarts the Python CMD application.  
- **Parameters:** _None_  
- **Usage:** `restart_shell`  
- **Help:** Useful for developers to quickly restart the application and apply changes without manually exiting.  
- **Synonyms:** `restart`  

---

## Listing Commands  

### 4. `ls_cred`

**Description:**  
The `ls_cred` function **displays a list of all registered credentials** in the password manager.

**Parameters:**  
- [`credentials_id?`] (_optional_)

**Functionality:**  
1. **Display of credentials:** All registered credentials are listed for the user.

**Synonyms:** `cred`, `list_groups`  

---

### 5. `ls_pws`  

**Description:**  
The `ls_pws` function **displays all passwords associated with a specific credential ID**. It separates active passwords from inactive (historical) ones and also displays associated labels.

**Parameters:**  
- [`credentials_id?`] (_optional_)

**Functionality:**  
1. **Selection of credential ID:** The user enters the ID of the credential for which passwords should be displayed (if not already provided).  

2. **Display of active and inactive passwords:**  
   - Active passwords are displayed first.  
   - Inactive (historical) passwords are displayed next.  

3. **Display of labels:** If labels are associated with the credential, they are also displayed.  

**Synonyms:** `show_passwords`, `list_pw`  

---

### 6. `ls_crypto`  

**Description:**  
The `ls_crypto` function **displays the available cryptographic methods**. It retrieves the list of encryption algorithms from stored data and presents it to the user.

**Parameters:**  
- _None_

**Functionality:**  
1. **Display of cryptographic solutions:** Encryption algorithms are shown as a list for user consultation.

**Synonyms:** `list_encryption`, `show_crypto`  

---

## Modification Commands  

### 7. `add_cred`  

**Description:**  
The `add_cred` function **adds a new credential** or **updates an existing credential** in the password manager. It supports creating new credentials, modifying existing ones, updating passwords, applying encryption, and adding labels to categorize credentials.

**Parameters:**  
- _None_

**Functionality:**  
1. **Enter credential ID:** The user enters an ID to identify their credentials. The ID is checked to determine if it already exists.  

2. **Check credential existence:**  
   - If the ID exists, the user is asked to confirm whether they want to modify the existing entry.  
   - If the user agrees to modify, and if a password is entered, the active password is deactivated and moved to the history before adding the new password.  

3. **Enter fields:**  
   - The user is prompted to enter their login and password.  

4. **Password strength validation:**  
   - The entered password is evaluated for strength. The function ensures it meets security standards before storing it.  

5. **Encryption:**  
   - The user selects an encryption method, and the password is encrypted accordingly.  

6. **Add labels:**  
   - The user enters a label to associate with the credentials, enabling easy categorization and identification.  

7. **Save data:**  
   - The updated credentials are saved, and a success message is displayed if everything works.  

**Synonyms:** `add_login`, `create_cred`, `add_credentials`  

---

### 8. `rmv_cred`  

**Description:**  
The `rmv_cred` function **removes a credential** by its ID from the password manager. The user must confirm deletion before the entry is permanently removed.

**Parameters:**  
- [`credentials_id?`] (_optional_)  

**Functionality:**  
1. **Enter credential ID:** The user enters the ID of the credential to delete.  

2. **Check credential existence:** If the credential exists, the user is warned that deletion is **permanent**.  

3. **Confirm deletion:** The user must confirm whether they truly want to delete the credential. If declined, deletion is canceled.  

4. **Delete credential:** If confirmed, the credential is removed from the database.  

5. **Update database:** The database is saved after deletion, and a success message is displayed.  

**Synonyms:** `rmv_cred`, `remove_cred`, `delete_cred`  

---

### 9. `rmv_pw`  

**Description:**  
The `rmv_pw` function **removes a password** by its ID from the password manager. It offers the user a confirmation prompt and handles the removal of active or archived passwords.

**Parameters:**  
- [`credentials_id?`] (_optional_)  

**Functionality:**  
1. **Check credential existence:** The user enters the ID of the credential to remove a password.  

2. **Enter password ID to remove:** The user enters the ID of the password to remove. If not found, an error message is shown.  

3. **Verify password status:**  
   - If the password is **active**, the user is warned that deletion will archive it.  
   - If the password is **archived**, the user is warned that deletion will be **permanent**.  

4. **Delete or archive password:**  
   - For an **active** password, it is deactivated (moved to history).  
   - For an **archived** password, it is permanently removed.  

5. **Update database:** The database is updated and saved after deletion, and a success message is displayed.  

**Synonyms:** `remove_password`, `delete_pw`, `remove_pw`  

---

## Search and Analysis Commands  

### 10. `recover_pw`

**Description:**  
The `recover_pw` function **recovers a password** by its ID and makes it active. It restores a previously deactivated password under a specific credential ID in the password manager.

**Parameters:**  
- [`credentials_id?`] (_optional_)  

**Functionality:**  
1. **Check credential existence:** The user enters the credential ID for password recovery.  

2. **Verify associated passwords:** If the credential is found, the function checks for associated passwords.  

3. **Enter password ID to recover:** The user enters the ID of the password to recover.  

4. **Warning:** If there is already an active password, the user is warned that it will be archived and replaced by the recovered password.  

5. **Activate password:** The selected password becomes active.  

6. **Update database:** The database is updated and saved.  

**Synonyms:** `recover_password`, `save_pw`, `save_password`  

---

### 11. `search_by_field`  

**Description:**  
The `search_by_field` function **searches for information** (login, password, or label) within stored credentials. It scans logins, passwords, and labels for matches and displays the results.

**Parameters:**  
- [`search_tile?`] (_optional_)  

**Functionality:**  
1. **Enter search field:** If no field is provided, the user is prompted to specify the field to search (login, password, or label).  

2. **Search logins:** The function scans stored credentials for matching logins.  

3. **Search passwords:** If no login matches, passwords are decrypted and compared.  

4. **Search labels:** If no password matches, labels are checked for matches.  

5. **Display results:** Matches are displayed, showing associated credential IDs.  

6. **Show associated credentials:** Details of matching credentials are listed, including passwords and other relevant data.  

**Synonyms:** `find_by_field`, `search_credentials`, `search_by_value`  

---

### 12. `get_strength`

### Description:
The `get_strength` function **evaluates the strength of a password** based on criteria such as length, the presence of uppercase letters, lowercase letters, numbers, and special characters. It displays the password's security level and indicates whether it is usable or not.

### Parameters:
- [`password?`] (_optional_): The password to evaluate. If not provided, the user is prompted to input a password.

### Functionality:
1. **Password Input**: If no password is provided as a parameter, the user is prompted to input a password for evaluation.
2. **Password Strength Evaluation**:
   - The function calls `password_strength` to analyze the password's strength, checking for criteria like length, uppercase/lowercase letters, numbers, and special characters.
   - Based on the result, it displays a message indicating the password's strength (between 0 and 4), along with a status (usable or not).
3. **Result Display**:
   - The password's security level is displayed in a color-coded message:
     - **Strong** (✔): If the password is deemed sufficiently secure.
     - **Medium** (∼): If the password is acceptable but could be improved.
     - **Weak** (✘): If the password is too weak to use.

Synonyms: `password_strength_check`, `evaluate_pw_strength`, `check_pw_security`

---

### 13. `get_pw`

### Description:
The `get_pw` function **generates a strong password** of a specified length as requested by the user. This password is created by combining real words with numbers and special characters while maintaining a high-security level.

### Parameters:
- [`desired_length?`] (_optional_): The desired password length. If not provided, a default length of 12 characters is used.

### Functionality:
1. **Password Length Input**: The user is prompted to enter the desired password length.
2. **Password Generation**:
   - A password is generated by selecting real words from a dictionary and combining them to meet the desired length.
   - The password is then enhanced with a random number and a special character to increase complexity.
3. **Length Validation**:
   - If the generated password is too short, additional characters are added to meet the limits defined in `length_range`.
   - If the password is too long, it is truncated to conform to the desired length.
4. **Character Modification**:
   - Some characters may be modified to include uppercase/lowercase letters and special characters to improve security.
   - If the password lacks numbers, a random number is added at the end.
5. **Display of the Generated Password**: The final password is displayed to the user.

Synonyms: `generate_strong_password`, `create_pw`, `secure_pw`

---

## Notes:

- Commands marked as _optional_ can be used without parameters or with optional parameters.
- If a command requires parameters but none are specified, they will be requested directly from the user during execution.
- **Command Syntax**: Commands must be entered exactly as specified.
- **Synonyms**: Synonyms allow flexible usage of commands.

---

# 3. General Usage

## Interface

The application's interface is designed to be simple and intuitive. Upon launch, it displays the following information:
- Application version
- Possible startup errors
- Command input field

---

## Interface Features

Using the commands available in the CMD interface, you can:
- **Add credentials**: Save a username and password.
- **View credentials**: View stored credentials along with their passwords.
- **Edit or delete credentials**: Manage existing credentials.
- **Handle cryptography**: Ensure the security of sensitive information.

---

#### Notes:
1. For all user requests (commands or others), the process can be interrupted by typing `-quit`.

2. For certain commands, you can **input the first parameter directly** after the command, without waiting for a prompt. For example, the two commands below are identical and work the same way:

#### Viewing Help for Commands

You can **view help for all commands** at any time via the dedicated help menu.


In total, there are **13 commands**, which can become complex when searching for specific help for a particular command.

---

### Special Arguments for Commands

You can add **special arguments** to commands, preceded by `--`, to directly display the characteristics of a specific command without going through the main `help` menu.

# 4. Cryptography

## Caesar Cipher

### Introduction
The **Caesar cipher** is a classical cryptography method where each letter in a message is shifted by a certain number of positions in the alphabet. This mechanism can be applied to strings containing both letters and numbers. The method described here enables encoding and decoding messages using a numeric key.

---

### Cipher Components

#### Alphabet and Numbers
The cipher uses an alphabet consisting of lowercase letters and digits:

- **Alphabet**: `['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']`
- **Digits**: `['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']`

#### Shift Functions

1. **Letter Shift**: The function `get_letter_shift(letter, shift)` shifts a letter by a specified number (key). This shift is performed cyclically within the alphabet.
2. **Number Shift**: The function `get_integer_shift(integer, shift)` shifts a digit cyclically within the sequence `0` to `9`.

<p align="center">
  <img src="images\Caesar3.svg.png" alt="Caesar Cipher" width="800">
</p>

---

## RSA Encryption

### Introduction
The **RSA encryption** algorithm is an asymmetric cryptographic technique widely used for securing communications. Unlike symmetric encryption, where the same key is used for both encryption and decryption, RSA uses a pair of keys: a public key for encryption and a private key for decryption.

---

### RSA Components

1. **Key Generation**:
   - **Public Key**: Used to encrypt messages.
   - **Private Key**: Used to decrypt messages.

2. **Prime Numbers**:
   RSA encryption relies on two large prime numbers, which are used to generate the public and private keys.

3. **Mathematical Functions**:
   - **Modular Inverse**: Used to calculate the private key from the public key.
   - **Greatest Common Divisor (GCD)**: Ensures the validity of the keys.
   - **Base 26**: Converts numbers to letters (A-Z) for message encoding.

---

### How RSA Works

#### 1. Key Generation
The RSA keys are generated through the following steps:
- Randomly generate two prime numbers **p** and **q** within a specified range.
- Calculate **n** as the product of **p** and **q**: `n = p * q`.
- Compute the totient of **n**, denoted as **φ(n)**: `φ(n) = (p - 1) * (q - 1)`.
- Select a number **e** such that **e** is "coprime" with **φ(n)** (i.e., their greatest common divisor is 1).
- Compute **d** as the modular inverse of **e** modulo **φ(n)**.

#### 2. Encryption
RSA encryption involves raising each character in the message to the power **e** and taking the remainder when divided by **n**. The result is encoded using a base-26 alphabet (A-Z).

#### 3. Decryption
Decryption reverses the process by raising the encrypted number to the power **d** (private key) and taking the remainder when divided by **n**. The result is converted back to plaintext.


---

# Documentation - Custom Encryptor

### Introduction
The **Custom Encryptor** is a custom encryption algorithm designed to secure messages. It uses padding techniques, timestamp manipulation, and base64 encoding to provide robust encryption and decryption.

---

### Components of the Custom Encryptor

1. **Message Padding**: If the message is shorter than the maximum allowed length, it is padded with random characters.

2. **Salt Generation**: Based on timestamps and the key difference, a salt is generated to enhance security.

   - **1**: Compute `ts`, the salt base:

     `ts = sqrt(t0^2 + t1^2)`

     - `t0`: Timestamp when the password is entered.  
     - `t1`: Timestamp when encryption starts.

   - **2**: Extract the salt base:  

     `b = ts - floor(ts)`

   - **3**: Calculate additional salt:  

     `s = ((b % 10 + (b % 100 - b % 10))^2) % 100`

3. **Encryption**: The message is combined with the salt and then encoded in base64.

4. **Decryption**: The inverse process retrieves the original message.

---

# 5. Customization

## Adding Commands

The application allows you to add new commands easily. Follow these steps to identify necessary files and configure relevant information.

---

### Step 1: Identify the Files to Modify

To add a new command, two files are essential: **`command_containers.py`** and **`command_list.json`**.

- **`command_containers.py`**: Contains the logic for commands.  
- **`command_list.json`**: Serves as an "inventory" of recognized commands.

---

### Step 2: Add Command Information

In **`command_list.json`**, provide the following information for each command:

- **`name`**: The command name.  
- **`description`**: What the command does.  
- **`parameters`**: Any parameters the command requires.  

⚠️ **NOTE**:
- Parameters must be separated by a comma **`,`**.  
- The command won't execute until all required parameters are provided.  
- Parameters can be **optional** by adding a `?` at the end of the name.

- **`help`**: Help information about the command.  
- **`synonyms`**: Synonyms allow commands to be called with alternative names.

---

### Step 3: Add Command Logic

To implement the command, create a function in **`command_containers.py`**.

⚠️ **IMPORTANT**: The function name must match the name defined in **`command_list.json`**.

#### Function Structure
Each command function receives an argument called `parameters`, which contains user-supplied input.

Based on the needs, you can:
- Use required parameters.  
- Define optional parameters with default values.  

---

### Step 4: Test the Command

Once the command logic is added, test its functionality to ensure it works as expected.

## Services

Services are important modules that encapsulate logic for the proper functioning of the application.

It is highly recommended that you use them when implementing your command logic.

## Services

---

# `UiService` API

## Description
The **`UiService`** class manages the display of messages in the password management application. It allows customizing the display of messages in the terminal with different colors and styles depending on the message type.

---

## Main Methods

### `UiService(debug_mode=False)` (`__init__`)
Initializes the service instance with an optional debug mode.

- **Parameters**:
  - `debug_mode`: A boolean indicating whether the debug mode is enabled (default: `False`).

---

### `display_header(self, header: str) -> None`
Displays a formatted header with blue text and underlined.

- **Parameters**:
  - `header`: The text of the header to be displayed.

- **Usage**: Used to display titles or important sections in the interface.

---

### `display(self, message: str, _type: str = None) -> None`
Displays a message with a specific format based on the message type.

- **Parameters**:
  - `message`: The message to be displayed.
  - `_type`: The type of message, which determines the style of the color (e.g., "error", "success", "info", etc.). This parameter is optional.

- **Usage**: Used to display general messages with colors suited to the message type (error, success, etc.).

---

### `display_crypto(self, header: str, data: list | dict) -> None`
Displays information about available encryption methods.

- **Parameters**:
  - `header`: The title or header to be displayed.
  - `data`: A dictionary or list containing information about the encryption algorithms.

- **Usage**: Used to display information about the encryption methods available in the application.

---

### `display_helpers(self, header: str, data: list | dict) -> None`
Displays help information for available commands in the application.

- **Parameters**:
  - `header`: The header of the help section.
  - `data`: A dictionary or list containing help information for each command.

- **Usage**: Used to display detailed help information about the available commands in the application.

---

### `display_passwords(self, header: str, data: list | dict, decrypter) -> None`
Displays the list of saved passwords, with decryption of the data.

- **Parameters**:
  - `header`: The title of the password section.
  - `data`: A list or dictionary containing the encrypted passwords.
  - `decrypter`: A decryption object used to decrypt the passwords.

- **Usage**: Used to display the saved passwords in the application after decrypting them.

---

### `prompt_user(self, prompt_message: str, question: bool = False) -> any`
Asks for user input in the terminal.

- **Parameters**:
  - `prompt_message`: The message to display to the user.
  - `question`: A boolean indicating if the prompt is a question (default: `False`).

- **Usage**: Used to ask questions or request information from the user in the terminal.

---

# `DatastoreService` API

## Description
The **`DatastoreService`** class allows reading and writing data to JSON and TXT files. It provides methods to save data, read data in different formats, and handle errors related to these operations.

---

## Main Methods

### `DatastoreService(target_directory)` (`__init__`)
Initializes the service instance by specifying the target directory where files will be saved or read.

- **Parameters**:
  - `target_directory`: The directory where files will be stored or retrieved from.

- **Usage**: Allows you to set the target directory for all read and write operations.

---

### `save_data(self, data, target_filename) -> bool`
Saves the data to a JSON file.

- **Parameters**:
  - `data`: The data to be saved in the file.
  - `target_filename`: The name of the file in which the data should be saved.

- **Returns**: Returns `True` if the save is successful, otherwise `False`.

- **Usage**: Used to save data in JSON format to a specific file. A success or error message is displayed via **`UiService`**.

---

### `read_data_as_json(self, target_filename) -> any`
Reads data from a file in JSON format and returns it as a Python object.

- **Parameters**:
  - `target_filename`: The name of the file to read.

- **Returns**: Returns the data as a Python object if the read is successful, otherwise `None`.

- **Usage**: Used to read JSON files and convert them into Python objects. If an error occurs, an error message is displayed via **`UiService`**.

---

### `read_data_as_txt(self, target_filename)`
Reads data from a text (TXT) file and returns a set of the read lines.

- **Parameters**:
  - `target_filename`: The name of the file to read.

- **Returns**: Returns a set containing the read lines if the read is successful, otherwise `None`.

- **Usage**: Used to read text files and return the lines as a set (eliminating duplicates). If an error occurs, an error message is displayed via **`UiService`**.

---

# `CypherService` API

## Description
The **`CypherService`** class allows the use of multiple encryption methods (Caesar, RSA, and custom) to encrypt and decrypt messages. It also provides key generation, encryption algorithm validity checks, and error handling for cryptographic operations.

---

## Main Methods

### `CypherService()` (`__init__`)
Initializes the encryption service instance with various encryption methods.

- **Parameters**: None
- **Usage**: Defines the available encryption methods (Caesar, RSA, Custom) and initializes the service's configuration attributes.

---

### `is_cypher_valid(self, algo_code: int | str) -> bool`
Checks if a given algorithm code is valid.

- **Parameters**:
  - `algo_code`: The encryption algorithm code to check (either as `int` or `str`).

- **Returns**: Returns `True` if the algorithm code is valid, otherwise `False`.

- **Usage**: Used to check the validity of an encryption algorithm before attempting to use it.

---

### `get_encryption_keys(self, encryption_method: int | str) -> any`
Generates and returns the keys needed for the specified encryption algorithm.

- **Parameters**:
  - `encryption_method`: The encryption algorithm code (either as `int` or `str`).

- **Returns**: Returns the generated keys for the algorithm, or an error if key generation fails.

- **Usage**: Generates keys for the selected encryption algorithm (e.g., public and private keys for RSA).

---

### `encrypt_master(self, algo_code: int, message: str, key: any) -> any`
Encrypts a given message using a specified encryption algorithm and key.

- **Parameters**:
  - `algo_code`: The encryption algorithm code (either as `int` or `str`).
  - `message`: The message to encrypt.
  - `key`: The key used for encryption.

- **Returns**: Returns the encrypted message if the operation is successful, or an error if the operation fails.

- **Usage**: Used to encrypt a message using the specified algorithm and key. Errors are handled and displayed via **`UiService`**.

---

### `decrypt_master(self, algo_code: int, _hash: str, key: any) -> any`
Decrypts a given message using a specified encryption algorithm and key.

- **Parameters**:
  - `algo_code`: The encryption algorithm code (either as `int` or `str`).
  - `_hash`: The encrypted message to decrypt.
  - `key`: The key used for decryption.

- **Returns**: Returns the decrypted message if the operation is successful, or an error if the operation fails.

- **Usage**: Used to decrypt a message using the specified algorithm and key. Errors are handled and displayed via **`UiService`**.

---

### `cypher_get_attr(self, algo_code: int, attr: str) -> any`
Checks if an encryption algorithm has a specific attribute and returns it.

- **Parameters**:
  - `algo_code`: The encryption algorithm code (either as `int` or `str`).
  - `attr`: The name of the attribute to check.

- **Returns**: Returns the specified attribute if present, otherwise `None`.

- **Usage**: Used to retrieve additional attributes of an encryption algorithm (e.g., a key generation method).

---

### `close_master(self)`
Closes all ongoing encryption methods.

- **Parameters**: None
- **Usage**: Properly closes all resources associated with encryption methods.

---

# `InteractionService` API

## Description
The **`InteractionService`** class handles user interactions for obtaining inputs, requesting confirmations, and retrieving login information. It provides methods for validating entered data types and managing exceptions related to interruption or cancellation of actions.

---

## Main Methods

### `InteractionService() (__init__)`
Initializes the interaction service instance.

- **Parameters**: None
- **Usage**: Initializes the program's exit command (currently unused).

---

### `get_input_from_user(mess: str, expected_type: type = str, ask_once: bool=False) -> any`
Requests input from the user and checks its type.

- **Parameters**:
  - `mess`: The message to display to the user.
  - `expected_type`: The expected type for input conversion (default: `str`).
  - `ask_once`: If `True`, does not ask for the input again if it is invalid or empty.

- **Returns**: The user input converted to the expected type. If `ask_once` is `True` and the input is empty or invalid, it returns `None`.

- **Usage**: Used to obtain values from the user while checking their validity. If the input is invalid, the user is prompted to enter a value again.

---

### `get_approval_user(self, mess: str, expected_type: type, ask_one: bool=False) -> bool`
Asks the user for a confirmation (e.g., a yes/no response).

- **Parameters**:
  - `mess`: The message to display to the user to request confirmation.
  - `expected_type`: The expected type for the response (e.g., `str`).
  - `ask_one`: If `True`, asks for confirmation only once.

- **Returns**: Returns `True` if the user approves (answer 'y'), `False` otherwise.

- **Usage**: Used to obtain a binary response from the user, such as a confirmation to proceed with an action.

---

### `get_credentials(self, parameters: list, list_cred: ()) -> any`
Retrieves credentials based on user-provided parameters or asks the user to select a login identifier.

- **Parameters**:
  - `parameters`: A list of parameters provided by the command line (e.g., the ID of a credential).
  - `list_cred`: A function to display the list of available credentials.

- **Returns**: Returns a tuple `(exists, cred_id)` where `exists` indicates if the credentials exist in the database, and `cred_id` is the identifier selected by the user.

- **Usage**: Allows the user to choose an identifier from a set of stored credentials or input a specific identifier through parameters or manual entry.

---

# `SecurityService` API

## Description
The **`SecurityService`** class provides functionalities for managing password security. It checks password strength, generates strong passwords from a dictionary, and validates passwords against security criteria. The class also handles specific exceptions for weak or incorrect passwords.

---

## Main Methods

### `SecurityService() (__init__)`
Initializes the password security service instance.

- **Parameters**: None
- **Usage**: Initializes the dictionary of letters and special characters for password transformations.

---

### `password_strength(password: str) -> (str, bool)`
Evaluates the strength of a given password.

- **Parameters**:
  - `password`: The password to evaluate.

- **Returns**: A tuple containing a message evaluating the password strength and a boolean indicating whether the password is secure enough (`True` if the password is strong, `False` otherwise).

- **Usage**: Used to check if a password meets security requirements such as length, presence of uppercase, lowercase, numbers, and special characters.

---

### `generate_strong_password(desired_length: int=12, length_range=(8, 16)) -> str`
Generates a strong password based on a dictionary of real words, adding complexity with numbers and special characters.

- **Parameters**:
  - `desired_length`: The desired length for the generated password (default: 12).
  - `length_range`: The acceptable length range for the generated password (default: between 8 and 16 characters).

- **Returns**: The generated password as a string.

- **Usage**: Used to automatically generate a secure and complex password by combining common words and special characters.

---

## Custom Exceptions

### `PasswordLength`
Raised when the length of the password does not meet the defined minimum or maximum requirements.

- **Parameters**:
  - `min_length`: The minimum length of the password.
  - `max_length`: The maximum length of the password.

- **Usage**: This exception is used when a password does not meet the specified length requirements.

---

### `PasswordSecurity`
Raised when the password does not meet any of the security requirements (uppercase, lowercase, digit, special character).

- **Parameters**: None
- **Usage**: Used when the password does not conform to the security criteria defined in the `password_strength` method.

---

### `Vulnerability`
A generic exception for any detected security vulnerability.

- **Parameters**: None
- **Usage**: This exception can be used to signal any vulnerability related to a password or insufficient security configuration.

### `QuitRequested`
Raised when a user requests to exit the application.

- **Usage**: Used to handle interruptions requested by the user, such as entering `-quit`.

---
