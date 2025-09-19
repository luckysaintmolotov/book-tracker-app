import requests
api_url = "https://openlibrary.org/search.json?"    #Open Library's search api

class Book:
    """Class to represent a book"""
    def __init__(self,id,title, author, isbn=None, year=None,
                genre=None, current_page=None, total_pages=None,
                start_date=None,end_date=None, rating=None, completion=None,status=None, time_stamp=None):
        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.genre = genre
        
        self.total_pages = total_pages
        self.current_page = current_page
        self.start_date = start_date
        self.end_date = end_date
        self.completion = completion
        
        self.rating = rating
        self.status = status
        self.time_stamp= time_stamp
        
    def __repr__(self):
        return f"Book(title={self.title}, author={self.author}, isbn={self.isbn}, year={self.year})"

    @staticmethod  
    def get_book_info_ISBN(isbn):
        """Function to search for book's author and title from the given urls"""

        results = requests.get(f"{api_url}isbn={isbn}").json()
        author = (results['docs'][0]["author_name"])
        title = (results['docs'][0]["title"])
        book = {
            "author": author,
            "title": title,
    }   
        return book
    @staticmethod  
    def get_ISBN_from_info(author,title,publish_year,language):
            """Function to get missing ISBN from given author and title"""
            results = requests.get(f"{api_url}title={title}&author={author}&publish_year={publish_year}&language={language}&fields=isbn&limit=1").json()
            ISBN = results['docs'][0]
            if results['docs'] and 'isbn' in results['docs'][0]:
                ISBN = results['docs'][0]['isbn'][0]  # Get only the first ISBN
            else:
                ISBN = None
            return ISBN

# This class represents a book with attributes like title, author, ISBN, year, genre, total pages, start date, end date, rating, completion status, and current status.
# It includes a method to convert the book data into a dictionary format for easier handling and storage.
