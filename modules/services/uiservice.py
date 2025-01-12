from rich import print

class UiService:
    def __init__(self, debug_mode=False):
        self.prefix = "[Password Manager]"
        self.messageColorThemes = {
            "error": "bold red",
            "lighterror": "bright_red",
            "warning": "bold italic yellow",
            "success": "bold italic green",

            "title": "bold blue",
            "info": "bright_blue",
            "enums": "magenta",

            "blank": "white"
        }

        self.debugMode = debug_mode

    def display_header(self, header: str) -> None:
        print(f'[bold orange1] {self.prefix} [/bold orange1]: [underline]{header}[/underline]')

    def display(self, message: str, _type: str = None) -> None:
        color_init = ""
        color_end = ""

        if _type and _type.lower() in self.messageColorThemes:
            color_id = self.messageColorThemes[_type.lower()]

            color_init = f"[{color_id}]"
            color_end = f"[/{color_id}]"

        output = f"{color_init}{message}{color_end}"

        return print(f"[bold orange1] {self.prefix} [/bold orange1]: {output}")

    def display_crypto(self, header: str, data: list | dict) -> None:
        self.display_header(header)

        for algo_id in data:
            algo_data = data[algo_id]

            if not algo_data:
                self.display(f'[bright red]Error while reading data for encryptor enum {algo_id}[/bright red]')
                continue
            algo_name, algo_desc, algo_code = algo_data['name'], algo_data['description'], algo_data['code']

            self.display(
                "[bold]Encryption method[/bold] : [bold bright_magenta]{0}[/bold bright_magenta]".format(algo_name))
            self.display(' -> [italic]Description[/italic] : {0}'.format(algo_desc))
            self.display(" -> [italic]Access Code[/italic] : {0}".format(algo_code))

    def display_helpers(self, header: str, data: list | dict) -> None:
        self.display_header(header)

        for commandName in data:
            command_data = data[commandName]
            print('\n')
            self.display(f'[bold blue]{commandName}[/bold blue]')

            for dataName in command_data:
                data_content = command_data[dataName]

                self.display(f'[bold italic]{dataName.capitalize()}[/bold italic]: {data_content}')

        print('\n\n')

    def display_passwords(self, header: str, data: list | dict, decrypter) -> None:
        entries = len(data)
        self.display(
            f'[bright_yellow]   ==> {header} {entries == 0 and ": None" or ": " + str(entries)}[/bright_yellow]\n')

        for passData in data:
            decrypted_pw = decrypter.decrypt_master(passData['crypto'], passData['value'], key=passData['key'])

            self.display(f'     -> [italic]ID: [bright_green]{passData["id"]}[/bright_green][/italic]')
            self.display(f'     -> [italic]Value:[/italic] [bold red]{decrypted_pw}[/bold red]')
            self.display(f'     -> [italic]Encryption: {passData["crypto"]}[/italic]')

            self.display('-' * 25 + '\n')

    ## Asks user for information, data or confirmation
    def prompt_user(self, prompt_message: str, question: bool = False) -> any:
        prompt_message = '[blink cyan]' + prompt_message + '[/blink cyan]'

        self.display(prompt_message)