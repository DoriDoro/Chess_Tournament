from views.menu import display_menu, get_choice
from views.player import create_player
from views.tournament import create_tournament


def handle_create_player():
    print("------------------------------------------------")
    print("CREATE A PLAYER:", end="\n\n")
    create_player()


def handle_create_tournament():
    print("------------------------------------------------")
    print("CREATE A TOURNAMENT:", end="\n\n")
    create_tournament()


def handle_start_tournament():
    print("------------------------------------------------")
    print("START TOURNAMENT:", end="\n\n")


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
            print("------------------------------------------------")
            print("Quitting program...", end="\n\n")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
