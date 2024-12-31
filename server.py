from datetime import datetime

from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

DB_PATH = "todo.db"

# Initialize the database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        token TEXT UNIQUE NOT NULL
    )
    ''')
    # Create todo table
    cursor.execute('''
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
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def homepage():
    return render_template("homepage.html")

# User registration
@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    username = data.get("username")
    token = data.get("token")

    if not username or not token:
        return jsonify({"message": "Missing username or token"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, token) VALUES (?, ?)", (username, token))
        conn.commit()
        conn.close()
        return jsonify({"message": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"message": "Username already exists"}), 400

# User authentication
@app.route("/auth", methods=["POST"])
def authenticate_user():
    data = request.json
    token = data.get("token")

    if not token:
        return jsonify({"message": "Missing token"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE token = ?", (token,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"user": user, "user_id": user[0], "username": user[1]}), 200
    return jsonify({"message": "Invalid token"}), 401

# Add a note
@app.route("/notes", methods=["POST"])
def add_note():
    data = request.json
    user_id = data.get("user_id")
    title = data.get("title")
    body = data.get("body")
    needed_time = data.get("neededTime")
    time = data.get("time")

    if not user_id or not title or not needed_time:
        return jsonify({"message": "Missing required fields"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO todo (user_id, time, title, body, neededTime) 
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, time, title, body, needed_time))
    conn.commit()
    conn.close()
    return jsonify({"message": "Note added successfully"}), 201

# Get notes for a user
@app.route("/notes/<int:user_id>", methods=["GET"])
def get_notes(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todo WHERE user_id = ?", (user_id,))
    notes = cursor.fetchall()
    conn.close()
    return jsonify({"notes": notes}), 200

# Get today's notes for a user
@app.route("/notes/today/<int:user_id>", methods=["GET"])
def get_today_notes(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todo WHERE user_id = ? AND neededTime LIKE ?", (user_id, f"{datetime.now().strftime('%Y-%m-%d')}%"))
    notes = cursor.fetchall()
    conn.close()
    return jsonify({"notes": notes}), 200


# Delete a note
@app.route("/notes", methods=["DELETE"])
def delete_note():
    data = request.json
    user_id = data.get("user_id")
    note_id = data.get("note_id")

    if not user_id or not note_id:
        return jsonify({"message": "Missing required fields"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todo WHERE id = ? AND user_id = ?", (note_id, user_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Note deleted successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
