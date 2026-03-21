from pydantic import BaseModel, Field, field_validator


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=100)

    @field_validator("username")
    def validate_username(cls, value):
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Имя пользователя не может быть пустым")
        if " " in cleaned:
            raise ValueError("Имя пользователя не должно содержать пробелы")
        return cleaned


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
