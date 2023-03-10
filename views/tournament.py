from tinydb import TinyDB

from controller.tournament import create_tournament_controller


def create_tournament_view():
    print("------------------------------------------------")
    print("CREATE A TOURNAMENT:", end="\n\n")

    tournament_id = int(input("Tournament ID (example: 1234): "))
    name = str(input("Name of tournament: "))
    city = str(input("Location of tournament: "))
    start_date = str(input("Start date (dd-mm-yyyy): "))
    end_date = str(input("End date (dd-mm-yyyy): "))
    rounds = int(input("Number of rounds? "))
    comments = str(input("Any comments? "))
    print()
    print(f"You have just created this tournament:")
    print(f"  [Tournament ID]: {tournament_id}")
    print(f"  [name]: {name}")
    print(f"  [city]: {city}")
    print(f"  [start date]: {start_date} and [end date]: {end_date}")
    print(f"  [rounds]: {rounds}")
    print(f"  [comments]: {comments}", end="\n\n")

    data_tournament = {"tournament_id": tournament_id, "name": name, "city": city, "start_date": start_date,
                       "end_date": end_date, "rounds": rounds, "comments": comments}

    create_tournament_controller(data_tournament)


def get_tournaments_view():
    database = TinyDB(f'data/tournaments/tournaments.json')
    tournament_table = database.table("all_tournaments")

    tournament_id_name_list = []

    for db in tournament_table:
        tournament_id_name_list.append([db['tournament_id'], db['name']])

    return tournament_id_name_list


def display_tournaments_view(tournament_id_name_list):
    print("------------------------------------------------")
    print("** CHOOSE TOURNAMENT **", end="\n\n")
    for db in tournament_id_name_list:
        print(f"[ID]: {db[0]}  -  [Name]: {db[1]}")
    print()
    print("choose * to go back to menu", end="\n\n")


def choose_tournament_view(tournament_id_name_list, player_id_list):
    print("------------------------------------------------")
    print("START A TOURNAMENT:", end="\n\n")

    while True:
        choice = input("Enter the Tournament_ID of your choice: ")
        print()

        if choice == "*":
            break

        choice = int(choice)

        for tournament_id, name in tournament_id_name_list:
            if choice == tournament_id:
                print(f"You have chosen: {name}", end="\n\n")

        # get the first pair

        print("Invalid choice. Please enter the Tournament_ID.", end="\n\n")
