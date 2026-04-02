from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from database.db import engine, AsyncSessionLocal
from api.tasks import router as tasks_router
from api.auth import router as auth_router
from api.comments import router as comments_router
from api.files import router as files_router
from api.health import router as health_router
from core.exceptions import TaskNotFound, CommentNotFound


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - инициализация БД
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        print("✓ Подключение к PostgreSQL успешно")
    except Exception as e:
        print(f"✗ Ошибка подключения к PostgreSQL: {e}")
    
    yield
    
    # Shutdown - закрытие соединений
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(comments_router)
app.include_router(files_router)
