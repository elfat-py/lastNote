from datetime import datetime, timedelta
import sqlite3
import os
from random import choice

from termcolor import cprint

from database import Database

# I want that every time i open the terminal to display some message if i have some tasks to do
# They will be saved by ID
# We will save them into some DB (sqlite3)
# when we are in the terminal it should be able to show us the tasks of the day (only titles)
# create a new database if not exists
db = Database()


class Todo:
    def main(self):
        cprint('Welcome to the lastTodo app!', 'red')
        print('What would you like to do?')
        print('1. Add a Note')
        print('2. View Notes')
        print('3. View Today\'s notes')
        print('4. Delete a note')
        print('5. Exit')
        choice = input()
        if choice == '1':
            self.addNote()
        elif choice == '2':
            self.viewNotes()
        elif choice == '3':
            self.viewTodayNotes()
        elif choice == '4':
            exit()
        else:
            print('Invalid choice!')
            self.main()


    def addNote(self):
        cprint('Note title!', 'green')
        noteTitle = input()
        cprint('Note body!', 'green')
        noteBody = input()
        neededTime = self.getDate()
        savedTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.save(savedTime, noteTitle, noteBody, neededTime)
        print('Note saved!')
        self.main()

    def getDate(self):
        cprint("When is the note needed?", 'red')
        cprint("1. Today", 'red')
        cprint("2. Tomorrow", 'red')
        cprint("3. After a specific number of days", 'red')
        cprint("4. Enter a specific date (e.g., 2024-12-31)", 'red')
        cprint("0. Go back to the main menu", 'magenta')
        cprint("Please choose an option:", 'yellow')
        choice = input("Choose an option (1/2/3/4): ").strip()

        if choice == '1':  # Today
            return datetime.now()
        elif choice == '2':  # Tomorrow
            return datetime.now() + timedelta(days=1)
        elif choice == '3':  # After a specific number of days
            days = int(input("Enter the number of days: "))
            return datetime.now() + timedelta(days=days)
        elif choice == '4':
            # TODO: the user might want to skip the time part
            dateInput = input("Enter the date in YYYY-MM-DD format: ")
            try:
                return datetime.strptime(dateInput, '%Y-%m-%d %H:%M:%S')  # Adjust format if needed
            except ValueError:
                print("Invalid date format. Please try again.")
                return self.getDate()  # Retry on invalid input
        elif choice == '0':
            self.main()
        else:
            print("Invalid choice. Please try again.")
            return self.getDate()  # Retry on invalid input

    def viewNotes(self):
        notes = db.getAll()

        # Check if there are any notes
        if len(notes) == 0:
            cprint('No notes found!', 'red')
            cprint('Press any key to continue...', 'green')
            input()
            self.main()
            return  # Return early to avoid further execution

        iterationNote = 1  # Initialize the iteration counter outside the loop

        for note in notes:
            # Handle showing a message for older notes
            if iterationNote == 3:
                cprint('Continue with older notes...', 'green')
                iterationNote = 1  # Reset the counter
                input()
                os.system('cls')

            # Parse the date (assuming note[1] is a string from the database)
            try:
                date_obj = datetime.strptime(note[1], '%Y-%m-%d %H:%M:%S')  # Adjust format if needed
                formatted_date = date_obj.strftime('%d-%m-%Y %H:%M:%S')
            except ValueError:
                formatted_date = 'Invalid date format'

            # Display the note
            cprint('|---------------------------------|', 'red')
            cprint('| ID: ' + str(note[0]) + ' |', 'blue')
            cprint('| Date: ' + formatted_date + ' |', 'blue')
            cprint('| Title: ' + note[2] + ' |', 'blue')
            cprint('| Body: ' + note[3] + ' |', 'blue')
            cprint('|---------------------------------|', 'red')

            iterationNote += 1  # Increment the counter

        # Prompt to continue
        cprint('Press any key to continue...', 'green')
        input()
        self.main()

    def viewTodayNotes(self):
        notes = db.getTodayNotes()
        if len(notes) == 0:
            cprint('No notes found!', 'red')
            cprint('Press any key to continue...', 'green')
            input()
            self.main()
            return  # Return early to avoid further execution

        iterationNote = 1  # Initialize the iteration counter outside the loop

        for note in notes:
            # Handle showing a message for older notes
            if iterationNote == 3:
                cprint('0. Go back to the main menu', 'magenta')
                cprint('Enter to continue with older notes... ', 'green')
                iterationNote = 1  # Reset the counter
                choice = input()
                if choice == '1':
                    self.main()
                os.system('cls')

            # Parse the date (assuming note[1] is a string from the database)
            try:
                date_obj = datetime.strptime(note[1], '%Y-%m-%d %H:%M:%S')  # Adjust format if needed
                formatted_date = date_obj.strftime('%d-%m-%Y %H:%M:%S')
            except ValueError:
                formatted_date = 'Invalid date format'

            # Display the note
            cprint('|---------------------------------|', 'red')
            cprint('| ID: ' + str(note[0]) + ' |', 'blue')
            cprint('| Date: ' + formatted_date + ' |', 'blue')
            cprint('| Title: ' + note[2] + ' |', 'blue')
            cprint('| Body: ' + note[3] + ' |', 'blue')
            cprint('|---------------------------------|', 'red')

            iterationNote += 1  # Increment the counter

        # Prompt to continue
        cprint('Press any key to continue...', 'green')
        input()
        self.main()

if __name__ == '__main__':
    todo = Todo()
    todo.main()
