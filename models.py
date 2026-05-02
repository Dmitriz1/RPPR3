from sqlalchemy import Column, Integer, String, Float
from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    faculty = Column(String)
    subject = Column(String)
    grade = Column(Float)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)