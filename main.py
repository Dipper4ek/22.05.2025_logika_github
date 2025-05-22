from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import List

app = FastAPI()

class User(BaseModel):
    id: int
    username: str
    email: EmailStr

users: List[User] = [
    User(id=1, username="john_doe", email="john@example.com"),
    User(id=2, username="alice", email="alice@example.com"),
    User(id=3, username="bob", email="bob@example.com"),
]

@app.get("/get_users", response_model=List[User])
def get_users():
    return {"message": "Good get did", "List users: ": users}

@app.post("/post_users", response_model=List[User])
def post_users(user: User):
    users.append(user)
    return {"message": "Good post did", "List users: ": users}

