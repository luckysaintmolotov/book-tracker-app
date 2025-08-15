import Menu

def menu_loop():
    """Main loop to display the menu and execute user choices"""
    menu_instance = Menu.Menu()
    
    while True:
        menu_instance.display_menu()
        choice = menu_instance.get_choice()
        menu_instance.execute_choice(choice)

menu_loop()
# This code initializes the menu for the Book Tracker App, displays it, and executes the user's choice.
# The Menu class handles the display and execution of menu options, allowing users to add books or view existing ones.  