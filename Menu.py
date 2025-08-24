from book_database import BooksTable as db
class Menu:
    """Class to manage the menu options for the Book Tracker App"""
    def __init__(self):
        self.options = {
            1: "Add Book",
            2: "View Books",
            3: "Search Book",
            4: "Update Book",
            5: "Delete Book",
            6: "View Removed Books",
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
            book = db.Create.create_book_item()
            if book:
                db.Create.add_to(book)
        elif choice == 2:
            db.View.all_books()
        elif choice == 3:
            db.View.by_author(input("Author: ").lower())
        elif choice == 4:   
            print("Update functionality not implemented yet.")
        elif choice == 5:
            db.View.all_books()
            db.Remove.remove_by_id(input("Input Unique ID of the book shown above: "))
        elif choice == 6:
            #to be implemented
            #book_database.view_removed_books()
            pass
        elif choice == 0:
            print("Exiting the Book Tracker App. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please try again.")
# This class manages the menu options for the Book Tracker App, allowing users to add, view, search, update, delete books, and view removed books.
# It provides methods to display the menu, get user input, and execute the selected option.