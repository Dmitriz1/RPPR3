from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    last_name: Mapped[str] = mapped_column(String(100))   # Фамилия
    first_name: Mapped[str] = mapped_column(String(100))  # Имя
    faculty: Mapped[str] = mapped_column(String(100))    # Факультет
    course_name: Mapped[str] = mapped_column(String(100)) # Курс
    grade: Mapped[int] = mapped_column(Integer)          # Оценка