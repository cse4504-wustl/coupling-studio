# Coupling Studio

The purpose of this studio is to practice:
* identifying high coupling in code and 
* refactoring code to reduce coupling

The code in this studio contains coupling scenarios that are similar to the [5 scenarios presented in class](https://github.com/cse4504-wustl/coupling).

## Overview

`library/` is a small command-line app for a university library. Members borrow books, and late returns are fined. Students borrow for 14 days and faculty for 60. It follows the Clean Architecture layout:

| Folder | Role |
|---|---|
| `cli/` | command-line interface |
| `use_cases/` | the operations the app supports: import, checkout, return, list |
| `entities/` | business objects: `Book`, `Loan`, `Member`, `Account`, `FinePolicy` |
| `dto/` | data passed out of use cases: `BookSummary`, `ReturnReceipt` |
| `persistence/` | the SQLite database |

There is also a `config.py` with library-wide settings.

Run it:
```bash
cd library
python3 main.py init
python3 main.py import data/books.csv
python3 main.py list
python3 main.py checkout --isbn 9780132350884 --member M001 --date 2026-10-01
python3 main.py return --isbn 9780132350884 --date 2026-10-25
```
`M001` is a student and `M002` is a faculty member. Then read the code; it's short.

To start over at any point, delete `library.db` and run `init` and `import` again.

---

## Find the high coupling scenarios in the app

Each of the five scenarios from Part 1 appears in the library app. Find each one and fill in your answers below.

**1. Configuration**
- Where (file : function):
- What change would break it:

**2. Database access**
- Where (file : function):
- What change would break it:

**3. Chained function calls**
- Where (file : function):
- What change would break it:

**4. External data format**
- Where (file : function):
- What change would break it:

**5. Direct property assignment**
- Where (file : function):
- What change would break it:

Two experiments to back up your answers. Predict the result first, then run:

**A. The supplier's new file.** This year's file adds a Year column:
```bash
python3 main.py import data/books_2027.csv
python3 main.py list
```
Look at the author column. Did the import fail? Should it have?

**B. A faculty member, then a student.** Both check out a book on the same day, in the same program run:
```bash
python3 -c "
from datetime import date
from persistence.database import get_connection
from use_cases.checkout_book import checkout_book
conn = get_connection()
print('Faculty due:', checkout_book(conn, '9780201616224', 'M002', date(2026, 10, 15)))
print('Student due:', checkout_book(conn, '9780596007126', 'M001', date(2026, 10, 15)))"
```
Students get 14 days. What did the student get, and why?

---

## Fix the problems

Refactor the app to remove each problem. A suggested order, smallest change first:

**Scenario 5: Direct property assignment.** Only `Book` should create a `Loan`. Give `Book` a method that checks it out; `checkout_book` tells the book what happened instead of building its internals.

**Scenario 3: Chained function calls.** `return_book` should not navigate from member to account to fine policy. Tell the member to charge a late fee, and let the entities work out the amount.

**Scenario 1: Configuration.** No code should change `config` while the program runs. The loan period depends on the type of member. Decide which entity should own that rule.

**Scenario 4: External data format.** `use_cases/` should not open files or know column positions. Add a DTO for an imported book, and have `import_books` receive a list of them. Move the CSV parsing out of `use_cases/` and read columns by name, so `books_2027.csv` imports correctly. Be ready to explain where you put the parsing and why.

**Scenario 2: Database access.** `use_cases/` should contain no SQL and should not import `sqlite3`. In `use_cases/`, define the interface the use cases need (a `Protocol`). Implement it in `persistence/`, and have `cli/` create it and pass it in.

### Done when

The commands from Part 2 still work, experiments A and B now give the right answers (update experiment B's snippet to match your new `checkout_book` parameters), and these searches (run inside `library/`) print nothing:
```bash
grep -rnE --include="*.py" "sqlite3|SELECT|INSERT|UPDATE" use_cases/
grep -rnE --include="*.py" "config\." use_cases/ entities/
grep -rnE --include="*.py" "get_account\(\)\.|\.loan = " use_cases/ cli/
```