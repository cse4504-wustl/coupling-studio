from datetime import date

from dto.return_receipt import ReturnReceipt
from entities.member import Account, FinePolicy, Member


def return_book(conn, isbn, today):
    cursor = conn.cursor()

    cursor.execute("SELECT borrower_id, due_date FROM books WHERE isbn = ?", (isbn,))
    row = cursor.fetchone()
    if row is None or row[0] is None:
        raise ValueError(f"Book {isbn} is not checked out")
    borrower_id, due_date = row[0], date.fromisoformat(row[1])

    cursor.execute("SELECT id, name, type, balance, daily_fine FROM members WHERE id = ?", (borrower_id,))
    m = cursor.fetchone()
    member = Member(m[0], m[1], m[2], Account(m[3], FinePolicy(m[4])))

    days_late = max(0, (today - due_date).days)
    fine = days_late * member.get_account().get_fine_policy().get_daily_rate()
    member.get_account().set_balance(member.get_account().get_balance() + fine)

    cursor.execute("UPDATE members SET balance = ? WHERE id = ?",
                   (member.get_account().get_balance(), member.member_id))
    cursor.execute("UPDATE books SET borrower_id = NULL, due_date = NULL WHERE isbn = ?", (isbn,))
    conn.commit()

    return ReturnReceipt(isbn, days_late, fine, member.get_account().get_balance())
