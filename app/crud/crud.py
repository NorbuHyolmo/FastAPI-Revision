from app.db import SessionLocal
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models import Book, Author
from app.exceptions import BookNotFound, DuplicateISBN
from app.schemas import BookCreate, BookUpdate


def get(db: Session, book_id: int) -> Book:
    book = db.get(Book, book_id)
    if book is None:
        raise BookNotFound(book_id)
    return book


def list_(
    db: Session, skip: int = 0, limit: int = 20, q: str | None = None
) -> list[Book]:
    stmt = select(Book).options(selectinload(Book.author))

    if q:
        stmt = stmt.where(Book.title.ilike(f"%{q}%"))

    stmt = stmt.order_by(Book.id.desc()).offset(skip).limit(limit)

    return db.scalars(stmt).all()


def create(db: Session, data: BookCreate) -> Book:
    author = db.scalar(select(Author).where(Author.name == data.author))
    if author is None:
        author = Author(name=data.author)
        db.add(author)

    book = Book(**data.model_dump(exclude={"author"}), author=author)
    db.add(book)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateISBN(data.isbn) from exc

    db.refresh(book)
    return book


def delete(db: Session, book_id: int) -> None:
    book = get(db, book_id)
    db.delete(book)
    db.commit()


def update(db: Session, book_id: int, data: BookUpdate) -> Book:
    book = get(db, book_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book
