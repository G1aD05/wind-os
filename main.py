import os
from pathlib import Path
import subprocess
import shutil

__version__ = "1.0.0-alpha"


class Main:
    def __init__(self):
        self.username = None
        self.password = None
        self.login_attempts = 0

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
        with open(Path(f"home/Applications/time.py"), 'w') as file:
            file.write("""import datetime as dt
print(f" The time and date right now is {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")""")
        os.mkdir(f"home/{username}/.secrets")
        os.mkdir(f"home/{username}/Downloads")
        os.mkdir(f"home/{username}/Documents")
        with open(Path(f"home/{username}/.secrets/password.txt"), 'w') as file:
            file.write(password)
        with open(Path(f"home/.system/device-name.txt"), 'w') as file:
            file.write(input("Let's name your device: "))
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
        raise Exception(f"WindOS has crashed! Error code: {code}")

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
            app_name = input("App name: ")
            result = subprocess.run(["python", f"home/Applications/{app_name}.py"], capture_output=True, text=True)
            print(f"\n{result.stdout}\n")
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

    def startup(self):
        print("Starting...")
        if not os.path.isdir(f"{os.getcwd()}/home"):
            self.setup()
            return ""
        else:
            print("Successfully booted!")
            self.login()

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
        command = input(f"{self.username}@{open('home/.system/device-name.txt', 'r').read()} % ")
        if command == "exit":
            self.main()
        else:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"\n{result.stdout}")
            self.terminal()


if __name__ == "__main__":
    program = Main()
    program.startup()
