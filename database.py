import sqlite3
import uuid
from datetime import datetime


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.cursor = self.conn.cursor()

        # Create users table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            token TEXT UNIQUE NOT NULL
        )
        ''')

        # Create todo table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS todo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            time TEXT,
            title TEXT,
            body TEXT,
            neededTime TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
        ''')
        self.conn.commit()

    # User registration
    def register_user(self, username):
        token = str(uuid.uuid4())  # Generate a unique token
        try:
            self.cursor.execute('''
            INSERT INTO users (username, token) VALUES (?, ?)
            ''', (username, token))
            self.conn.commit()
            print(f"User registered successfully.\nYour token: {token}")
            with open("auth_token.txt", "w") as token_file:
                token_file.write(token)
            print("Token saved to auth_token.txt")
        except sqlite3.IntegrityError:
            print("Username already exists.")

    # User authentication
    def authenticate_user(self, token):
        self.cursor.execute('''
        SELECT id, username FROM users WHERE token = ?
        ''', (token,))
        result = self.cursor.fetchone()
        if result:
            return result  # Returns (user_id, username)
        return None

    # Save a new note
    def save(self, user_id, time, title, body, neededTime):
        self.cursor.execute('''
        INSERT INTO todo (user_id, time, title, body, neededTime) VALUES (?, ?, ?, ?, ?)
        ''', (user_id, time, title, body, neededTime))
        self.conn.commit()

    # Get all notes for a user
    def get_all(self, user_id):
        self.cursor.execute('''
        SELECT * FROM todo WHERE user_id = ?
        ''', (user_id,))
        return self.cursor.fetchall()

    # Delete a note
    def delete_note(self, user_id, note_id):
        self.cursor.execute('''
        DELETE FROM todo WHERE id = ? AND user_id = ?
        ''', (note_id, user_id))
        self.conn.commit()

    # Get today's notes for a user
    def get_today_notes(self, user_id):
        self.cursor.execute('''
        SELECT * FROM todo WHERE user_id = ? AND neededTime LIKE ?
        ''', (user_id, f'{datetime.now().strftime("%Y-%m-%d")}%',))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
