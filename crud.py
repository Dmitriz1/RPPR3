from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Student
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services import *
from auth_router import get_current_user

router = APIRouter(prefix="/students", tags=["students"])

# CREATE
def add_student(db: Session, student: Student):
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.post("/")
def create_student(
    student: Student,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)  # 🔒 защита
):
    return add_student(db, student)

# READ all
def get_students(db: Session):
    return db.query(Student).all()

@router.get("/")
def read_students(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return get_students(db)

# Студенты по факультету
def get_students_by_faculty(db: Session, faculty: str):
    return db.query(Student).filter(Student.faculty == faculty).all()

# Уникальные курсы (предметы)
def get_unique_courses(db: Session):
    return [c[0] for c in db.query(Student.subject).distinct().all()]

# Студенты по предмету с оценкой < 30
def get_students_by_course_low_grade(db: Session, subject: str):
    return db.query(Student).filter(
        Student.subject == subject,
        Student.grade < 30
    ).all()

# Средний балл по факультету
def get_avg_grade_by_faculty(db: Session, faculty: str):
    return db.query(func.avg(Student.grade)).filter(
        Student.faculty == faculty
    ).scalar()

@router.get("/faculty/{faculty}")
def students_by_faculty(
    faculty: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return get_students_by_faculty(db, faculty)

# UPDATE
def update_student_grade(db: Session, student_id: int, new_grade: float):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student:
        student.grade = new_grade
        db.commit()
        db.refresh(student)
    return student

@router.put("/{student_id}")
def update_grade(
    student_id: int,
    new_grade: float,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return update_student_grade(db, student_id, new_grade)

@router.delete("/{student_id}")
def delete(
    student_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return delete_student(db, student_id)

# DELETE
def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student:
        db.delete(student)
        db.commit()
    return student