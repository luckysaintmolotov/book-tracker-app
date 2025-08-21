import sqlite3
import uuid,re,random
from datetime import datetime
from Book import Book
from Book_logs import update_log
"""Database management module for the Book Tracker App"""
db_name = 'databases/books.db'
def create_database_if_not_exists():
    """Create the database and tables if they do not exist"""
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "books" (
        "id" TEXT,
        "author" TEXT,
        "title" TEXT,
        "ISBN" TEXT UNIQUE,
        "year" TEXT,
        "creation_date" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY("id")
    )""")
    # Create the books table with unique ISBN and primary key on id

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "genres" (
        "genre_id" TEXT,
        "genre_name" TEXT UNIQUE,
        PRIMARY KEY("genre_id"))""")
    # Create the genres table with unique genre names and primary key on genre_id

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "book_genres" (
        "book_id" TEXT NOT NULL,
        "genre_id" TEXT NOT NULL,
        PRIMARY KEY("book_id", "genre_id"),
        FOREIGN KEY ("book_id") REFERENCES "books"("id")
        ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY ("genre_id") REFERENCES "genres"("genre_id")
        ON UPDATE CASCADE ON DELETE CASCADE
    )""")
    # Create the book_genres table to link books and genres with foreign keys

    cursor.execute("""CREATE TABLE IF NOT EXISTS "reading_progress" (
        "id" TEXT,
        "book_id" TEXT NOT NULL,
        "total_pages" INTEGER,
        "current_pages" INTEGER,
        "start_date" DATE,
        "end_date" DATE,
        "percentage" REAL,
        "status" TEXT,
        "last_updated" TIMESTAMP,
        PRIMARY KEY("id"),
        FOREIGN KEY ("book_id") REFERENCES "books"("id")
        ON UPDATE CASCADE ON DELETE CASCADE
    )""")
    # Create the reading_progress table to track reading progress with foreign key to books

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "book_status" (
        "status_id" TEXT,
        "progress_id" TEXT NOT NULL,
        "status" TEXT,
        "timestamp" TIMESTAMP,
        PRIMARY KEY("status_id"),
        FOREIGN KEY ("progress_id") REFERENCES "reading_progress"("id")
        ON UPDATE CASCADE ON DELETE CASCADE
    )""")
    # Create the book_status table to track status updates with foreign key to reading_progress

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "reviews_and_info" (
        "review_id" TEXT,
        "book_id" TEXT,
        "description" TEXT,
        "review" TEXT,
        "notes" TEXT,
        "timestamp" TIMESTAMP,
        PRIMARY KEY("review_id"),
        FOREIGN KEY ("book_id") REFERENCES "books"("id")
        ON UPDATE CASCADE ON DELETE CASCADE
    )""")
    # Create the reviews_and_info table to store reviews and additional information with foreign key to books

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "review_tags" (
        "review_id" TEXT NOT NULL,
        "tag" TEXT NOT NULL,
        PRIMARY KEY("review_id", "tag"),
        FOREIGN KEY ("review_id") REFERENCES "reviews_and_info"("review_id")
        ON UPDATE CASCADE ON DELETE CASCADE
    )""")
    # Create the review_tags table to link reviews and tags with foreign key to reviews_and_info

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "removed_books" (
        "id" TEXT,
        "book_id" TEXT NOT NULL,
        "timestamp" TIMESTAMP,
        PRIMARY KEY("id"),
        FOREIGN KEY ("book_id") REFERENCES "books"("id")
        ON UPDATE CASCADE ON DELETE CASCADE
    )""")
    # Create the removed_books table to keep track of removed books with foreign key to books

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "restored_books" (
        "id" TEXT,
        "removed_id" TEXT NOT NULL,
        "book_id" TEXT NOT NULL,
        "timestamp" TIMESTAMP,
        PRIMARY KEY("id"),
        FOREIGN KEY ("removed_id") REFERENCES "removed_books"("id")
        ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY ("book_id") REFERENCES "books"("id")
        ON UPDATE CASCADE ON DELETE CASCADE
    )""")
    conn.commit()
    conn.close()
    # Create the restored_books table to keep track of restored books with foreign keys to removed_books and books
