from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db, engine
from models import Base
from crud import (
    add_student,
    get_students,
    get_students_by_faculty,
    get_unique_courses,
    get_students_by_course_low_grade,
    get_avg_grade_by_faculty,
    update_student_grade,
    delete_student
)
from fill_data import fill_db_from_csv
from export_csv import export_db_to_csv

# Создание таблиц (если не используешь Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Students API")


# Заполнение базы из CSV
@app.post("/fill")
def fill_database(db: Session = Depends(get_db)):
    fill_db_from_csv(db)
    return {"message": "Database filled from CSV"}


# Получить всех студентов
@app.get("/students")
def list_students(db: Session = Depends(get_db)):
    return get_students(db)


# Студенты по факультету
@app.get("/students/faculty/{faculty}")
def students_by_faculty(faculty: str, db: Session = Depends(get_db)):
    return get_students_by_faculty(db, faculty)


# Уникальные курсы (предметы)
@app.get("/courses")
def unique_courses(db: Session = Depends(get_db)):
    return get_unique_courses(db)


# Студенты по предмету с оценкой ниже 30
@app.get("/students/course/{subject}/low")
def students_low_grade(subject: str, db: Session = Depends(get_db)):
    return get_students_by_course_low_grade(db, subject)


# Средний балл по факультету
@app.get("/faculty/{faculty}/avg")
def avg_grade(faculty: str, db: Session = Depends(get_db)):
    avg = get_avg_grade_by_faculty(db, faculty)
    return {"faculty": faculty, "average_grade": avg}


# Обновление оценки студента
@app.put("/students/{student_id}")
def update_grade(student_id: int, new_grade: float, db: Session = Depends(get_db)):
    student = update_student_grade(db, student_id, new_grade)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# Удаление студента
@app.delete("/students/{student_id}")
def delete(student_id: int, db: Session = Depends(get_db)):
    student = delete_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted"}


# Экспорт базы в CSV
@app.get("/export")
def export_csv(db: Session = Depends(get_db)):
    export_db_to_csv(db)
    return {"message": "Database exported to CSV"}