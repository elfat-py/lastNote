from termcolor import cprint

class Text:
    def mainMenuOptions(self):
        cprint('Welcome to the lastTodo app!', 'yellow')
        cprint('What would you like to do?', 'green')
        cprint('1. Add a Note', 'red')
        cprint('2. View Notes', 'red')
        cprint('3. View Today\'s notes', 'red')
        cprint('4. Delete a note', 'red')
        cprint('0. Exit', 'red')

    def dateTimeOptions(self):
        cprint("When is the note needed?", 'red')
        cprint("1. Today", 'red')
        cprint("2. Tomorrow", 'red')
        cprint("3. After a specific number of days", 'red')
        cprint("4. Enter a specific date (e.g., 2024-12-31)", 'red')
        cprint("5. Go back to the main menu", 'magenta')
        cprint("Please choose an option:", 'yellow')

    def showNotes(self, note, formatted_date):
        cprint('|---------------------------------|', 'red')
        cprint('| ID: ' + str(note[0]) + ' |', 'blue')
        cprint('| Date: ' + formatted_date + ' |', 'blue')
        cprint('| Title: ' + note[2] + ' |', 'blue')
        cprint('| Body: ' + note[3] + ' |', 'blue')
        cprint('|---------------------------------|', 'red')
