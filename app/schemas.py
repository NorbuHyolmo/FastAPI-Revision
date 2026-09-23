from datetime import datetime
from typing import Generic, TypeVar
from pydantic import BaseModel, Field, field_validator


T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    skip: int
    limit: int


class AuthorResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=0, le=2100)
    isbn: str | None = Field(default=None)

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        return value.strip()

    model_config = {
        "json_schema_extra": {
            "examples": [{"title": "Dune", "author": "Frank Herbert", "year": 1965}]
        }
    }


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    author: str | None = Field(default=None, min_length=1, max_length=100)
    year: int | None = Field(default=None, ge=0, le=2100)


class BookRead(BaseModel):
    id: int
    title: str
    author: AuthorResponse
    year: int
    isbn: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
