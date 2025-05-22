from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
import sqlite3

app = FastAPI()

# 📌 Схема користувача (для запитів)
class UserCreate(BaseModel):
    username: str
    email: EmailStr

# 📌 Схема користувача (для відповідей)
class User(UserCreate):
    id: int

# 📌 Ініціалізація бази
def init_db():
    with sqlite3.connect("users.db") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
init_db()

# 📌 Отримати всі користувачі
def get_all_users() -> List[User]:
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email FROM users")
        rows = cursor.fetchall()
        return [User(id=row[0], username=row[1], email=row[2]) for row in rows]

# 📌 Отримати одного користувача
def get_user_by_id(user_id: int) -> User:
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return User(id=row[0], username=row[1], email=row[2])
        raise HTTPException(status_code=404, detail="User not found")

# 📌 Створити користувача
def create_user(user: UserCreate) -> User:
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email) VALUES (?, ?)",
                (user.username, user.email)
            )
            user_id = cursor.lastrowid
            return User(id=user_id, username=user.username, email=user.email)
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="Email already exists")

# 🔹 /users/{user_id} — Отримати одного користувача
@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    return get_user_by_id(user_id)

# 🔹 /users — Отримати список усіх користувачів
@app.get("/users", response_model=List[User])
def read_users():
    return get_all_users()

# 🔹 /create_user — Створити нового користувача
@app.post("/create_user", response_model=User)
def create_new_user(user: UserCreate):
    return create_user(user)
