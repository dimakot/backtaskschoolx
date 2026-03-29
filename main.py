from fastapi import FastAPI
from fastapi.responses import JSONResponse
from database.db import engine, Base
from api.tasks import router as tasks_router
from api.auth import router as auth_router
from api.comments import router as comments_router
from core.exceptions import TaskNotFound, CommentNotFound

try:
    Base.metadata.create_all(bind=engine)
    print("Подключение к PostgreSQL успешно")
except Exception as e:
    print(f"Ошибка подключения к PostgreSQL: {e}")

app = FastAPI()


@app.exception_handler(TaskNotFound)
def task_not_found_handler(request, exc: TaskNotFound):
    return JSONResponse(
        status_code=404,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


@app.exception_handler(CommentNotFound)
def comment_not_found_handler(request, exc: CommentNotFound):
    return JSONResponse(
        status_code=404,
        content={"error": {"code": exc.code, "message": exc.message}},
    )

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(comments_router)
