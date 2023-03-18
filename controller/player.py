import random

from tinydb import TinyDB, Query

from model.player import Player


# TODO: if already player inside the list_of_players in tournament do not add several the tournament,
#  perhaps not necessary


# option 1: create player:
def create_player_controller(data_player):
    new_player = Player(data_player["player_id"], data_player["first_name"], data_player["last_name"],
                        data_player["birth_date"])
    data = {"player_id": new_player.player_id, "first_name": new_player.first_name,
            "last_name": new_player.last_name, "birth_date": new_player.birth_date,
            "rank": 0, "score": 0.0,
            "played_tournaments": {"name": data_player["name_of_tournament"], "played_against": []}}

    # add player_id to the tournament in tournaments.json inside list_of_players:
    add_player_id_to_list_of_players_controller(new_player.player_id, data_player["name_of_tournament"])

    # create the database:
    db = TinyDB(f'data/players/players.json', indent=4)
    # create a table and name the table:
    all_players = db.table("all_players")
    all_players.insert(data)
    # close the db and save all changes made
    db.close()


def add_player_id_to_list_of_players_controller(player_id, tournament_name):
    get_list_of_players = get_player_id_from_list_of_players(tournament_name)

    database = TinyDB(f'data/tournaments/tournaments.json', indent=4)
    tournament_table = database.table("all_tournaments")

    # update the list_of_player list in tournaments.json:
    tournament_table.update({"list_of_players": get_list_of_players + [player_id]}, Query().name == tournament_name)
    database.close()


# option 1: create player and option 3: start a tournament:
def get_player_id_from_list_of_players(name_of_tournament):
    database = TinyDB(f'data/tournaments/tournaments.json', indent=4)
    tournament_table = database.table("all_tournaments")
    # get the list_of_player from tournaments.json, table: all_tournaments
    tournament = tournament_table.get(Query().name == name_of_tournament)

    get_list_of_players = tournament['list_of_players']

    return get_list_of_players


# option 3: start a tournament:

def _get_tournament_table():
    db_tournament = TinyDB(f'data/tournaments/tournaments.json', indent=4)
    return db_tournament.table("all_tournaments")


def _get_tournament(name_of_tournament):
    db_tournament = TinyDB(f'data/tournaments/tournaments.json', indent=4)
    tournament_table = db_tournament.table("all_tournaments")

    return tournament_table.get(Query().name == name_of_tournament)


def _get_player_table():
    db_player = TinyDB('data/players/players.json', indent=4)
    player_table = db_player.table("all_players")

    return player_table


def _get_player(player_id):
    db_player = TinyDB('data/players/players.json', indent=4)
    player_table = db_player.table("all_players")

    return player_table.get(Query().player_id == player_id)


def pair_players_controller(name_of_tournament):
    list_of_players = _get_tournament(name_of_tournament)["list_of_players"]  # get list of all players inside list_of_players
    current_round = _get_tournament(name_of_tournament)["current_round"]  # get the current_round
    rounds = _get_tournament(name_of_tournament)["rounds"]   # gets the rounds in total to play

    get_played_against = []
    for player_id in list_of_players:
        get_played_against_of_player = _get_player(player_id)['played_tournaments']['played_against']

        data = {"player_id": player_id, "played_against": get_played_against_of_player}
        get_played_against.append(data)

    if current_round <= rounds:
        get_verified_list_of_players = verify_number_of_player(name_of_tournament)
        # k=2 choose two unique values
        paired_players = random.sample(get_verified_list_of_players, k=2)
        # save paired_players in opponent
        add_player_id_to_played_against_controller(paired_players, name_of_tournament)
        # get player_id, first_name and last_name
        list_of_names = get_name_of_player(paired_players)

    # update rounds in tournament
    tournament_table = _get_tournament_table()
    tournament_table.update({"current_round": (current_round + 1)}, Query().name == name_of_tournament)

    # TODO: if current_round is more than rounds do something...
    return list_of_names


def verify_number_of_player(name_of_tournament):
    from views.player import add_additional_player_to_tournament_view

    get_verified_list_of_players_before = get_player_id_from_list_of_players(name_of_tournament)

    # check if 8 players are inside the list_of_players:
    number_of_players = len(get_verified_list_of_players_before)

    while number_of_players < 2:  # TODO 8
        add_additional_player_to_tournament_view(name_of_tournament)
        number_of_players += 1

    get_verified_list_of_players = get_player_id_from_list_of_players(name_of_tournament)

    return get_verified_list_of_players


def add_player_id_to_played_against_controller(player_ids, name_of_tournament):
    player_table = _get_player_table()

    get_played_against_player_1 = _get_player(player_ids[0])["played_tournaments"]["played_against"]
    get_played_against_player_1 = get_played_against_player_1 + [player_ids[1]]  # TODO adds duplicates to the list?

    get_played_against_player_2 = _get_player(player_ids[1])["played_tournaments"]["played_against"]
    get_played_against_player_2 = get_played_against_player_2 + [player_ids[0]]

    player_table.update({"played_tournaments": {"name": name_of_tournament,
                                                "played_against": [get_played_against_player_1]}},
                        Query().player_id == player_ids[0])
    player_table.update({'played_tournaments': {'name': name_of_tournament,
                                                'played_against': [get_played_against_player_2]}},
                        Query().player_id == player_ids[1])


def get_name_of_player(player_ids):
    database = TinyDB(f'data/players/players.json', indent=4)
    player_table = database.table("all_players")

    # create single player from player_ids list:
    player_id_1 = player_ids[0]
    player_id_2 = player_ids[1]

    # get name from database:
    player_1 = player_table.get(Query().player_id == player_id_1)
    p1_name = f"{player_1['first_name']} {player_1['last_name']}"

    player_2 = player_table.get(Query().player_id == player_id_2)
    p2_name = f"{player_2['first_name']} {player_2['last_name']}"

    return p1_name, p2_name
