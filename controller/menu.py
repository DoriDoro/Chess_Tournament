from tinydb import TinyDB

from views.menu import display_menu, get_choice
from views.tournament import add_player_to_tournament, create_tournament, display_tournaments, get_tournaments

tournament_id_name_list = get_tournaments()


def handle_create_player():
    # get all tournaments
    display_tournaments(tournament_id_name_list)
    # choose a tournament
    add_player_to_tournament(tournament_id_name_list)
    # create player
    # save player inside the tournament


def handle_create_tournament():
    print("------------------------------------------------")
    print("CREATE A TOURNAMENT:", end="\n\n")
    create_tournament()


def handle_start_tournament():
    # choose a tournament
    # add player (check already added player and add more)
    # pair the players for the first round
    print("------------------------------------------------")
    print("START TOURNAMENT:", end="\n\n")
    # get all tournaments
    display_tournaments(tournament_id_name_list)


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
