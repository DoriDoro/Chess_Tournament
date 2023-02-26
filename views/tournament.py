from tinydb import TinyDB

from model.tournament import Tournament


def create_tournament(self):
    tournament_id = int(input("Please enter the ID of the Tournament: "))
    name = str(input("Enter the name of the Chess Tournament: "))
    city = str(input("Enter the location of the Chess Tournament: "))
    start_date = str(input("When does the Chess Tournament starts? (dd-mm-yyyy): "))
    end_date = str(input("Please enter the end date of the Chess Tournament (dd-mm-yyyy): "))
    list_tours = int(input("Question: "))
    rounds = int(input("How many rounds are possible for this Chess Tournament? "))
    comments = str(input("Do you have any comments concerning the Chess Tournament? "))
    print(f"You have just created this tournament: [name]: {name}, [city]: {city}, [start date]: "
          f"{start_date}, [end date]: {end_date}, [list_tours]: {list_tours}, [rounds]: {rounds}, "
          f"[comments]: {comments}")

    new_tournament = Tournament(tournament_id, name, city, start_date, end_date, list_tours, comments, rounds)
    data = {"tournament_id": new_tournament.tournament_id, "name": new_tournament.name,
            "city": new_tournament.city, "start_date": new_tournament.start_date,
            "end_date": new_tournament.end_date, "list_tours": new_tournament.list_tours,
            "rounds": new_tournament.rounds, "comments": new_tournament.comments,
            "list_of_players": [], "current_round": 0}

    db = TinyDB(f'data/tournaments/tournaments.json', indent=4)
    db.insert(data)
