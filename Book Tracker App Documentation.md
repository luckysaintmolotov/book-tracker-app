# Book Tracker App Documentation

---

## Database Schema

### books

| Column | Type    | Constraints         | Description                |
|--------|---------|---------------------|----------------------------|
| id     | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique book ID             |
| title  | TEXT    | NOT NULL            | Book title                 |
| author | TEXT    | NOT NULL            | Book author                |
| isbn   | TEXT    |                     | Book ISBN (optional)       |
| year   | TEXT    |                     | Publication year (optional)|

### removed_books

| Column | Type    | Constraints         | Description                |
|--------|---------|---------------------|----------------------------|
| id     | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique removed book ID      |
| title  | TEXT    | NOT NULL            | Book title                 |
| author | TEXT    | NOT NULL            | Book author                |
| isbn   | TEXT    |                     | Book ISBN (optional)       |
| year   | TEXT    |                     | Publication year (optional)|

---

## Program Flowchart

```
Start
  |
  v
User chooses action:
  |-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|
  v                   v                   v                   v                   v                   v
Add Book         View Books         Remove Book         View Removed Books   Restore Removed Book   Exit
  |                   |                   |                   |                   |                   |
  v                   v                   v                   v                   v                   v
Get user input   Fetch all books    Get book ID         Fetch all removed    Get removed book ID   End
(title, author,  from books table  from user           books from           from user
isbn, year)      and display       |                   removed_books table  |
  |                   |             |                   and display         |
  v                   v             |                   |                   |
Create Book      Show books         v                   Show removed        Restore book:
object           list              Remove book:         books list          - Move to books table
  |                   |             - Move to           |                   - Remove from removed_books
  v                   |             removed_books       |                   |
Add to books     |                 - Delete from        |                   |
table            |                 books table          |                   |
  |              |                 - If books table     |                   |
  v              |                 empty, reset ID      |                   |
Show success     |                 count                |                   |
message          |                 |                    |                   |
  |              |                 v                    |                   |
  v              |             Show success             |                   |
End              |             message                  |                   |
                 |                 |                    |                   |
                 v                 v                    v                   v
             End              End                  End                 End
```