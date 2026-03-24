from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Student

engine = create_engine("sqlite:///./students.db")

with Session(engine) as session:
    # Берем первые 5 записей из базы
    stmt = select(Student).limit(5)
    results = session.execute(stmt).scalars().all()

    print("Первые 5 студентов из базы данных:")
    for s in results:
        print(f"{s.last_name} {s.first_name} | Факультет: {s.faculty} | Оценка: {s.grade}")