from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from app.exceptions import BookNotFound
from app.routers.books import router, DB
from app.schemas import BookRead

app = FastAPI(
    title="BookShelf API",
    version="1.0.0",
    summary="Manage a personal library and enrich it with OpenLibrary API",
    description="A simple API for managing a bookshelf.",
    contact={"name": "My Team", "email": "myteam@example.com"},
    license_info={"name": "MIT"},
    openapi_tags=[
        {"name": "Books", "description": "Create, Read, Update, Delete Books"},
        {"name": "default", "description": "Liveliness and Readiness probes"},
    ],
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


# @app.get("/page", response_model_exclude_none=True, response_model=list[BookRead])
# def get_pagination():
#     return list(DB.values())