class BooksTable(Book):
    """Class to handle all functions dedicated to the books table"""

    @staticmethod
    def create_book_item():
        """Function to create a book item with basic data"""
        def generate_book_id(author, title, year, isbn):
            """Function that generates a UUID"""
            if len(year) < 4  or year is None:
                year = 1900
                isbn = "000000000000000000000"
            # Input sanitization
            author = author.strip()
            title = title.strip()
            year = year 
            isbn = isbn.strip()
            
            author = re.sub(r'[^a-zA-Z0-9 ]', '', author)
            title = re.sub(r'[^a-zA-Z0-9 ]', '', title)
            isbn = re.sub(r'[^0-9X]', '', isbn)  # ISBN can contain digits and 'X' for ISBN-10

            # Generate a unique ID for the book
            return str(uuid.uuid5(uuid.NAMESPACE_X500, f"{author}{title}{year}{isbn}"))
            
        title = input("Enter book title: ").lower().strip()#!required
        author = input("Enter book author: ").lower().strip()#!required
        isbn = input("Enter book ISBN, if unknown leave blank: ")
        year = input("Enter book publication year, if unknown leave blank: ")
        id = generate_book_id(author,title,year,isbn)
        if not title or not author:
            print("Title and Author fields are required. Please try again.")
            update_log("Book creation failed due to missing required fields.")
            return None  
    
        print(f"Book created successfully. ID:{id} Title: {title}, Author: {author}, ISBN: {isbn}, Year: {year} on {datetime.now().strftime('%d-%m-%Y')}")
        """Convert book data to class and return it"""
        update_log("Book created successfully.")
        return Book(id=id,title=title, author=author, isbn=isbn if isbn else None, year=year if year else None, )
    
    @staticmethod
    def add_to(book):
        """Function to add book item to the database"""
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE title=? AND author=?', (book.title, book.author))
        existing_book = cursor.fetchone()
        # Check if the book already exists in the database
        if existing_book is not None:
            print(f"Book '{book.title}' by {book.author} already exists in the database.")
            conn.close()
            return
        # If the book does not exist, insert it into the database
        cursor.execute('''
            INSERT INTO books (id, title, author, isbn, year, creation_date)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (book.id, book.title, book.author, book.isbn, book.year))
        conn.commit()
        conn.close()
        print(f"Book '{book.title}' with ID: {book.id}added to the database successfully.")
        update_log(f"Book '{book.title}' added to the database successfully.")


    class View:
        @staticmethod
        def all_books():  
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute("""
                        SELECT * FROM books             
                        """)
            books = cursor.fetchall()
            conn.close()
            book_list = {}
            for book in books:
                book_list[book[0]] = {
                        "author": book[1],
                        "title": book[2],
                        "isbn": book[3],
                        "year": book[4]
                    }
            if not book_list:
                    print("No books found in the database.")

            else:
                print(f"Books in the database: {len(book_list)}")
            book_count = 0
            for book_id, book_data in book_list.items():
                book_count+=1
                print(f"""
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Book #{book_count}

Title: {book_data['title']}, Author: {book_data['author']}, 
ISBN: {book_data['isbn']}, Year: {book_data['year']}
ID: {book_id},
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -""") 

        @staticmethod
        def by_author(author):
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute("""
                        SELECT * FROM books 
                        WHERE author LIKE ?""",('%' + author + '%',))
            books = cursor.fetchall()
            conn.close()
            book_list = {}
            for book in books:
                book_list[book[0]] = {
                        "author": book[1],
                        "title": book[2],
                        "isbn": book[3],
                        "year": book[4]
                    }
            if not book_list:
                    print(f"No books by {author} found in the database.")

            else:
                print(f"Books by {author} in the database: {len(book_list)}")
            book_count = 0
            for book_id, book_data in book_list.items():
                book_count+=1
                
                print(f"""
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Book #{book_count}

Title: {book_data['title']}, 
ISBN: {book_data['isbn']}, Year: {book_data['year']}
ID: {book_id},
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -""") 
            
        @staticmethod
        def by_author_and_title(author,title):
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute("""
                        SELECT * FROM books 
                        WHERE author LIKE ? AND title LIKE ?""",('%' + author + '%', '%' + title + '%'))
            books = cursor.fetchall()
            conn.close()
            book_list = {}
            for book in books:
                book_list[book[0]] = {
                        "author": book[1],
                        "title": book[2],
                        "isbn": book[3],
                        "year": book[4]
                    }
            if not book_list:
                    print(f"No book {title} by {author} found in the database.")

            else:
                print(f"{title} by {author} in the database: {len(book_list)}")
            book_count = 0
            for book_id, book_data in book_list.items():
                book_count+=1
                
                print(f"""
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Book #{book_count}

ISBN: {book_data['isbn']}, Year: {book_data['year']}
ID: {book_id},
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -""") 
        
        #further functions will be implemented

    class Remove:
        """Function to handle all database removal"""
        #to be implemented
        pass
    
    class Restore:
        """Function to handle database restoration"""
        #to be implemented 
        pass
    
def view_books_in_database():
    """Function to view all books in the database"""
    conn = sqlite3.connect('databases/books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    book_list = {}
    for book in books:
        book_list[book[0]] = {
            "title": book[1],
            "author": book[2],
            "isbn": book[3],
            "year": book[4]
        }
    if not book_list:
        print("No books found in the database.")
        
    else:
        print("Books in the database:")
        for book_id, book_data in book_list.items():
            print(f"ID: {book_id}, Title: {book_data['title']}, Author: {book_data['author']}, ISBN: {book_data['isbn']}, Year: {book_data['year']}") 

def remove_book_from_database(id):
    """Function to remove a book from the database by ID, and makes a history of the removed book in a separate table"""
    conn = sqlite3.connect('databases/books.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS removed_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT,
            year TEXT
        )
    ''')
    cursor.execute('SELECT * FROM books WHERE id=?', (id,))
    book = cursor.fetchone()
    if book:
        cursor.execute('''
            INSERT INTO removed_books (title, author, isbn, year)
            VALUES (?, ?, ?, ?)
        ''', (book[1], book[2], book[3], book[4]))
        cursor.execute('DELETE FROM books WHERE id=?', (id,))
        conn.commit()
        if is_books_table_empty()==True:
            # If the books table is empty, reset the ID count
            reset_books_table_id()
            update_log(f"Book with ID {id} removed and books table reset.")
        else:
            update_log("Book removed successfully, but books table is not empty, so ID count remains unchanged.")

        print(f"Book with ID {id} removed from the database and added to removed_books history.")
        
    else:
        print(f"No book found with ID {id}.")
    update_log(f"No book found with ID {id}.")
    conn.close() 

