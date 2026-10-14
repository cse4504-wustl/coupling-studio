from datetime import timedelta

import config
from entities.book import Book, Loan


def checkout_book(conn, isbn, member_id, today):
    cursor = conn.cursor()

    cursor.execute("SELECT isbn, title, author, borrower_id FROM books WHERE isbn = ?", (isbn,))
    row = cursor.fetchone()
    if row is None:
        raise ValueError(f"No book with ISBN {isbn}")
    if row[3] is not None:
        raise ValueError(f"'{row[1]}' is already checked out")

    cursor.execute("SELECT type FROM members WHERE id = ?", (member_id,))
    member_row = cursor.fetchone()
    if member_row is None:
        raise ValueError(f"No member with id {member_id}")

    # Faculty get a longer loan period
    if member_row[0] == "faculty":
        config.LOAN_DAYS = config.FACULTY_LOAN_DAYS

    book = Book(row[0], row[1], row[2])
    book.loan = Loan(
        member_id=member_id,
        checkout_date=today,
        due_date=today + timedelta(days=config.LOAN_DAYS),
        renewals=0,
    )

    cursor.execute(
        "UPDATE books SET borrower_id = ?, due_date = ? WHERE isbn = ?",
        (member_id, book.loan.due_date.isoformat(), isbn),
    )
    conn.commit()
    return book.loan.due_date
