import pandas as pd
from database import SessionLocal
from models import Student


def import_students(file_path: str):
    db = SessionLocal()
    try:
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            db.add(Student(
                name=row["name"],
                faculty=row["faculty"],
                subject=row["subject"],
                grade=row["grade"]
            ))

        db.commit()
    finally:
        db.close()


def delete_students(ids: list[int]):
    db = SessionLocal()
    try:
        db.query(Student).filter(Student.id.in_(ids)).delete(synchronize_session=False)
        db.commit()
    finally:
        db.close()