import os
import time
from pathlib import Path
import subprocess
import shutil
from urllib.request import urlretrieve
import importlib.util
import importlib.machinery
import logging

__version__ = "1.0.2.1-alpha"


class Main:
    def __init__(self):
        self.username = None
        self.password = None
        self.login_attempts = 0
        self.boot_start_function = self.login
        self.setup_start_function = self.setup

    def setup(self):
        print("\nHello, let's get your device set up!")
        username = input("\nUsername: ")
        password = input("Password: ")
        if username == "":
            print("\nUsername cannot be empty!")
            self.setup()
        os.mkdir('home')
        os.mkdir('home/.system')
        os.mkdir(f'home/{username}')
        os.mkdir(f'home/Applications')
        urlretrieve('https://raw.githubusercontent.com/G1aD05/wind-os/main/apps/downloader.py',
                    'home/Applications/downloader.py')
        urlretrieve('https://raw.githubusercontent.com/G1aD05/wind-os/main/apps/time.py', 'home/Applications/time.py')
        os.mkdir(f"home/{username}/.secrets")
        os.mkdir(f"home/{username}/Downloads")
        os.mkdir(f"home/{username}/Documents")
        with open(Path(f"home/{username}/.secrets/password.txt"), 'w') as file:
            file.write(password)
        with open(Path(f"home/.system/device-name.txt"), 'w') as file:
            file.write(input("Let's name your device: "))
        open(Path(f"home/.system/logs"), 'w')
        print("Setup complete!")
        self.login()

    def new_user(self):
        print("\nHello, let's get your account set up!")
        username = input("\nUsername: ")
        password = input("Password: ")
        if username == "":
            print("Username cannot be emtpy")
            self.new_user()
        os.mkdir(f'home/{username}')
        os.mkdir(f"home/{username}/.secrets")
        os.mkdir(f"home/{username}/Downloads")
        os.mkdir(f"home/{username}/Documents")
        with open(Path(f"home/{username}/.secrets/password.txt"), 'w') as file:
            file.write(password)
        print("Setup complete!")
        self.login()

    def panic(self, code):
        if os.path.isfile('home/.system/logs'):
            file = open('home/.system/logs', 'r').read()
            open('home/.system/logs', 'w').write(f'{file}\n{f"WindOS has crashed! Error code: {code}"}')
        logging.error(Exception(f"WindOS has crashed! Error code: {code}"))

    def login(self):
        print("\nPlease log in.")
        self.username = input("\nUsername: ")
        self.password = input("Password: ")
        if self.login_attempts >= 5:
            raise Exception("Too many login attempts!")
        if not os.path.isdir(f"home/{self.username}"):
            print("Login info was wrong!")
            self.login_attempts += 1
            self.login()
        else:
            if not os.path.isfile(f"home/{self.username}/.secrets/password.txt"):
                self.panic("PASSWORD_SAVE_FILE_NOT_FOUND")
            with open(f'home/{self.username}/.secrets/password.txt', 'r') as file:
                password = file.read()
            if not self.password == password:
                print("Login info was wrong!")
                self.login_attempts += 1
                self.login()
            else:
                print("Logging in...")
                self.login_attempts = 0
                self.main()

    def main(self):
        print("Welcome, select an option")
        print("""
1. Run an app
2. Make a user
3. Log out
4. New document
5. Open document
6. Move file
7. Terminal
8. Reboot
9. Power Off
10. Settings
        """)
        selection = input("Selection: ")
        if selection == "1":
            try:
                app_name = input("App name: ")
                loader = importlib.machinery.SourceFileLoader(app_name, f'home/Applications/{app_name}.py')
                spec = importlib.util.spec_from_loader(loader.name, loader)
                module = importlib.util.module_from_spec(spec)
                loader.exec_module(module)
                module.main()
                time.sleep(3)
                self.main()
            except:
                print('Failed to run app!')
                self.main()
        elif selection == "2":
            self.new_user()
        elif selection == "3":
            self.login()
        elif selection == "4":
            try:
                with open(Path(f'home/{self.username}/Documents/{input("Document name: ")}'), 'w') as file:
                    file.write(input("Contents: "))
                self.main()
            except:
                print("Failed to make a new document")
                self.main()
        elif selection == "5":
            print("Edit or View")
            selection = input("Selection: ")
            if selection == "Edit":
                with open(Path(input("Path to file: ")), 'w') as file:
                    file.write(input("Contents: "))
                self.main()
            elif selection == "View":
                with open(Path(input("Path to file: ")), 'r') as file:
                    print(f"Contents: {file.read()}")
                self.main()
        elif selection == "6":
            shutil.move(input("Source Directory: "), input("Destination directory: "))
            self.main()
        elif selection == "7":
            print("\nLaunching terminal...")
            self.terminal()
        elif selection == "8":
            print("Rebooting...")
            self.startup()
        elif selection == "9":
            print("\nPowering Down...")
            exit()
        elif selection == "10":
            self.settings()
        else:
            self.main()

    def bios(self):
        print("""1. Boot the OS
2. Configure boot start function
3. Configure setup start function
        """)
        selection = input("Selection: ")
        if selection == "1":
            if not os.path.isdir(f"{os.getcwd()}/home"):
                self.setup_start_function()
            else:
                print("Successfully booted!")
                self.boot_start_function()
        elif selection == "2":
            function = input("Function name (ex: self.main NO PARENTHESES): ")
            try:
                self.boot_start_function = getattr(self, function)
                self.bios()
            except:
                self.panic("FUNCTION_NOT_FOUND_ERROR")
        elif selection == "3":
            function = input("Function name (ex: main NO PARENTHESES): ")
            try:
                self.setup_start_function = getattr(self, function)
                self.bios()
            except:
                self.panic("FUNCTION_NOT_FOUND_ERROR")
        else:
            self.bios()

    def startup(self):
        print("Starting...")
        print("""1. Install WindOS/Boot WindOS
2. Open the BIOS
        """)
        selection = input("Selection: ")
        if selection == "1":
            if not os.path.isdir(f"{os.getcwd()}/home"):
                self.setup_start_function()
            else:
                print("Successfully booted!")
                self.boot_start_function()
        elif selection == "2":
            print("Opening the BIOS")
            print("\nBIOS Launched!")
            self.bios()

    def settings(self):

        print("""
1. Delete an account
2. Factory reset this device
3. Exit
        """)
        selection = input("Selection: ")
        if selection == "1":
            user = input("User to remove: ")
            if user == "":
                print("Username cannot be nothing!")
                self.settings()
            try:
                shutil.rmtree(f'home/{user}')
                self.settings()
            except:
                print("Failed to delete user")
                self.settings()
        elif selection == "2":
            if input("Please enter your password: ") == open(f'home/{self.username}/.secrets/password.txt', 'r').read():
                if input("Confirm? Y/n: ") == "Y":
                    try:
                        shutil.rmtree('home/')
                        self.startup()
                    except:
                        self.panic("FAILED_TO_FACTORY_RESET")
                else:
                    self.settings()
            else:
                print("Wrong password")
                self.settings()
        elif selection == "3":
            self.main()

    def terminal(self):
        command = input(f"{self.username}@{open('home/.system/device-name.txt', 'r').read()} {os.getcwd()} % ")
        if command == "exit":
            self.main()
        else:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"\n{result.stdout}")
            self.terminal()


if __name__ == "__main__":
    program = Main()
    program.startup()
