FROM python:3.13-slim

WORKDIR /app

ENV PATH="/root/.local/bin:$PATH"

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    uv sync --frozen

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uv run python -m uvicorn main:app --host 0.0.0.0 --port 8000"]
