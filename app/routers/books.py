from fastapi import APIRouter, status
from app.schemas import BookCreate, BookRead
from app.exceptions import BookNotFound
from datetime import datetime, timezone

_db: dict[int, str] = {}
_next_id = 1

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int):
    if book_id not in _db:
        raise BookNotFound(book_id)
    return _db[book_id]


@router.get("/", response_model=list[BookRead])
def list_books():
    return list(_db.values())


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    global _next_id
    record = book.model_dump() | {
        "id": _next_id,
        "created_at": datetime.now(timezone.utc),
    }
    _db[_next_id] = record
    _next_id += 1
    return record


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    if book_id in _db:
        del _db[book_id]
        return {"message": "Book deleted successfully."}
    else:
        raise BookNotFound(book_id)
