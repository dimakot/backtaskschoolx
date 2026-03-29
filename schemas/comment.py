from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class CommentCreate(BaseModel):
    content: str = Field(min_length=1, max_length=500)

    @field_validator("content")
    def validate_content(cls, value: str):
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Текст комментария не может быть пустым")
        return cleaned


class CommentResponse(BaseModel):
    id: int
    task_id: int
    author_id: int
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
