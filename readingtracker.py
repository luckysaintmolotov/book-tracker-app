import sqlite3
from datetime import datetime
import book_database

book_id = 1

def update_reading_progress(book_id):
    "Function for tracking reading progress of a book."
    book = book_database.get_book_by_id(book_id)
    if book:
        if book.updated is None:
            print(f"Tracking progress for book: {book.title} by {book.author}")

            #requires data validation
            book.start_date = input("Enter start date (YYYY-MM-DD): ")
            book.end_date = input("Enter end date (YYYY-MM-DD) if no end date, press Enter: ")
            book.current_page = int(input("Enter current page number: "))
            book.total_pages = int(input("Enter total pages in the book: "))
            book.completion = (book.current_page / book.total_pages) * 100
            book.updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Reading progress updated:")
            print(f"Title: {book.title}, Author: {book.author}, Current Page: {book.current_page}, Total Pages: {book.total_pages}, Completion: {book.completion:.2f}%")
        else:
            print(f"Reading progress for book: {book.title} by {book.author} has already been updated{book.updated}.")
            print(f"Start Date: {book.start_date}, End Date: {book.end_date}, Current Page: {book.current_page}, Total Pages: {book.total_pages}, Completion: {book.completion:.2f}%")
    else:
        print(f"No book found with ID {book_id}.")  
