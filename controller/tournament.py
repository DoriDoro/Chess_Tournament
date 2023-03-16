from tinydb import TinyDB

from model.tournament import Tournament


def create_tournament_controller(data_tournament):
    new_tournament = Tournament(data_tournament["name"], data_tournament["city"],
                                data_tournament["start_date"], data_tournament["end_date"],
                                data_tournament["comments"], data_tournament["rounds"])
    data = {"tournament_id": data_tournament["tournament_id"], "name": new_tournament.name,
            "city": new_tournament.city, "start_date": new_tournament.start_date,
            "end_date": new_tournament.end_date, "rounds": new_tournament.rounds, "comments": new_tournament.comments,
            "list_tours": [], "list_of_players": [], "current_round": 0}

    db = TinyDB(f'data/tournaments/tournaments.json', indent=4)
    all_tournaments = db.table("all_tournaments")
    all_tournaments.insert(data)
    # close the db and save all changes made
    db.close()
