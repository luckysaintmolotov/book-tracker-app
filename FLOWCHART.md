# Program Flow

```
Start
  |
  v
User Choice:
  |-------------------------------|-------------------------------|-----------------------------|
  |                               |                               |                             |
  v                               v                               v                             v
Add Book by ISBN            Add Book Manually             View Books in DB             View Removed Books
  |                               |                               |                             |
  v                               v                               v                             v
Enter ISBN                  Get Book Data from User Input   Display Books              Display Removed Books
  |                               |                               |                             |
  v                               v                               v                             v
Get Book Data from API       Review Book Data                Remove Book?                Restore Book?
  |                               |                               |                             |
  v                               v                               v                             v
Is Data Valid?               Is Data Valid?                   Remove by ID                Restore by ID
  |                               |                               |                             |
  | Yes                          | Yes                          |                             |
  v                               v                               v                             v
Add Book to Database        Add Book to Database         Move Book to removed_books   Move Book to books
  |                               |                               |                             |
  v                               v                               v                             v
End                        End                        If books table empty:         End
                                                      Reset ID count
                                                      End
```