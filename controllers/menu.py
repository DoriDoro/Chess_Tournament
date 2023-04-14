from views.menu import display_menu, get_choice, quitting_program
from views.player import (
    add_player_to_tournament_view,
)
from views.tournament import (
    choose_tournament_view,
    create_tournament_view,
    display_tournaments_view,
    get_tournaments_view,
)


def handle_create_player():
    tournament_id_name_list = get_tournaments_view()

    display_tournaments_view(tournament_id_name_list)
    add_player_to_tournament_view(tournament_id_name_list)


def handle_create_tournament():
    create_tournament_view()


def handle_start_tournament():
    tournament_id_name_list = get_tournaments_view()

    display_tournaments_view(tournament_id_name_list)
    choose_tournament_view(tournament_id_name_list)


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
            quitting_program()
            break
        else:
            print("  Invalid choice. Please enter a number between 1 and 4.")
