import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Student

# Подключаемся к базе
engine = create_engine("sqlite:///./students.db")


def transfer_data():
    with open('students.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        with Session(engine) as session:
            # Очистим таблицу перед заполнением (опционально)
            session.query(Student).delete()

            for row in reader:
                new_student = Student(
                    last_name=row['Фамилия'],
                    first_name=row['Имя'],
                    faculty=row['Факультет'],
                    course_name=row['Курс'],
                    grade=int(row['Оценка'])
                )
                session.add(new_student)

            session.commit()
            print("Данные успешно перенесены из CSV в базу данных!")


if __name__ == "__main__":
    transfer_data()