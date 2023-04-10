import json

from datetime import datetime
from tinydb import TinyDB, Query

from model.tournament import Tournament


# private functions:
def _get_tournament_table():
    db_tournament = TinyDB(f'data/tournaments/tournaments.json', indent=4)
    return db_tournament.table("all_tournaments")


def _get_tournament(name_of_tournament):
    db_tournament = TinyDB(f'data/tournaments/tournaments.json', indent=4)
    tournament_table = db_tournament.table("all_tournaments")

    return tournament_table.get(Query().name == name_of_tournament)


def _get_player(player_id):
    db_player = TinyDB('data/players/players.json', indent=4)
    player_table = db_player.table("all_players")

    return player_table.get(Query().player_id == player_id)


# option 2: create tournament:
def create_tournament_controller(data_tournament):
    new_tournament = Tournament(data_tournament["name"], data_tournament["city"],
                                data_tournament["comments"], data_tournament["rounds"])

    start_date = datetime.now().isoformat()

    data = {
        "tournament_id": data_tournament["tournament_id"],
        "name": new_tournament.name,
        "city": new_tournament.city,
        "start_date": start_date,
        "end_date": new_tournament.end_date,
        "rounds": new_tournament.rounds,
        "comments": new_tournament.comments,
        "list_rounds": {},
        "list_of_players": [],
        "current_round": 0
    }

    # usage of datetime, serialization necessary
    json_data = json.dumps(data)
    # insert() of TinyDB expects dictionary no json string, so parse data
    parsed_data = json.loads(json_data)

    db = TinyDB(f'data/tournaments/tournaments.json', indent=4)
    all_tournaments = db.table("all_tournaments")
    all_tournaments.insert(parsed_data)
    # close the db and save all changes made
    db.close()


# option 3: start a tournament:
def reorganize_list_score_tournament_controller(list_score_tournament):
    dict_score_tournament = {}

    for i, item in enumerate(list_score_tournament[:-1]):
        dict_score_tournament[f"pair{i+1}"] = {
            "score": item[1],
            "names": item[2],
            "paired_players": item[0]
        }

    return dict_score_tournament


def add_pair_to_list_rounds(name_of_tournament, data_list_rounds):
    tournament_table = _get_tournament_table()

    tournament_table.update({"list_rounds": data_list_rounds}, Query().name == name_of_tournament)


def get_current_round_controller(name_of_tournament):
    return _get_tournament(name_of_tournament)["current_round"]


def get_list_round_info_controller(name_of_tournament):
    list_rounds_rounds = _get_tournament(name_of_tournament)["list_rounds"]

    for rounds in list_rounds_rounds.items():
        last_round = rounds[0]
    return last_round


def get_results_tournaments_controller():
    tournaments = _get_tournament_table()

    data_tournaments_players = {}
    for tournament in tournaments:
        name_of_tournament = tournament["name"]
        start_date = tournament["start_date"]
        end_date = tournament["end_date"]
        list_of_players = tournament["list_of_players"]
        list_rounds = tournament["list_rounds"]

        data_player = {}
        for player_id in list_of_players:
            player_table = _get_player(player_id)
            name = f'{player_table["first_name"]} {player_table["last_name"]}'
            score = player_table["score"]
            data = {"player_id": player_id, "name": name, "score": score}
            data_player[player_id] = data

        data_tournament = {"name": name_of_tournament, "start_date": start_date, "end_date": end_date,
                           "list_of_players": list_of_players, "list_rounds": list_rounds, "player_data": data_player}
        data_tournaments_players[name_of_tournament] = data_tournament

    return data_tournaments_players


def set_end_date_controller(name_of_tournament):
    tournament_tabel = _get_tournament_table()

    end_date = datetime.now().isoformat()

    json_data = json.dumps(end_date)
    parsed_json = json.loads(json_data)

    tournament_tabel.update({"end_date": parsed_json}, Query().name == name_of_tournament)
