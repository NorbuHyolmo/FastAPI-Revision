from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=0, le=2100)
    isbn: str | None = Field(default=None)

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        return value.strip()


class BookRead(BaseModel):
    id: int
    title: str
    author: str
    year: int
    isbn: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
