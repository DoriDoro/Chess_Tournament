from tinydb import TinyDB

from model.tournament import Tournament
from views.player import create_player


def create_tournament():
    print("------------------------------------------------")
    print("CREATE A TOURNAMENT:", end="\n\n")

    tournament_id = int(input("Please enter the ID of the Tournament (example: 1234): "))
    name = str(input("Enter the name of the Chess Tournament: "))
    city = str(input("Enter the location of the Chess Tournament: "))
    start_date = str(input("When does the Chess Tournament starts? (dd-mm-yyyy): "))
    end_date = str(input("Please enter the end date of the Chess Tournament (dd-mm-yyyy): "))
    rounds = int(input("How many rounds are possible for this Chess Tournament? "))
    comments = str(input("Do you have any comments concerning the Chess Tournament? "))
    print()
    print(f"You have just created this tournament:")
    print(f"  [Tournament ID]: {tournament_id}")
    print(f"  [name]: {name}")
    print(f"  [city]: {city}")
    print(f"  [start date]: {start_date} and [end date]: {end_date}")
    print(f"  [rounds]: {rounds}")
    print(f"  [comments]: {comments}", end="\n\n")

    new_tournament = Tournament(name, city, start_date, end_date, comments, rounds)
    data = {"tournament_id": tournament_id, "name": new_tournament.name,
            "city": new_tournament.city, "start_date": new_tournament.start_date,
            "end_date": new_tournament.end_date, "rounds": new_tournament.rounds, "comments": new_tournament.comments,
            "list_tours": [], "list_of_players": [], "current_round": 0}

    db = TinyDB(f'data/tournaments/tournaments.json', indent=4)
    db.insert(data)


def get_tournaments():
    database = TinyDB(f'data/tournaments/tournaments.json')
    tournament_id_name_list = []
    for db in database:
        tournament_id_name_list.append([db['tournament_id'], db['name']])

    return tournament_id_name_list


def get_players(tournament_name):
    database = TinyDB(f'data/tournaments/{tournament_name}.json')
    player_id_list = []
    for db in database:
        player_id_list.append(db['player_id'])

    return player_id_list


def display_tournaments(tournament_id_name_list):
    print("------------------------------------------------")
    print("** CHOOSE TOURNAMENT **", end="\n\n")
    for db in tournament_id_name_list:
        print(f"[ID]: {db[0]}  -  [Name]: {db[1]}")
    print()
    print("choose * to go back to menu", end="\n\n")


def add_player_to_tournament(tournament_id_name_list):

    while True:
        choice = input("Enter the Tournament_ID of your choice: ")
        print()

        # check if the user choice "*" to quit:
        if choice == "*":
            break

        # check if choice is an int and display the Tournament name or display error:
        choice = int(choice)

        for tournament_id, name in tournament_id_name_list:
            if choice == tournament_id:
                print(f"You have chosen: {name}", end="\n\n")

                # create while loop to add x players in one tournament
                number_of_player = 8
                while number_of_player > 0:
                    create_player(name)
                    number_of_player -= 1
                    if number_of_player == 0:
                        return

        print("Invalid choice. Please enter the Tournament_ID.", end="\n\n")


def choose_tournament(tournament_id_name_list, player_id_list):
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
