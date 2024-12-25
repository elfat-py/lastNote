import sqlite3
from datetime import datetime


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('todo1.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS todo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            title TEXT,
            body TEXT,
            neededTime TEXT
        )
        ''')
        self.conn.commit()

    def save(self, time, title, body, neededTime):
        self.cursor.execute('''
        INSERT INTO todo (time, title, body, neededTime) VALUES (?, ?, ?, ?)
        ''', (time, title, body, neededTime))
        self.conn.commit()

    def getAll(self):
        self.cursor.execute('''
        SELECT * FROM todo
        ''')
        return self.cursor.fetchall()


    def deleteNote(self, id):
        self.cursor.execute('''
        DELETE FROM todo WHERE id = ?
        ''', (id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def getTodayNotes(self):
        self.cursor.execute('''
        SELECT * FROM todo WHERE neededTime LIKE ?
        ''', (f'{datetime.now().strftime("%Y-%m-%d")}%',))
        return self.cursor.fetchall()
