import uuid
import sqlite3

# Database setup
def setup_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        token TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Register a new user
def register_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    token = str(uuid.uuid4())
    try:
        cursor.execute("INSERT INTO users (username, token) VALUES (?, ?)", (username, token))
        conn.commit()
        print(f"User registered successfully.\nYour token: {token}")
        with open("auth_token.txt", "w") as token_file:
            token_file.write(token)
        print("Token saved to auth_token.txt")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    conn.close()

# Authenticate using a token
def authenticate_user(token):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE token = ?", (token,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

# Example usage
if __name__ == "__main__":
    setup_database()
    print("1. Register\n2. Login")
    choice = input("Choose an option: ")

    if choice == "1":
        username = input("Enter username: ")
        register_user(username)
    elif choice == "2":
        token_file = input("Enter the path to your token file: ")
        try:
            with open(token_file, "r") as file:
                token = file.read().strip()
                username = authenticate_user(token)
                if username:
                    print(f"Welcome back, {username}!")
                else:
                    print("Invalid token.")
        except FileNotFoundError:
            print("Token file not found.")
