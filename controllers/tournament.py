import json

from datetime import datetime
from tinydb import TinyDB, Query, where

from models.tournament import Tournament


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


def _get_player_table():
    db_player = TinyDB('data/players/players.json', indent=4)
    player_table = db_player.table("all_players")

    return player_table


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
        dict_score_tournament[f"pair{i + 1}"] = {
            "score": item[1],
            "names": item[2],
            "paired_players": item[0]
        }

    return dict_score_tournament


# TODO list_rounds "1" will be overwritten by adding new data
def add_player_score_to_list_rounds_controller(name_of_tournament, list_of_scores, current_round):
    tournament_table = _get_tournament_table()
    get_list_rounds = _get_tournament(name_of_tournament)["list_rounds"]

    pair_player_score = []
    # add time and date to pair_player_score

    player_score = []
    for key, value in list_of_scores.items():
        get_player = _get_player(key)
        player_score.append(get_player)
        score = get_player["score"]
        player_score.append({"score": score})

    for i in range(0, len(player_score), 2):
        sublist = player_score[i:i+2]
        pair_player_score.append(sublist)

    """
    print('player score ', player_score)
    print('pair player score', pair_player_score)
    player score  [{'player_id': 'DE75321', 'first_name': 'Dean', 'last_name': 'Trello', 'birth_date': '9-10-1987', 'rank': 0, 'score': 1, 'played_tournaments': {'name': 'The Golden Summer', 'played_against': ['WE15453']}}, {'score': 1}, {'player_id': 'YU60023', 'first_name': 'Danny', 'last_name': 'Blitz', 'birth_date': '5-9-2000', 'rank': 0, 'score': 0.5, 'played_tournaments': {'name': 'The Golden Summer', 'played_against': ['JI98563']}}, {'score': 0.5}, {'player_id': 'ER11102', 'first_name': 'Odin', 'last_name': 'Thor', 'birth_date': '11-11-2000', 'rank': 0, 'score': 0, 'played_tournaments': {'name': 'The Golden Summer', 'played_against': ['JJ10203']}}, {'score': 0}, {'player_id': 'JI98563', 'first_name': 'Helen', 'last_name': 'Stark', 'birth_date': '8-12-1999', 'rank': 0, 'score': 0.5, 'played_tournaments': {'name': 'The Golden Summer', 'played_against': ['YU60023']}}, {'score': 0.5}, {'player_id': 'WE15453', 'first_name': 'Bilan', 'last_name': 'Urk', 'birth_date': '9-8-1992', 'rank': 0, 'score': 0, 'played_tournaments': {'name': 'The Golden Summer', 'played_against': ['DE75321']}}, {'score': 0}, {'player_id': 'ER30003', 'first_name': 'Ragnar', 'last_name': 'Hammer', 'birth_date': '9-9-1999', 'rank': 0, 'score': 0, 'played_tournaments': {'name': 'The Golden Summer', 'played_against': ['HG11102']}}, {'score': 0}, {'player_id': 'JJ10203', 'first_name': 'Sarah', 'last_name': 'Dean', 'birth_date': '6-11-1998', 'rank': 0, 'score': 1, 'played_tournaments': {'name': 'The Golden Summer', 'played_against': ['ER11102']}}, {'score': 1}, {'player_id': 'HG11102', 'first_name': 'Odin', 'last_name': 'Sky', 'birth_date': '11-11-1999', 'rank': 0, 'score': 1, 'played_tournaments': {'name': 'The Golden Summer', 'played_against': ['ER30003']}}, {'score': 1}]
    pair player score [[{'player_id': 'DE75321', 'first_name': 'Dean', 'last_name': 'Trello', 'birth_date': '9-10-1987', 'rank': 0, 'score': 1, 'played_tournaments': {'name': 'The Golden Summer', 'played_against': ['WE15453']}}, {'score': 1}], [{'player_id': 'YU60023', 'first_name': 'Danny', 'last_name': 'Blitz', 'birth_date': '5-9-2000', 'rank': 0, 'score': 0.5, 'played_tournaments': {'name': 'The Golden Summer', 'played_against': ['JI98563']}}, {'score': 0.5}], [{'player_id': 'ER11102', 'first_name': 'Odin', 'last_name': 'Thor', 'birth_date': '11-11-2000', 'rank': 0, 'score': 0, 'played_tournaments': {'name': 'The Golden Summer', 'played_against': ['JJ10203']}}, {'score': 0}], [{'player_id': 'JI98563', 'first_name': 'Helen', 'last_name': 'Stark', 'birth_date': '8-12-1999', 'rank': 0, 'score': 0.5, 'played_tournaments': {'name': 'The Golden Summer', 'played_against': ['YU60023']}}, {'score': 0.5}], [{'player_id': 'WE15453', 'first_name': 'Bilan', 'last_name': 'Urk', 'birth_date': '9-8-1992', 'rank': 0, 'score': 0, 'played_tournaments': {'name': 'The Golden Summer', 'played_against': ['DE75321']}}, {'score': 0}], [{'player_id': 'ER30003', 'first_name': 'Ragnar', 'last_name': 'Hammer', 'birth_date': '9-9-1999', 'rank': 0, 'score': 0, 'played_tournaments': {'name': 'The Golden Summer', 'played_against': ['HG11102']}}, {'score': 0}], [{'player_id': 'JJ10203', 'first_name': 'Sarah', 'last_name': 'Dean', 'birth_date': '6-11-1998', 'rank': 0, 'score': 1, 'played_tournaments': {'name': 'The Golden Summer', 'played_against': ['ER11102']}}, {'score': 1}], [{'player_id': 'HG11102', 'first_name': 'Odin', 'last_name': 'Sky', 'birth_date': '11-11-1999', 'rank': 0, 'score': 1, 'played_tournaments': {'name': 'The Golden Summer', 'played_against': ['ER30003']}}, {'score': 1}]]
    """

    get_list_rounds[current_round + 1] = pair_player_score

    tournament_table.update({"list_rounds": get_list_rounds}, Query().name == name_of_tournament)

    """
    tournament_table = _get_tournament_table()

    end_date = datetime.now().isoformat()

    json_data = json.dumps(end_date)
    parsed_json = json.loads(json_data)

    tournament_table.update({"end_date": parsed_json}, Query().name == name_of_tournament)
    """


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
            data_player[player_id] = {"name": name, "score": score}

        data_tournaments_players[name_of_tournament] = {
            "start_date": start_date,
            "end_date": end_date,
            "list_of_players": list_of_players,
            "list_rounds": list_rounds,
            "player_data": data_player
        }

    return data_tournaments_players


def set_end_date_controller(name_of_tournament):
    tournament_table = _get_tournament_table()

    end_date = datetime.now().isoformat()

    json_data = json.dumps(end_date)
    parsed_json = json.loads(json_data)

    tournament_table.update({"end_date": parsed_json}, Query().name == name_of_tournament)
