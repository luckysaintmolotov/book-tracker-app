import pandas as pd 
from tabulate import tabulate
book_genre_list = [
    # Fiction Genres
    "Literary Fiction",
    "Contemporary Fiction",
    "Historical Fiction",
    "Romance",
    "Mystery",
    "Thriller",
    "Crime",
    "Science Fiction",
    "Fantasy",
    "Horror",
    "Dystopian",
    "Adventure",
    "Young Adult (YA)",
    "New Adult",
    "Magical Realism",
    "Speculative Fiction",
    "Cyberpunk",
    "Post-Apocalyptic",

    # Non-Fiction Genres
    "Biography",
    "Autobiography",
    "Memoir",
    "History",
    "Science",
    "Philosophy",
    "Self-Help",
    "Travel",
    "True Crime",
    "Business",
    "Psychology",
    "Politics",
    "Nature",
    "Sociology",
    "Journalism",

    # Specialized Genres
    "Poetry",
    "Drama",
    "Short Stories",
    "Graphic Novel",
    "Comic Book",
    "Essay Collection",
    "Anthology",

    # Children's and Middle Grade
    "Picture Book",
    "Chapter Book",
    "Middle Grade",
    "Children's Fiction",
    "Educational",

    # Specialized Fiction
    "Western",
    "Satire",
    "Epistolary",
    "Gothic",
    "Experimental",
    "Alternative History"
]



class Genres:
    current_list = book_genre_list
    @staticmethod
    def get_user_genre():
        user_genre = input("Enter genre for the book : ").lower()
        if user_genre:
            return user_genre
        else:
            user_genre = None
            return  user_genre
    
    @staticmethod
    def select_from_list():
        df = pd.DataFrame(book_genre_list, columns=['Genres'])
        print(df)
        genre = int(input("Enter the index of the genre (1-50): "))
        #print(book_genre_list[genre-1])
        genre = book_genre_list[genre-1].lower()
        #print(genre)
        return genre
        

    