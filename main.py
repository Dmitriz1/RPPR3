from fastapi import FastAPI
from database import engine, Base
from auth_router import router as auth_router
from student_router import router as student_router
from tasks_router import router as tasks_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(student_router)
app.include_router(tasks_router)