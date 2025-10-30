from fastapi import FastAPI
from src.database import init_db
from src.routers import teachers , students , sessions
from src.models import *
app = FastAPI()

init_db()


app.include_router(teachers.router)
app.include_router(students.router)
app.include_router(sessions.router)
