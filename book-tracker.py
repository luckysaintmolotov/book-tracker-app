import Menu
import book_database
from Book_logs import update_log

def menu_loop():
    """Main loop to display the menu and execute user choices"""
    update_log("Book Tracker App started")    
    menu_instance = Menu.Menu()
    init_database = book_database.create_database_if_not_exists()
    if init_database:
        update_log("Database initialized successfully.")
    else:
        update_log("Database already exists or could not be initialized.")
    while True:
        menu_instance.display_menu()
        choice = menu_instance.get_choice()
        menu_instance.execute_choice(choice)

menu_loop()
# This code initializes the menu for the Book Tracker App, displays it, and executes the user's choice.
# The Menu class handles the display and execution of menu options, allowing users to add books or view existing ones.  