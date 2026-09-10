import hashlib
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "app.db"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

TEST_USERS = [
    {"username": "admin", "password": "admin123", "role": "admin"},
    {"username": "testuser", "password": "password123", "role": "user"},
    {"username": "farmer", "password": "farmer123", "role": "user"},
    {"username": "demo", "password": "demo123", "role": "user"},
]

def seed_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"Connecting to database: {DB_PATH}")
    for u in TEST_USERS:
        uname = u["username"].strip().lower()
        pwd_hash = hash_password(u["password"])
        role = u["role"]
        
        cursor.execute("SELECT id FROM users WHERE username = ?", (uname,))
        row = cursor.fetchone()
        if row:
            cursor.execute(
                "UPDATE users SET password_hash = ?, role = ? WHERE username = ?",
                (pwd_hash, role, uname)
            )
            print(f"  [Updated] Username: '{uname}', Role: '{role}', Password: '{u['password']}'")
        else:
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (uname, pwd_hash, role)
            )
            print(f"  [Created] Username: '{uname}', Role: '{role}', Password: '{u['password']}'")

    conn.commit()
    conn.close()
    print("Test users seeded successfully!")

if __name__ == "__main__":
    seed_users()
