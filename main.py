from datetime import datetime, timedelta
import os
from termcolor import cprint
from database import Database
from text import Text
# I want that every time i open the terminal to display some message if i have some tasks to do
# They will be saved by ID
# We will save them into some DB (sqlite3)
# when we are in the terminal it should be able to show us the tasks of the day (only titles)

class Todo:
    def __init__(self):
        self.text = Text()
        self.db = Database()
    def main(self):
        try:
            self.text.mainMenuOptions()
            choice = input().strip()
            if choice == '1':
                self.addNote()
            elif choice == '2':
                notes = self.db.getAll()
                self.viewNotes(notes)
            elif choice == '3':
                notes = self.db.getTodayNotes()
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

    def addNote(self):
        try:
            cprint('Enter the title of your note:', 'green')
            noteTitle = input().strip()
            cprint('Enter the body of your note:', 'green')
            noteBody = input().strip()
            neededTime = self.getDate()
            savedTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.db.save(savedTime, noteTitle, noteBody, neededTime)
            cprint('Note successfully saved!', 'green')
            self.main()
        except KeyboardInterrupt:
            cprint('Exiting...', 'red')
            exit(0)

    def deleteNote(self):
        try:
            cprint('Here are your current notes:', 'green')
            notes = self.db.getAll()
            if not notes:
                cprint('No notes available to delete.', 'red')
                return self.main()
                # TODO: should find a better way to handle this
            # self.viewNotes(notes)  # Display all notes for reference
            cprint('Enter the ID of the note you want to delete:', 'yellow')
            try:
                note_id = int(input().strip())
                self.db.deleteNote(note_id)
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

            iterationNote = 1  # Counter for displaying notes
            for note in notes:
                if None in note:
                    cprint('Invalid note found. Skipping...', 'red')
                    continue
                if iterationNote == 3:  # Pause after every three notes
                    cprint('Continue with older notes...', 'green')
                    iterationNote = 1
                    input()
                    os.system('cls')

                try:
                    date_obj = datetime.strptime(note[4], '%Y-%m-%d %H:%M:%S')
                    formatted_date = date_obj.strftime('%d-%m-%Y %H:%M:%S')
                except ValueError:
                    formatted_date = 'Invalid date format'

                self.text.showNotes(note, formatted_date)
                iterationNote += 1

            cprint('Press any key to return to the main menu...', 'green')
            input()
            self.main()
        except KeyboardInterrupt:
            cprint('Exiting...', 'red')
            exit(0)



if __name__ == '__main__':
    todo = Todo()
    todo.main()
