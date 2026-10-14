from dto.book_summary import BookSummary


def list_books(conn):
    rows = conn.execute("SELECT isbn, title, author, due_date FROM books ORDER BY title").fetchall()
    return [
        BookSummary(isbn, title, author, f"due {due}" if due else "available")
        for isbn, title, author, due in rows
    ]
