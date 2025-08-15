# Program Flow

```
Start
  |
  v
Display Menu (Menu module)
  |
  v
User Choice:
  |-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|
  |                   |                   |                   |                   |                   |                   |
  v                   v                   v                   v                   v                   v
Add Book         View Books         Search Book         Update Book         Delete Book         Exit
  |                   |                   |                   |                   |                   |
  v                   v                   v                   v                   v                   v
Get Book Data   Show All Books      Show All Books      (Not implemented)  Show All Books      End
(book_database) (book_database)     (book_database)                        (book_database)
  |                   |                   |                                   |
  v                   v                   v                                   v
Add to DB        Display List        Display List                        Remove Book by ID
(book_database)  (book_database)     (book_database)                     (book_database)
  |                                                                       |
  v                                                                       v
If table empty, reset ID count (book_database)        <-------------------|
  |                                                                       |
  v                                                                       v
End                                                                  End
```