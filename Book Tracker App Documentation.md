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


```mermaid
graph TD
    A[Start] --> B[Initialize Database]
    B --> C[Display Menu]
    C --> D{User Selects Option}
    D -->|Add Book| E[Get User Input]
    D -->|View Books| F[Fetch All Books From Database]
    D -->|Remove Book| G[View Current Books And Get Book ID]
    D -->|View Removed Books| H[Fetch All Removed Books From Database]
    D -->|Restore Removed Book| I[Get Removed Book ID]
    D -->|Exit| J[End]

    E --> K[Create Book Object]
    K --> L[Add To Database]
    L --> M[Show Success Message]
    M --> C

    F --> N[Show Books List]
    N --> C

    G --> O[Move Book To Removed_Books Table]
    O --> P[Delete From Books Table]
    P --> Q{Is Books Table Empty?}
    Q -->|Yes| R[Reset ID Counter]
    Q -->|No| S[Show Success Message]
    S --> C
    R --> S

    H --> T[Show Removed Books List]
    T --> U{Restore Book?}
    U -->|Yes| I
    U -->|No| C

    I --> V[Move Book Back To Books Table]
    V --> W[Delete From Removed_Books Table]
    W --> X[Show Success Message]
    X --> C
```