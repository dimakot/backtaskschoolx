from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: Optional[str] = None
    status: str = "new"
    priority: str = "medium"

    @field_validator("title")
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("Название не может быть пустым")
        if value[0].isdigit():
            raise ValueError("Название не должно начинаться с цифры")
        return value.strip()

    @field_validator("status")
    def validate_status(cls, value):
        allowed = ["new", "in_progress", "done"]
        if value not in allowed:
            raise ValueError(f"Статус должен быть одним из: {', '.join(allowed)}")
        return value

    @field_validator("priority")
    def validate_priority(cls, value):
        allowed = ["low", "medium", "high"]
        if value not in allowed:
            raise ValueError(f"Приоритет должен быть одним из: {', '.join(allowed)}")
        return value


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None

    @field_validator("title")
    def validate_title(cls, value):
        if value is None:
            return value
        if not value.strip():
            raise ValueError("Название не может быть пустым")
        if value[0].isdigit():
            raise ValueError("Название не должно начинаться с цифры")
        return value.strip()

    @field_validator("status")
    def validate_status(cls, value):
        if value is None:
            return value
        allowed = ["new", "in_progress", "done"]
        if value not in allowed:
            raise ValueError(f"Статус должен быть одним из: {', '.join(allowed)}")
        return value

    @field_validator("priority")
    def validate_priority(cls, value):
        if value is None:
            return value
        allowed = ["low", "medium", "high"]
        if value not in allowed:
            raise ValueError(f"Приоритет должен быть одним из: {', '.join(allowed)}")
        return value


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}
