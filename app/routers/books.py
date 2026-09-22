from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.exceptions import BookNotFound
from app.schemas import BookCreate, BookRead
from app.db import get_db
from app.crud import crud

router = APIRouter(prefix="/books", tags=["Books"])
DB = Annotated[Session, Depends(get_db)]


@router.get(
    "/{book_id}",
    response_model=BookRead,
    summary="Get a Book",
    description="Fetches the information about the book using a book id",
    responses={
        200: {"description": "Book Fetched Successfully"},
        404: {"description": "Book Not Found"},
        422: {"description": "Validation Failed"},
    },
)
def get_book(db: DB, book_id: int):
    return crud.get(db, book_id)


@router.get(
    "/",
    response_model=list[BookRead],
    summary="Get All Books",
    description="Fetch all the books from the database",
    responses={200: {"description": "Fetched All Books Successfully"}},
)
def list_books(db: DB, skip: int = 0, limit: int = 20, q: str | None = None):
    return crud.list_(db, skip, limit, q)


@router.post(
    "",
    response_model=BookRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a Book",
    description="Adds a book to a shelf. Titles are trimmed; ISBNs are not verified",
    responses={
        201: {"description": "Book Created"},
        409: {"description": "A book with this isbn already exists"},
        422: {"description": "Validation Failed"},
    },
)
def create_book(db: DB, book: BookCreate):
    return crud.create(db, book)


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a book",
    description="Delete a book from the database using book id",
    responses={
        204: {"description": "Book Deleted Successfully"},
        404: {"description": "Book with the provided id not found"},
        422: {"description": "Validation Failed"},
    },
)
def delete_book(db: DB, book_id: int):
    return crud.delete(db, book_id)
