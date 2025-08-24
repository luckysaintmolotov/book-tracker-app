import sqlite3
import uuid
import pandas as pd
from datetime import datetime
from Book import Book
from genres import Genres
from Book_logs import update_log
"""Database management module for the Book Tracker App"""
DB_NAME = 'databases/books.db'

def create_database_if_not_exists():
    """Create the database and tables if they do not exist"""
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "books" (
        "id" TEXT,
        "author" TEXT,
        "title" TEXT,
        "ISBN" TEXT ,
        "year" TEXT,
        "creation_date" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY("id")
    )""")
    # Create the books table with ISBN and primary key on id


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "removed_books" (
        "id" TEXT,
        "author" TEXT,
        "title" TEXT,
        "ISBN" TEXT ,
        "year" TEXT,
        "creation_date" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY("id")
    )""")
    # Create the removed_books table to keep track of removed books with foreign key to books

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "restored_books" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "book_id" TEXT NOT NULL,
    "author" TEXT,
    "title" TEXT,
    "timestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("book_id") REFERENCES "books"("id")
    ON DELETE CASCADE
    )""")
    # Create the restored books table to keep track of restored books with foreign key to books

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "genres"  (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "genre" TEXT)""")
    # Create the basic_book_genres table to keep track of genres 
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "book_genres"(
    "genre_id" INTEGER, 
    "book_id" TEXT,
    FOREIGN KEY ("genre_id") REFERENCES "genres"("id"),
    FOREIGN KEY ("book_id") REFERENCES  "books"("id")  
    ON DELETE CASCADE
    )""")
    # Create the book_genres table to keep track of books and their assigned genres
    
    
    conn.commit()
    conn.close()
def create_database_backup():
    conn=sqlite3.connect(DB_NAME)
    b_conn = sqlite3.connect(f"{DB_NAME}.bk-{datetime.now()}")
    
    conn.backup(b_conn)
    b_conn.close()
    conn.close()
    
class BooksTable(Book):
    """Class to contain all functions dedicated to the books table"""

    
    class Create:
        """Class to handle the creation functions"""    
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
            conn = sqlite3.connect(DB_NAME)
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
        """Class to handle all functions that pertain to viewing the database tables"""
        @staticmethod
        def all_books():  
            conn = sqlite3.connect(DB_NAME)
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

            for book_id, book_data in book_list.items():
                print(f"""Title: {book_data['title']}, Author: {book_data['author']},   | | |   ID {book_id}""")

        @staticmethod
        def by_author(author):
            conn = sqlite3.connect(DB_NAME)
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
            for book_id, book_data in book_list.items():
                print(f"""Title: {book_data['title']}, Author: {book_data['author']},   | | |   ID {book_id}""")
            
        @staticmethod
        def by_author_and_title(author,title):
            conn = sqlite3.connect(DB_NAME)
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
            for book_id, book_data in book_list.items():
                print(f"""Title: {book_data['title']}, Author: {book_data['author']},   | | |   ID {book_id}""")

        @staticmethod
        def by_ISBN(isbn):
            pass
        
        @staticmethod
        def by_genre(genre):
            pass
        
        @staticmethod
        def by_random():
            pass
        #further functions will be implemented
    class Remove:
        """Function to handle all database removal"""

        @staticmethod
        def remove_by_id(book_id):
            conn = sqlite3.connect(DB_NAME)
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            
            # Move to removed_books first
            cursor.execute('''
            INSERT INTO removed_books (id, author, title, isbn, year, creation_date)
            SELECT id, author, title, isbn, year, creation_date 
            FROM books WHERE id = ?
            ''', (book_id,))
            
            # Then delete from books 
            cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
            
            # Commit the transaction
            conn.commit()
            print(f"Book with ID {book_id} successfully removed.")
    class Restore:
        """Function to handle database restoration"""
        
        @staticmethod
        def by_author(author):
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            
            # Find and verify the books
            cursor.execute("""SELECT * FROM removed_books WHERE author LIKE ?""", ('%' + author + '%',))
            books = cursor.fetchall()
            print(f'Total books by {author.lower()} found: {len(books)}')
            
            book_list = {}
            for book in books:
                book_list[book[0]]={
                    "id": book[0],
                    "author": book[1],
                    "title": book[2],
                    "isbn": book[3],
                    "year": book[4]
                }
            
            if not book_list:
                print("No books found")
            else:
                print(f"Books that can be recovered: {len(book_list)}")
                for book_id, book_data in book_list.items():
                    print(f"""Title: {book_data['title']}, Author: {book_data['author']},   | | |   ID {book_id}""")
                
                if input("Do you want to restore? (yes/no): ").lower() == "yes":
                    title = input("To restore, please input the title: ").strip().lower()  # Strip whitespace and convert to lowercase
                    
                    # Check if the title exists in the book_list
                    found = False
                    for book_id, book_data in book_list.items():
                        print(f"Comparing with stored title: '{book_data['title']}'")  # Debugging output
                        
                        if book_data['title'] == title:
                            found = True
                            # Restore the book to the books table
                            cursor.execute('''
                                INSERT INTO books (id, title, author, isbn, year)
                                VALUES (?, ?, ?, ?, ?)''', 
                                (book_data["id"],book_data['title'], book_data['author'], book_data['isbn'], book_data['year'])
                            )

                            #add to the recovered table
                            cursor.execute('''
                                INSERT INTO restored_books (book_id, author, title)
                                VALUES (?, ?, ?)''', 
                                (book_data["id"],book_data['title'], book_data['author'])
                            )
                            print(f"Restored: Title: {book_data['title']}, Author: {book_data['author']}, ID: {book_id}")
                            
                            cursor.execute("DELETE FROM removed_books WHERE id = ?", (book_id,))
                            break
                    
                    if not found:
                        print("No matching title found for restoration.")
            result = cursor.fetchone()
            conn.commit() 
            conn.close()
            
                                
        @staticmethod
        def by_title_and_or_author(title,author):
            pass
        
        @staticmethod
        def by_id(id):
            pass
        
        @staticmethod
        def all():
            pass

class GenresTable():
    
    @staticmethod
    def load_default_if_not():
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(""" SELECT genre FROM genres """,)
        result = c.fetchone()
        if result is None:
            for genre in Genres.current_list:
                c.execute("""
                INSERT INTO genres (genre)
                VALUES (?)""",(genre,))
            conn.commit()
            conn.close()
        else:
            print("Predefined genres already loaded")
    class Create:
        @staticmethod
        def create_new_genre_item():
            def add_custom_genre_to(genre):
                    conn = sqlite3.connect(DB_NAME)
                    c = conn.cursor()
                    c.execute("""
                    SELECT * FROM genres 
                    WHERE genre LIKE ?""",('%' + genre.lower() + '%',))
                    list_of_existing_genres = c.fetchall()
                    if not list_of_existing_genres:
                        c.execute("""INSERT INTO genres (genre) VALUES (?)""",(genre.lower(),))
                        conn.commit()
                        return genre
                        #print(f"Added new genre: {genre}")
                    else:
                        df = pd.DataFrame(list_of_existing_genres,columns=["ID","Genre"]).to_string(index=False)
                        if len(df) >= 1:
                            genre = list_of_existing_genres[1-1]
                            return genre
                        else:
                            print(df)
                            index = int(input("Genre exists, please enter the index: "))
                            genre = list_of_existing_genres[index-1]
                            return genre
            
            if input("Select from list? (Yes): ").lower() == "yes":
                genre = Genres.select_from_list()
                return genre
            else:
                genre = Genres.get_user_genre()
                add_custom_genre_to(genre)
                return genre
        
        @staticmethod
        def add_to(book,genre):

            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("""
            INSERT INTO book_genres (genre_id, book_id)
            VALUES (?, ?)""",(genre,book.id))
            conn.commit()
            conn.close()
        
    class View:
        pass
    
    
# This module provides functions to manage the book database, including creating the database, adding books, viewing books, removing books, and restoring removed books.
# It uses SQLite for database management and includes logging functionality to track operations.
# The database is structured with two tables: one for current books and another for removed books,
# allowing for easy management and retrieval of book data.

"""Testing the book_database module"""
if __name__ == "__main__":
    create_database_if_not_exists()
    #GenresTable.insert_defaults()
    # Uncomment the following lines to test the functions
    book = BooksTable.Create.create_book_item()
    genre = GenresTable.Create.create_new_genre_item()
    
    #BooksTable.add_to(book)
    #BooksTable.View.all_books()
    #BooksTable.View.by_author('Welsh')
    #BooksTable.View.by_author_and_title('Irvine Welsh','Porno')
    #id=('6dbcfb2b-8098-532b-9c31-0d7d12589886')
    #BooksTable.Remove.remove_by_id(id)
    #BooksTable.Restore.by_author("Irvine Welsh")
    GenresTable.Create.add_to(book,genre)