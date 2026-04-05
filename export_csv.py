import pandas as pd
from sqlalchemy.orm import Session
from models import Student

def export_db_to_csv(db: Session, csv_path="students_export.csv"):
    students = db.query(Student).all()

    data = [
        {
            "Фамилия": s.last_name,
            "Имя": s.first_name,
            "Факультет": s.faculty,
            "Курс": s.subject,
            "Оценка": s.grade
        }
        for s in students
    ]

    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)