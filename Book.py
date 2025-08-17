class Book:
    """Class to represent a book"""
    def __init__(self, title, author, isbn=None, year=None,
                genre=None, current_page=None, total_pages=None,
                start_date=None,end_date=None, rating=None, completion=None,status=None, updated=None):
        
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.genre = genre
        self.total_pages = total_pages
        self.current_page = current_page
        self.start_date = start_date
        self.end_date = end_date
        self.rating = rating
        self.completion = completion
        self.status = status
        self.updated= updated
        
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

# This class represents a book with attributes like title, author, ISBN, year, genre, total pages, start date, end date, rating, completion status, and current status.
# It includes a method to convert the book data into a dictionary format for easier handling and storage.
