import book_database
class Menu:
    """Class to manage the menu options for the Book Tracker App"""
    def __init__(self):
        self.options = {
            1: "Add Book",
            2: "View Books",
            3: "Search Book",
            4: "Update Book",
            5: "Delete Book",
            0: "Exit"
        }

    def display_menu(self):
        """Display the menu options"""
        print("\nBook Tracker Menu:")
        for key in self.options:
            print(f"{key}. {self.options[key]}")
            
            
    def get_choice(self):
        """Get the user's choice from the menu"""
        while True:
            try:
                choice = int(input("Select an option: "))
                if choice in self.options:
                    return choice
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
                
    def execute_choice(self, choice):
        """Execute the chosen menu option"""
        if choice == 1:
            book = book_database.add_book_by_user_input()
            if book:
                book_database.add_book_to_database(book)
        elif choice == 2:
            book_database.view_books_in_database()
        elif choice == 3:
            book_database.view_books_in_database()
        elif choice == 4:   
            print("Update functionality not implemented yet.")
        elif choice == 5:
            book_database.view_books_in_database()
            book_database.remove_book_from_database(book_id=int(input("Enter the book ID to delete: ")))
        elif choice == 0:
            print("Exiting the Book Tracker App. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please try again.")