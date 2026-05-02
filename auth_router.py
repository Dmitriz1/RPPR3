from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User

router = APIRouter(prefix="/auth", tags=["auth"])

sessions = {}  # примитивное хранилище сессий: token -> user_id

@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered", "user_id": user.id}

import uuid

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.username == username,
        User.password == password
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = str(uuid.uuid4())

    # 🔥 авторизация по ID
    sessions[token] = user.id

    return {"token": token}

from fastapi import Header

@router.post("/logout")
def logout(authorization: str = Header(...)):
    sessions.pop(authorization, None)
    return {"message": "Logged out"}

def get_current_user(authorization: str = Header(...)):
    user_id = sessions.get(authorization)

    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return user_id