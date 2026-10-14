import argparse
from datetime import date

from persistence.database import get_connection, init_db
from use_cases.checkout_book import checkout_book
from use_cases.import_books import import_books
from use_cases.list_books import list_books
from use_cases.return_book import return_book


def run():
    parser = argparse.ArgumentParser(description="Library lending system")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="create the database and sample members")

    p = sub.add_parser("import", help="import books from a supplier CSV file")
    p.add_argument("file")

    sub.add_parser("list", help="list all books")

    p = sub.add_parser("checkout", help="check out a book")
    p.add_argument("--isbn", required=True)
    p.add_argument("--member", required=True)
    p.add_argument("--date", help="checkout date YYYY-MM-DD (default: today)")

    p = sub.add_parser("return", help="return a book")
    p.add_argument("--isbn", required=True)
    p.add_argument("--date", help="return date YYYY-MM-DD (default: today)")

    args = parser.parse_args()
    today = date.fromisoformat(args.date) if getattr(args, "date", None) else date.today()
    conn = get_connection()

    try:
        if args.command == "init":
            init_db(conn)
            print("Database ready. Members: M001 (student), M002 (faculty)")

        elif args.command == "import":
            print(f"Imported {import_books(conn, args.file)} books")

        elif args.command == "list":
            for b in list_books(conn):
                print(f"{b.isbn}  {b.title:<40} {b.author:<24} {b.status}")

        elif args.command == "checkout":
            due = checkout_book(conn, args.isbn, args.member, today)
            print(f"Checked out. Due {due.isoformat()}")

        elif args.command == "return":
            r = return_book(conn, args.isbn, today)
            print(f"Returned. {r.days_late} days late, fine ${r.fine:.2f}, "
                  f"balance ${r.new_balance:.2f}")
    except ValueError as err:
        print(f"Error: {err}")
    finally:
        conn.close()
