from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services import *
from auth_router import get_current_user
from models import Student

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/")
def get_all(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return get_students(db)


@router.post("/")
def create(student: Student, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return add_student(db, student)


@router.get("/faculty/{faculty}")
def by_faculty(faculty: str, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return get_students_by_faculty(db, faculty)


@router.get("/courses")
def courses(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return get_unique_courses(db)


@router.get("/low/{subject}")
def low(subject: str, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return get_students_by_course_low_grade(db, subject)


@router.get("/avg/{faculty}")
def avg(faculty: str, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return get_avg_grade_by_faculty(db, faculty)


@router.put("/{student_id}")
def update(student_id: int, new_grade: float, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return update_student_grade(db, student_id, new_grade)


@router.delete("/{student_id}")
def delete(student_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return delete_student(db, student_id)