class Loan:
    def __init__(self, member_id, checkout_date, due_date, renewals):
        self.member_id = member_id
        self.checkout_date = checkout_date
        self.due_date = due_date
        self.renewals = renewals


class Book:
    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.loan = None  # a Loan while the book is checked out

    def is_available(self):
        return self.loan is None
