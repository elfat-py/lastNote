# lastNote

Welcome to **lastNote**, the **ultimate procrastinator-friendly** task management app you never knew you needed but now can't live without!

Tired of forgetting your plans until it's way too late? Fear not! **lastNote** is here to haunt your terminal with the tasks you keep running from. It'll pop up every time you open your terminal, cheerfully reminding you of your unfulfilled responsibilities.

---

## Features

1. **Add Notes**: Write down your big ideas or "I'll definitely do this tomorrow" moments.
2. **View All Notes**: Remind yourself how productive you were (or weren’t).
3. **View Today's Notes**: Get called out on the tasks you’ve been avoiding today.
4. **Delete Notes**: Pretend they never existed.
5. **Humorous Terminal Presence**: No more escaping from your to-dos; they’ll greet you with a warm welcome every time you open your terminal.

---

## How It Works

- **Notes by ID**: Tasks are saved with a unique ID in an SQLite database.
- **Smart Filters**: View only today’s tasks or all tasks.
- **Persistent Storage**: Your notes are stored in a database so they won't disappear (unfortunately for you!).

---

## Installation

Follow these steps to get started with **lastNote**:

### Prerequisites
- Python 3.x installed on your machine.
- Basic knowledge of **procrastination**.

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/elfat-py/lastnote/
   ```

2. Navigate to the project folder:
   ```bash
   cd lastNote
   ```

3. Install dependencies:
   ```bash
   pip install termcolor
   ```

4. Make sure `sqlite3` is available (it comes pre-installed with Python).

5. Set up automatic terminal execution:
   - **Command Prompt (Windows)**:
     - Copy the provided `startTerminalWithNotes.bat` to the Startup folder:
       ```bash
       shell:startup
       ```
     - Now, every time you open your terminal, **lastNote** will greet you!

---

## Usage

Run the app manually:
```bash
python main.py
```

Or just open your terminal (if you set up the `.bat` file) and let **lastNote** do its magic. Here's what you can expect:

### Main Menu Options
1. **Add a Note**:
   - Title your task and give it a body (or skip it to "do it later").
   - Set a time: today, tomorrow, after X days, or pick a specific date.
2. **View Notes**:
   - See all your notes listed by ID, date, title, and body.
3. **View Today’s Notes**:
   - Only see tasks scheduled for today—so you’ll know exactly what to ignore.
4. **Delete Notes**:
   - Erase the evidence of your unproductivity.
5. **Exit**:
   - Run away (for now).

---

## File Structure

- **main.py**: The heart of the app; handles user interaction.
- **database.py**: Manages the SQLite database.
- **startTerminalWithNotes.bat**: Runs the app automatically every time the terminal is opened.
- **todo1.db**: The SQLite database where your notes are stored.

---

## Pro Tips

1. **Mess up a date?** No worries. Just delete the note and start over (like with most things in life).
2. **Too many notes?** Enjoy the fun of scrolling endlessly through your tasks.
3. **Afraid of commitment?** Use the "Delete Note" option liberally—we won’t judge.

---

## Known Bugs

1. If you enter an invalid date format, the app might ask you to try again...forever. (But hey, we all make mistakes.)
2. The terminal might feel a bit judgmental after showing your overdue tasks. Don’t take it personally.

---

## License

This project is licensed under the **MIT License**—freedom to procrastinate responsibly.

---

## Credits

**Developed with love and a healthy dose of sarcasm by YOU**. Thanks to Python and SQLite for enabling such wonderfully distracting projects.

Happy Tasking! Or...Happy Procrastinating!

