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
