from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String, nullable=False)   # Фамилия
    first_name = Column(String, nullable=False)  # Имя
    faculty = Column(String, nullable=False)     # Факультет
    subject = Column(String, nullable=False)     # Курс (предмет!)
    grade = Column(Float, nullable=False)        # Оценка