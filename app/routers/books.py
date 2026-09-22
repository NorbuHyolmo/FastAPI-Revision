from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.exceptions import BookNotFound
from app.schemas import BookCreate, BookRead

_db: dict[int, str] = {}
_next_id = 1

router = APIRouter(prefix="/books", tags=["Books"])


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
def get_book(book_id: int):
    if book_id not in _db:
        raise BookNotFound(book_id)
    return _db[book_id]


def get_all_books():
    return list(_db.values())


books = Annotated[list, Depends(get_all_books)]


@router.get(
    "/",
    response_model=list[BookRead],
    summary="Get All Books",
    description="Fetch all the books from the database",
    responses={200: {"description": "Fetched All Books Successfully"}},
)
def list_books(books: books):
    return books


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
def create_book(book: BookCreate):
    global _next_id
    record = book.model_dump() | {
        "id": _next_id,
        "created_at": datetime.now(timezone.utc),
    }
    _db[_next_id] = record
    _next_id += 1
    return record


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
def delete_book(book_id: int):
    if book_id in _db:
        del _db[book_id]
        return {"message": "Book deleted successfully."}
    else:
        raise BookNotFound(book_id)
