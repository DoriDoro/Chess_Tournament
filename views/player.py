from tinydb import TinyDB

from controller.player import create_player_controller


# option 1: create player:
def add_player_to_tournament_view(tournament_id_name_list):

    while True:
        choice = input(" Enter the Tournament_ID of your choice: ")
        print()

        # check if the user choice "*" to quit:
        if choice == "*":
            break

        # check if choice is an int and display the Tournament name or display error:
        choice = int(choice)

        for tournament_id, name in tournament_id_name_list:
            if choice == tournament_id:
                print(f" You have chosen: {name}", end="\n\n")
                # TODO if already 8 players in tournament, do not add any player, choose other tournament
                number_of_player = 8
                while number_of_player > 0:
                    create_player_view(name)
                    number_of_player -= 1
                    if number_of_player == 0:
                        return

        print(" Invalid choice. Please enter the Tournament_ID.", end="\n\n")


# option 1: create player and option 3: start a tournament:
def create_player_view(name_of_tournament):
    print("------------------------------------------------")
    print(" ** CREATE A PLAYER **", end="\n\n")

    player_id = str(input(" Player ID (example: AB12345): "))
    first_name = str(input(" First name: "))
    last_name = str(input(f" Enter {first_name}'s last name: "))
    birth_date = str(input(f" Enter the birth date of {first_name} {last_name} (dd-mm-yyyy): "))
    print()
    print(f" You have just created this player: ")
    print(f"   [id]: {player_id}")
    print(f"   [name]: {first_name} {last_name}")
    print(f"   [birthday]: {birth_date}", end="\n\n")

    data_player = {"name_of_tournament": name_of_tournament, "player_id": player_id,
                   "first_name": first_name, "last_name": last_name, "birth_date": birth_date}

    create_player_controller(data_player)


# option 3: start tournament:
def add_additional_player_to_tournament_view(name_of_tournament):
    print("   There are not enough players available for this tournament.", end="\n\n")
    create_player_view(name_of_tournament)
