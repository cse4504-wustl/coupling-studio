from dataclasses import dataclass


@dataclass(frozen=True)
class BookSummary:
    isbn: str
    title: str
    author: str
    status: str
