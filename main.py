from datetime import datetime, timedelta
import os
from termcolor import cprint
from database import Database
from text import Text


class Todo:
    def __init__(self):
        self.text = Text()
        self.db = Database()
        self.current_user = None  # Store the logged-in user's ID and username

    def main(self):
        try:
            # Handle user login or registration
            if not self.current_user:
                self.authenticate_user()

            # Show the main menu
            self.text.mainMenuOptions()
            choice = input().strip()
            if choice == '1':
                self.addNote()
            elif choice == '2':
                notes = self.db.get_all(self.current_user[0])  # Fetch notes for the logged-in user
                self.viewNotes(notes)
            elif choice == '3':
                notes = self.db.get_today_notes(self.current_user[0])  # Fetch today's notes for the user
                self.viewNotes(notes)
            elif choice == '4':
                self.deleteNote()
            elif choice == '0':  # Adjusted to '0' to match "Exit" correctly
                cprint('Exiting...', 'red')
                exit(0)
            else:
                cprint('Invalid choice! Please try again.', 'red')
                self.main()
        except KeyboardInterrupt:
            cprint('Exiting...', 'red')
            exit(0)

    def authenticate_user(self):
        cprint("1. Register\n2. Login", 'green')
        choice = input("Choose an option: ").strip()

        if choice == '1':
            username = input("Enter username: ").strip()
            self.db.register_user(username)
            cprint("User registered successfully. Please log in to continue.", 'green')
            self.authenticate_user()
        elif choice == '2':
            token_file = input("Enter the path to your token file: ").strip()
            print(token_file)
            try:
                with open(token_file, "r") as file:
                    token = file.read().strip()
                    user = self.db.authenticate_user(token)
                    if user:
                        self.current_user = user
                        cprint(f"Welcome back, {self.current_user[1]}!", 'green')
                    else:
                        cprint("Invalid token. Please try again.", 'red')
                        self.authenticate_user()
            except FileNotFoundError:
                cprint("Token file not found. Please try again.", 'red')
                self.authenticate_user()
        else:
            cprint("Invalid choice. Please try again.", 'red')
            self.authenticate_user()

    def addNote(self):
        try:
            cprint('Enter the title of your note:', 'green')
            noteTitle = input().strip()
            cprint('Enter the body of your note:', 'green')
            noteBody = input().strip()
            neededTime = self.getDate()
            savedTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.db.save(self.current_user[0], savedTime, noteTitle, noteBody, neededTime)  # Associate note with user
            cprint('Note successfully saved!', 'green')
            self.main()
        except KeyboardInterrupt:
            cprint('Exiting...', 'red')
            exit(0)

    def deleteNote(self):
        try:
            cprint('Here are your current notes:', 'green')
            notes = self.db.get_all(self.current_user[0])
            if not notes:
                cprint('No notes available to delete.', 'red')
                return self.main()
            cprint('Enter the ID of the note you want to delete:', 'yellow')
            try:
                note_id = int(input().strip())
                self.db.delete_note(self.current_user[0], note_id)  # Ensure only user's notes can be deleted
                cprint(f'Note with ID {note_id} has been deleted successfully.', 'green')
            except ValueError:
                cprint('Invalid ID entered. Please try again.', 'red')
                return self.deleteNote()
            self.main()
        except KeyboardInterrupt:
            cprint('Exiting...', 'red')
            exit(0)

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

    def viewNotes(self, notes):
        try:
            if not notes:
                cprint('No notes found!', 'red')
                cprint('Press any key to return to the main menu...', 'green')
                input()
                self.main()

            for note in notes:
                formatted_date = note[4]
                self.text.showNotes(note, formatted_date)

            cprint('Press any key to return to the main menu...', 'green')
            input()
            self.main()
        except KeyboardInterrupt:
            cprint('Exiting...', 'red')
            exit(0)


if __name__ == '__main__':
    todo = Todo()
    todo.main()
