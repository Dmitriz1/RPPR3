import pandas as pd
from sqlalchemy.orm import Session
from models import Student
from crud import add_student

def fill_db_from_csv(db: Session, csv_path="students.csv"):
    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        student = Student(
            last_name=row['Фамилия'],
            first_name=row['Имя'],
            faculty=row['Факультет'],
            subject=row['Курс'],   # это строка!
            grade=float(row['Оценка'])
        )
        add_student(db, student)