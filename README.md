# LastNote

Welcome to **LastNote**, the **ultimate procrastinator-friendly** task management terminal app you never knew you needed but now can't live without!

Tired of forgetting your plans until it's way too late? Fear not! **LastNote** is here to haunt your terminal with the tasks you keep running from. It'll pop up every time you open your pc

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
- **Persistent Storage**: Your notes are stored in a database so they won't disappear (we hope so).

---

## Installation

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
   Make sure sqlite3 is available (it comes pre-installed with Python).

4. Compile the project into an executable (optional but recommended for deployment):
   ```bash
   pyinstaller --onefile main.py
   ```
   The compiled file will be located in the `dist` folder.

5. Set up automatic terminal execution:

   #### Command Prompt (Windows):
   Use the provided `startTerminalWithNotes.bat` batch file for automatic startup.

---

## Batch File Logic: `startTerminalWithNotes.bat`

The `startTerminalWithNotes.bat` file ensures that **LastNote** runs only once during a session when the computer starts. Here’s how it works:

### Code Breakdown

```batch
@echo off
REM Marker file to track if the application has already run
set markerFile=C:\Users\alex\lastNote_marker.txt

REM Check if the marker file exists
if exist "%markerFile%" (
    echo Application already run for this session.
    exit
)

REM Create the marker file
echo "LastNote executed on %date% %time%" > "%markerFile%"

REM Run the application
cd /d "C:\path\to\project\lastNote"
start "" "dist\lastNote.exe" auto
exit
```

### Explanation:

- **Marker File**: A marker file (`C:\Users\alex\lastNote_marker.txt`) is created after the program is run for the first time in a session. This prevents the program from being executed multiple times during the same session.
- **Check Marker File**: If the marker file exists, the script exits immediately without launching the program.
- **Create Marker File**: If the marker file does not exist, it is created with the current date and time.
- **Run the Application**: The `lastNote.exe` executable is launched in auto mode, displaying today’s notes immediately.
- **Session Management**: The marker file ensures the program only runs once per session. You can remove the marker file manually or set up a shutdown script to delete it.

---

## Usage

### Run the app manually:
```bash
python main.py
```

### Run the app automatically on startup:
Copy `startTerminalWithNotes.bat` to your Startup folder:
Windows: 
```bash
shell:startup
```
(Your auth token should be on that same folder as well.)


Reboot your system, and **LastNote** will greet you on the first terminal session.

### Run the app manually with the auto flag:
```bash
dist\lastNote.exe auto
```

---

## File Structure

- `main.py`: The heart of the app; handles user interaction.
- `text.py`: Provides UI elements and options for the user.
- `startTerminalWithNotes.bat`: Ensures the app runs automatically during system startup.
- `lastNote_marker.txt`: A marker file created during the first session to prevent multiple runs in the same session.
- `dist\lastNote.exe`: The compiled executable of the app.

---

## Known Bugs

- If you enter an invalid date format, the app might ask you to try again...forever.
- Running auto mode without proper setup might cause the app to close prematurely.

---

## Pro Tips

- **Marker File Removal**: If you want to re-run the app in the same session, delete the `lastNote_marker.txt` file manually.
- **Startup Optimization**: Use the auto flag sparingly if you need more control over when the app launches.

---

## License

This project is licensed under the MIT License
---

## Credits

Developed by a dev for devs

---

## Happy Tasking! Or...Happy Procrastinating!

