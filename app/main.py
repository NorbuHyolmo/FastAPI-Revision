from fastapi import FastAPI, Query, status
from fastapi.responses import JSONResponse
from app.schemas import BookCreate, BookRead
from datetime import datetime, timezone
from app.exceptions import BookNotFound
from app.routers.books import router

app = FastAPI(
    title="BookShelf API",
    version="1.0.0",
    description="A simple API for managing a bookshelf.",
)

app.include_router(router)


@app.exception_handler(BookNotFound)
def book_not_found_handler(request, exc: BookNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"Book with ID {exc.book_id} not found."},
    )


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
