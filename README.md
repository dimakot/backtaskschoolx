# Task Manager API

REST API для управления задачами.

## Стек

- **FastAPI** — веб-фреймворк
- **SQLAlchemy** — ORM
- **PostgreSQL** — база данных
- **Pydantic** — валидация данных
- **Alembic** — миграции БД
- **Uvicorn** — ASGI сервер

## Структура

```
backtask/
├── main.py              # Точка входа
├── alembic.ini          # Конфиг Alembic
├── api/
│   └── tasks.py         # Эндпоинты задач
├── schemas/
│   └── task.py          # Pydantic-схемы
├── database/
│   ├── db.py            # Подключение к PostgreSQL
│   └── models.py        # SQLAlchemy модель
└── alembic/
    └── versions/        # Файлы миграций
```

## Установка и запуск

### 1. Установить uv (менеджер пакетов)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Клонировать репозиторий

```bash
git clone <url-репозитория>
cd backtask
```

### 3. Установить зависимости

```bash
uv sync
```

### 4. Настроить PostgreSQL

Создать базу данных:

```bash
psql -d postgres -c "CREATE DATABASE backtask;"
```

Если у вас другой пользователь/пароль PostgreSQL, задайте переменную окружения:

```bash
export DATABASE_URL="postgresql://ваш_пользователь:ваш_пароль@localhost:5432/backtask"
```

Также нужно обновить `sqlalchemy.url` в файле `alembic.ini` на ваш URL.

### 5. Применить миграции

```bash
uv run alembic upgrade head
```

### 6. Запустить сервер

```bash
uv run python -m uvicorn main:app --reload
```

Документация API: http://127.0.0.1:8000/docs

## API эндпоинты

| Метод  | URL             | Описание                  |
|--------|-----------------|---------------------------|
| POST   | /tasks/         | Создать задачу            |
| GET    | /tasks/         | Получить все задачи       |
| GET    | /tasks/{id}     | Получить задачу по ID     |
| PATCH  | /tasks/{id}     | Обновить задачу           |
| DELETE | /tasks/{id}     | Удалить задачу            |

## Валидация

- **title** — от 3 до 100 символов, не может быть пустым, не может начинаться с цифры
- **status** — `new`, `in_progress` или `done`
- **priority** — `low`, `medium` или `high`
