class BookNotFound(Exception):
    def __init__(self, book_id: int):
        self.book_id = book_id


class DuplicateISBN(Exception):
    def __init__(self, isbn: str):
        self.isbn = isbn
