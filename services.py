from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Student
from redis_client import redis_client
from cache import cache


def serialize(student):
    return {
        "id": student.id,
        "name": student.name,
        "faculty": student.faculty,
        "subject": student.subject,
        "grade": student.grade
    }


# CREATE
def add_student(db: Session, student: Student):
    db.add(student)
    db.commit()
    db.refresh(student)

    redis_client.flushdb()
    return student


# READ all
@cache(ttl=120)
def get_students(db: Session):
    students = db.query(Student).all()
    return [serialize(s) for s in students]


# FILTER
@cache(ttl=120)
def get_students_by_faculty(db: Session, faculty: str):
    students = db.query(Student).filter(Student.faculty == faculty).all()
    return [serialize(s) for s in students]


# UNIQUE
@cache(ttl=120)
def get_unique_courses(db: Session):
    return [c[0] for c in db.query(Student.subject).distinct().all()]


# LOW GRADE
@cache(ttl=120)
def get_students_by_course_low_grade(db: Session, subject: str):
    students = db.query(Student).filter(
        Student.subject == subject,
        Student.grade < 30
    ).all()
    return [serialize(s) for s in students]


# AVG
@cache(ttl=120)
def get_avg_grade_by_faculty(db: Session, faculty: str):
    return db.query(func.avg(Student.grade)).filter(
        Student.faculty == faculty
    ).scalar()


# UPDATE
def update_student_grade(db: Session, student_id: int, new_grade: float):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student:
        student.grade = new_grade
        db.commit()
        db.refresh(student)
        redis_client.flushdb()

    return student


# DELETE
def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student:
        db.delete(student)
        db.commit()
        redis_client.flushdb()

    return student