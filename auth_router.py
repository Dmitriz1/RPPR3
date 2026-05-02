from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
from models import User
import uuid

router = APIRouter(prefix="/auth", tags=["auth"])

sessions = {}


@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise HTTPException(400, "User exists")

    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"user_id": user.id}


@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.username == username,
        User.password == password
    ).first()

    if not user:
        raise HTTPException(401, "Invalid credentials")

    token = str(uuid.uuid4())
    sessions[token] = user.id

    return {"token": token}


@router.post("/logout")
def logout(authorization: str = Header(...)):
    sessions.pop(authorization, None)
    return {"message": "ok"}


def get_current_user(authorization: str = Header(...)):
    user_id = sessions.get(authorization)

    if not user_id:
        raise HTTPException(401, "Unauthorized")

    return user_id