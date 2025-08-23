import sqlite3
from datetime import datetime
import book_database
from Book import Book


def create_table_if_not_exists():
    """Function to create the reading tracking table if it does not exist"""
    conn = sqlite3.connect('databases/books.db')
    cursor = conn.cursor()
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS reading_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT NOT NULL,
        title TEXT NOT NULL,
        start_date TEXT,
        end_date TEXT,
        days INTEGER,
        current_page INTEGER,
        total_pages INTEGER,
        pages_per_day INTEGER,
        completion REAL,
        updated TEXT,
        book_id INTEGER,
        FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE
    )
    ''')
    conn.commit()
    conn.close()

def add_reading_progress(book):
    """Function to add reading progress for a book"""
    conn = sqlite3.connect('databases/books.db')
    cursor = conn.cursor()
    cursor.execute(''' 
    INSERT INTO reading_progress (author, title, start_date, end_date, days, current_page, total_pages, pages_per_day, completion, updated, book_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (book.author, book.title, book.start_date, book.end_date, 0, book.current_page, book.total_pages, 0, book.completion, datetime.now(), book.id))
    conn.commit()
    conn.close()

def update_reading_progress(id):
    "Function for tracking reading progress of a book."
    book = book_database.get_book_by_id(id)
    if book:
        if book.time_stamp is None:
            print(f"Tracking progress for book: {book.title} by {book.author}")

            #requires data validation
            book.start_date = input("Enter start date (YYYY-MM-DD): ")
            book.end_date = input("Enter end date (YYYY-MM-DD) if no end date, press Enter: ")
            if book.end_date == "":
                book.end_date = book.start_date
            else:
                print(f"End date set to {book.end_date} for book: {book.title} by {book.author}")
            book.current_page = int(input("Enter current page number: "))
            book.total_pages = int(input("Enter total pages in the book: "))
            
            book.completion = (book.current_page / book.total_pages) * 100
            
            book.time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            add_reading_progress(book)
            print("Reading progress updated:")
            print(f"Title: {book.title}, Author: {book.author}, Current Page: {book.current_page}, Total Pages: {book.total_pages}, Completion: {book.completion:.2f}%")
        
        else:
            print(f"Reading progress for book: {book.title} by {book.author} has already been updated{book.time_stamp}.")
            print(f"Start Date: {book.start_date}, End Date: {book.end_date}, Current Page: {book.current_page}, Total Pages: {book.total_pages}, Completion: {book.completion:.2f}%")

    else:
        print(f"No book found with ID {id}.")  


create_table_if_not_exists()
update_reading_progress(1)





