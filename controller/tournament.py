from tinydb import TinyDB

from model.tournament import Tournament


# option 2: create tournament:
def create_tournament_controller(data_tournament):
    new_tournament = Tournament(data_tournament["name"], data_tournament["city"],
                                data_tournament["start_date"], data_tournament["end_date"],
                                data_tournament["comments"], data_tournament["rounds"])
    data = {"tournament_id": data_tournament["tournament_id"], "name": new_tournament.name,
            "city": new_tournament.city, "start_date": new_tournament.start_date,
            "end_date": new_tournament.end_date, "rounds": new_tournament.rounds, "comments": new_tournament.comments,
            "list_rounds": {}, "list_of_players": [], "current_round": 0}

    db = TinyDB(f'data/tournaments/tournaments.json', indent=4)
    all_tournaments = db.table("all_tournaments")
    all_tournaments.insert(data)
    # close the db and save all changes made
    db.close()


def reorganize_list_score_tournament_controller(list_score_tournament, list_of_scores):
    dict_score_tournament = {}

    for i, item in enumerate(list_score_tournament[:-1]):
        dict_score_tournament[f"pair{i+1}"] = {
            "score": item[1],
            "names": item[2],
            "paired_players": item[0]
        }

    return dict_score_tournament


def display_results_controller(paired_players, name_of_tournament):
    pass
    # single pair: names
    # result of the match

def end_results_controller():
    pass
