# Task Manager API

REST API для управления задачами.

## Стек

- **FastAPI** — веб-фреймворк
- **SQLAlchemy** — ORM
- **PostgreSQL** — база данных
- **Pydantic** — валидация данных
- **Alembic** — миграции БД
- **Uvicorn** — ASGI сервер

## Что реализовано

- Подключение к БД через SQLAlchemy
- Аутентификация: `/auth/register`, `/auth/login`
- Repository Pattern для работы с данными
- Защищенные эндпоинты задач (Bearer Token)

## Структура

```
backtask/
├── main.py              # Точка входа
├── alembic.ini          # Конфиг Alembic
├── api/
│   ├── auth.py          # Эндпоинты авторизации
│   └── tasks.py         # Эндпоинты задач
├── auth/
│   └── dependencies.py  # Проверка токена и текущий пользователь
├── core/
│   └── security.py      # JWT и хеширование пароля
├── repositories/
│   ├── user_repository.py
│   └── task_repository.py
├── schemas/
│   ├── auth.py          # Pydantic-схемы для auth
│   └── task.py          # Pydantic-схемы задач
├── database/
│   ├── db.py            # Подключение к PostgreSQL
│   └── models.py        # SQLAlchemy модели User/Task
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
export SECRET_KEY="ваш_секретный_ключ"
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

### Аутентификация

| Метод | URL            | Описание                              |
|-------|----------------|---------------------------------------|
| POST  | /auth/register | Регистрация пользователя + JWT токен |
| POST  | /auth/login    | Логин пользователя + JWT токен       |

### Задачи (требуют Bearer Token)

| Метод  | URL             | Описание                  |
|--------|-----------------|---------------------------|
| POST   | /tasks/         | Создать задачу            |
| GET    | /tasks/         | Получить все задачи       |
| GET    | /tasks/{id}     | Получить задачу по ID     |
| PATCH  | /tasks/{id}     | Обновить задачу           |
| DELETE | /tasks/{id}     | Удалить задачу            |

Пример передачи токена:

```bash
curl -X GET http://127.0.0.1:8000/tasks/ \
    -H "Authorization: Bearer <ваш_access_token>"
```

## Валидация

- **title** — от 3 до 100 символов, не может быть пустым, не может начинаться с цифры
- **status** — `new`, `in_progress` или `done`
- **priority** — `low`, `medium` или `high`
