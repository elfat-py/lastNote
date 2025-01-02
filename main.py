import sys
import uuid
import requests
from datetime import datetime, timedelta
from termcolor import cprint

from text import Text

SERVER_URL = "https://last-note.tech/"


class Todo:
    def __init__(self):
        self.current_user = None
        self.text = Text()

    def main(self):
        """
        Main entry point for the application. Handles user authentication
        and navigates through the main menu or directly to 'auto' mode.
        """
        try:
            if not self.current_user:
                self.loginUser()  # Attempt to authenticate the user
                if not self.current_user:
                    self.authenticate_user()

            # Auto mode: Show today's notes and exit
            if len(sys.argv) > 1 and sys.argv[1] == 'auto':
                cprint(f"Welcome, {self.current_user['username']}!", "yellow")
                cprint("The notes for today are as follows:", "green")
                self.view_notes(today=True)
                return  # Exit after showing today's notes in auto mode

            # Main menu for manual interaction
            cprint(f"Welcome, {self.current_user['username']}!", "yellow")
            while True:
                self.text.mainMenuOptions()
                choice = input("Choose an option: ").strip()

                if choice == '1':
                    self.add_note()
                elif choice == '2':
                    self.view_notes()
                elif choice == '3':
                    self.view_notes(today=True)
                elif choice == '4':
                    self.delete_note()
                elif choice == '0':
                    cprint("Exiting...", "red")
                    exit(0)
                else:
                    cprint("Invalid choice. Please try again.", "red")

        except KeyboardInterrupt:
            cprint("Exiting...", "red")
            exit(0)
        except Exception as e:
            cprint(f"An unexpected error occurred: {str(e)}", "red")
            exit(1)

    def authenticate_user(self):
        self.text.authenticateOptions()
        choice = input("Choose an option: ").strip()
        if choice == '1':
            self.registerUser()
        elif choice == '2':
            self.loginUser()
        elif choice == '0':
            cprint("Exiting...", "red")
            exit(0)
        else:
            cprint("Something somehow, somewhere went wrong", "red")
            exit(1)

    def registerUser(self):
        username = input("Enter your username: ").strip()
        token = str(uuid.uuid4())  # Generate a unique token
        response = requests.post(f"{SERVER_URL}/register", json={"username": username, "token": token})

        with open("auth_token.txt", "w") as token_file:
            token_file.write(token)
        print("Token saved to auth_token.txt")

        if response.status_code == 201:
            cprint("User registered successfully.", "green")
        else:
            cprint(f"Failed to register user: {response.json()['message']}", "red")
            exit(1)

    def loginUser(self):
        try:
            with open("auth_token.txt", "r") as file:
                token = file.read().strip()
        except FileNotFoundError:
            cprint("No token found. If you have a token place it into some txt file auth_token.txt on the root dir where lastNote.exe file is located for auto-login", "yellow")
            cprint("Please register or enter your token.", "red")
            token = input("Enter your token: ").strip()

        response = requests.post(f"{SERVER_URL}/auth", json={"token": token})
        if response.status_code == 200:
            self.current_user = response.json()
            cprint("User logged in successfully.", "green")
        else:
            cprint(f"Failed to login user: {response.json()['message']}", "red")
            self.authenticate_user()

    def add_note(self):
        title = input("Enter note title: ").strip()
        body = input("Enter note body: ").strip()

        needed_time = self.getDate()
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        response = requests.post(f"{SERVER_URL}/notes", json={
            "user_id": self.current_user["user_id"],
            "title": title,
            "body": body,
            "time": time,
            "neededTime": needed_time
        })

        if response.status_code == 201:
            cprint("Note added successfully.", "green")
            self.main()
        else:
            cprint(f"Failed to add note: {response.json()['message']}", "red")
            self.main()

    def getDate(self):
        self.text.dateTimeOptions()
        choice = input("Choose an option (1/2/3/4): ").strip()

        if choice == '1':  # Today
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elif choice == '2':  # Tomorrow
            return (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        elif choice == '3':  # After a specific number of days
            try:
                days = int(input("Enter the number of days: ").strip())
                return (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                print("Invalid input. Please enter a valid number of days.")
                return self.getDate()
        elif choice == '4':  # Custom date and time
            dateInput = input("Enter the date in YYYY-MM-DD format: ").strip()
            timeInput = input("(Press enter to skip) Enter the time in HH:MM:SS format: ").strip()
            if not timeInput:
                timeInput = '00:00:00'
            try:
                return datetime.strptime(f"{dateInput} {timeInput}", '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                print("Invalid date or time format. Please try again.")
                return self.getDate()
        elif choice == '0':
            self.main()
        else:
            print("Invalid choice. Please try again.")
            return self.getDate()

    def view_notes(self, today=False):
        """
        Fetch and display notes for the current user.
        If 'today' is True, only today's notes are fetched; otherwise, fetch all notes.
        """
        try:
            user_id = self.current_user["user_id"]
            endpoint = f"{SERVER_URL}/notes/today/{user_id}" if today else f"{SERVER_URL}/notes/{user_id}"
            response = requests.get(endpoint)

            if response.status_code == 200:
                notes = response.json().get("notes", [])
                if not notes:
                    cprint('No notes found, have a great time!', 'red')
                    self._handle_exit_or_menu()
                    return

                for note in notes:
                    formatted_date = note[4]  # Assuming note[4] contains the date
                    self.text.showNotes(note, formatted_date)

                self._handle_exit_or_menu()
            else:
                error_message = response.json().get('message', 'Unknown error occurred')
                cprint(f"Failed to retrieve notes: {error_message}", "red")
                self.main()

        except Exception as e:
            cprint(f"An error occurred while fetching notes: {str(e)}", "red")
            self.main()

    def _handle_exit_or_menu(self):
        """
        Handle behavior based on whether the program is in 'auto' mode or manual mode.
        """
        if len(sys.argv) > 1 and sys.argv[1] == 'auto':
            cprint('Here')
            cprint('Press any key to exit...', 'green')
            input()
            sys.exit(0)
        else:
            cprint('Press any key to return to the main menu...', 'green')
            input()
            self.main()

    def delete_note(self):
        try:
            user_id = self.current_user["user_id"]

            response = requests.get(f"{SERVER_URL}/notes/{user_id}")
            if response.status_code == 200:
                notes = response.json()["notes"]
                if not notes:
                    cprint('No notes found!', 'red')
                    cprint('Press any key to return to the main menu...', 'green')
                    input()
                    self.main()

                for note in notes:
                    formatted_date = note[4]
                    self.text.showNotes(note, formatted_date)

                cprint('Enter the ID of the note you want to delete:', 'yellow')
                try:
                    note_id = int(input().strip())
                    response = requests.delete(f"{SERVER_URL}/notes", json={
                        "user_id": user_id,
                        "note_id": note_id
                    })

                    if response.status_code == 200:
                        cprint(f'Note with ID {note_id} has been deleted successfully.', 'green')
                        self.main()
                    else:
                        cprint(f"Failed to delete note: {response.json()['message']}", "red")
                        self.main()

                except ValueError:
                    cprint('Invalid ID entered. Please try again.', 'red')
                    return self.delete_note()

            else:
                cprint(f"Failed to retrieve notes: {response.json()['message']}", "red")
                self.main()
        except KeyboardInterrupt:
            cprint('Exiting...', 'red')
            exit(0)


if __name__ == "__main__":
    todo = Todo()
    todo.main()
