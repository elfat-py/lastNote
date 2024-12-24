from datetime import datetime
import sqlite3

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
        print('1. Add a note')
        print('2. View notes')
        print('3. View Today\'s note')
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
        savedTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.save(savedTime, noteTitle, noteBody)
        print('Note saved!')
        self.main()

    def viewNotes(self):
        notes = db.getAll()
        for note in notes:
            print(note[0])

        cprint('Press any key to continue...', 'green')
        input()
        self.main()
    def viewTodayNotes(self):
        notes = db.getTodayNotes()
        for note in notes:
            print(note)

        cprint('Press any key to continue...', 'green')
        input()
        self.main()

if __name__ == '__main__':
    todo = Todo()
    todo.main()