def is_books_table_empty():
    """Check if the books table is empty."""
    conn = sqlite3.connect('databases/books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM books')
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

def reset_books_table_id():
    """Delete all rows and reset AUTOINCREMENT ID for books table."""
    conn = sqlite3.connect('databases/books.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="books"')
    conn.commit()
    conn.close()
    print("Books table cleared and ID count reset.")

def view_removed_books():
    """Function to view all removed books in the database"""
    conn = sqlite3.connect('databases/books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM removed_books')
    removed_books = cursor.fetchall()
    conn.close()
    if not removed_books:
        print("No removed books found in the database.")
        update_log("No removed books found in the database.")
    else:
        print("Removed books:")
        for book in removed_books:
            print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, ISBN: {book[3]}, Year: {book[4]}")
    
    # Restore functionality to restore a removed book back to the main books table
    if removed_books:
        print("You can restore a removed book back to the main books table.")
        restore_choice = input("Do you want to restore a removed book? (yes/no): ")
        if restore_choice.lower() == 'yes':
            restore_removed_book(id=int(input("Enter the ID of the book you want to restore: ")))
            update_log("Removed book restored successfully.")
        else:
            print("No book restored.")
        update_log("Removed books viewed successfully.")
    else:
        print("No removed books available to restore.")    

def restore_removed_book(id):
    """Function to restore a removed book back to the main books table"""
    conn = sqlite3.connect('databases/books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM removed_books WHERE id=?', (id,))
    book = cursor.fetchone()
    if book:
        cursor.execute('''
            INSERT INTO books (title, author, isbn, year)
            VALUES (?, ?, ?, ?)
        ''', (book[1], book[2], book[3], book[4]))
        cursor.execute('DELETE FROM removed_books WHERE id=?', (id,))
        conn.commit()
        print(f"Book with ID {id} restored to the main books table.")
    
    else:
        print(f"No removed book found with ID {id}.")
    conn.close()

def get_book_id(author,title):
    """Function to get book ID from database by author and title"""
    conn = sqlite3.connect('databases/books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM books WHERE author=? AND title=?', (author, title))
    book_id = cursor.fetchone()
    conn.close()
    if book_id:
        return book_id[0]
    else:
        print(f"No book found with author '{author}' and title '{title}'.")
        return None

def get_book_by_id(id):
    """Function to get book details by ID"""
    conn = sqlite3.connect('databases/books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id=?', (id,))
    book = cursor.fetchone()
    conn.close()
    if book:
        return Book(id=book[0],title=book[1], author=book[2], isbn=book[3], year=book[4])
    else:
        print(f"No book found with ID {id}.")
        return None    
    
# This module provides functions to manage the book database, including creating the database, adding books, viewing books, removing books, and restoring removed books.
# It uses SQLite for database management and includes logging functionality to track operations.
# The database is structured with two tables: one for current books and another for removed books,
# allowing for easy management and retrieval of book data.

"""Testing the book_database module"""
if __name__ == "__main__":
    create_database_if_not_exists()
    # Uncomment the following lines to test the functions
    book = BooksTable.create_book_item()
    BooksTable.add_to(book)
    BooksTable.View.all_books()
    BooksTable.View.by_author('Welsh')
    BooksTable.View.by_author_and_title('Irvine Welsh','Porno')
    