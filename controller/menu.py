from views.menu import display_menu, get_choice
from views.player import create_player
from views.tournament import create_tournament


def handle_create_player():
    print("Create a Player selected.")
    create_player()


def handle_create_tournament():
    print("Create a Tournament selected.")
    create_tournament()


def handle_start_tournament():
    print("Start Tournament selected.")


def run_menu():
    while True:
        display_menu()
        choice = get_choice()

        if choice == "1":
            handle_create_player()
        elif choice == "2":
            handle_create_tournament()
        elif choice == "3":
            handle_start_tournament()
        elif choice == "4":
            print("Quitting program...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
