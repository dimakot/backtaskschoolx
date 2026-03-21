from fastapi import FastAPI
from database.db import engine, Base
from api.tasks import router as tasks_router
from api.auth import router as auth_router

try:
    Base.metadata.create_all(bind=engine)
    print("Подключение к PostgreSQL успешно")
except Exception as e:
    print(f"Ошибка подключения к PostgreSQL: {e}")

app = FastAPI()

app.include_router(auth_router)
app.include_router(tasks_router)
