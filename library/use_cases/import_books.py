def import_books(conn, file_path):
    """Add every book in the supplier's CSV file to the catalog."""
    count = 0
    with open(file_path) as f:
        next(f)  # skip header
        for line in f:
            # Columns: [0] = ISBN, [1] = Title, [2] = Author
            data = line.strip().split(",")
            conn.execute(
                "INSERT OR REPLACE INTO books (isbn, title, author) VALUES (?, ?, ?)",
                (data[0], data[1], data[2]),
            )
            count += 1
    conn.commit()
    return count
