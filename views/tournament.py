from tinydb import TinyDB

from model.tournament import Tournament


def create_tournament():
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

    print("------------------------------------------------")
    print("** CHOOSE TOURNAMENT **", end="\n\n")
    for db in database:
        print(f"[ID]: {db['tournament_id']}  -  [Name]: {db['name']}")
    print()
    print("choose * to go back to menu", end="\n\n")


def choose_tournament():
    database = TinyDB(f'data/tournaments/tournaments.json')
    tournament_id_list = []
    for db in database:
        tournament_id_list.append(db['tournament_id'])

    while True:
        choice = int(input("Enter the Tournament_ID of your choice: "))

        if choice in tournament_id_list:
            print(f"You have chosen: {choice}", end="\n\n")
            break
        elif choice == "*":
            break
        else:
            print("Invalid choice. Please enter the Tournament_ID.", end="\n\n")
