import sqlite3

class Book:
    """Class to represent a book"""
    def __init__(self, title, author, isbn=None, year=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year

    def __repr__(self):
        return f"Book(title={self.title}, author={self.author}, isbn={self.isbn}, year={self.year})"
    def convert_to_dict(self):
        """Convert book data to a dictionary"""
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "year": self.year
        }

def add_book_by_user_input():
    """Function to add basic book data from user input"""
    title = input("Enter book title: ")#!required
    author = input("Enter book author: ")#!required
    isbn = input("Enter book ISBN, if unknown leave blank: ")
    year = input("Enter book publication year, if unknown leave blank: ")     
    if not title or not author:
        print("Title and Author fields are required. Please try again.")
        return None  
    print(f"Book data entered successfully. Title: {title}, Author: {author}, ISBN: {isbn}, Year: {year}")
    """Convert book data to class and return it"""
    return Book(title=title, author=author, isbn=isbn if isbn else None, year=year if year else None)
  
def add_book_to_database(book):
    """Function to add book data to the database"""
    conn = sqlite3.connect('databases/books.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT,
            year TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO books (title, author, isbn, year)
        VALUES (?, ?, ?, ?)
    ''', (book.title, book.author, book.isbn, book.year))
    conn.commit()
    conn.close()
    print(f"Book '{book.title}' added to the database successfully.")
    
  #test

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

def remove_book_from_database(book_id):
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
  cursor.execute('SELECT * FROM books WHERE id=?', (book_id,))
  book = cursor.fetchone()
  if book:
        cursor.execute('''
            INSERT INTO removed_books (title, author, isbn, year)
            VALUES (?, ?, ?, ?)
        ''', (book[1], book[2], book[3], book[4]))
        cursor.execute('DELETE FROM books WHERE id=?', (book_id,))
        conn.commit()
        if is_books_table_empty()==True:
            # If the books table is empty, reset the ID count
            reset_books_table_id()
            print("Book removed successfully and books table is now empty, so ID count reset to 0.")
        else:
            print("Book removed successfully, but books table is not empty, so ID count remains unchanged.")

        print(f"Book with ID {book_id} removed from the database and added to removed_books history.")
  else:
        print(f"No book found with ID {book_id}.")
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
    else:
        print("Removed books:")
        for book in removed_books:
            print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, ISBN: {book[3]}, Year: {book[4]}")

def restore_removed_book(book_id):
    """Function to restore a removed book back to the main books table"""
    conn = sqlite3.connect('databases/books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM removed_books WHERE id=?', (book_id,))
    book = cursor.fetchone()
    if book:
        cursor.execute('''
            INSERT INTO books (title, author, isbn, year)
            VALUES (?, ?, ?, ?)
        ''', (book[1], book[2], book[3], book[4]))
        cursor.execute('DELETE FROM removed_books WHERE id=?', (book_id,))
        conn.commit()
        print(f"Book with ID {book_id} restored to the main books table.")
    
    else:
        print(f"No removed book found with ID {book_id}.")
    conn.close()

