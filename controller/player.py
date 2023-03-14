import random

from tinydb import TinyDB, Query

from model.player import Player

Query = Query()


def get_player_id_from_list_of_players(name_of_tournament):
    database = TinyDB(f'data/tournaments/tournaments.json', indent=4)
    tournament_table = database.table("all_tournaments")
    # get the list_of_player from all_tournaments
    tournament = tournament_table.get(Query.name == name_of_tournament)
    get_list_of_players = tournament['list_of_players']

    return get_list_of_players


def get_name_of_player(player_ids):
    database = TinyDB(f'data/players/players.json', indent=4)
    player_table = database.table("all_players")

    player_id_1 = player_ids[0]
    player_id_2 = player_ids[1]

    player_1 = player_table.get(Query.player_id == player_id_1)
    p1_name = f"{player_1['first_name']} {player_1['last_name']}"

    player_2 = player_table.get(Query.player_id == player_id_2)
    p2_name = player_2['first_name'] + " " + player_2['last_name']

    return p1_name, p2_name



def add_player_id_to_list_of_players_controller(player_id, tournament_name):
    get_list_of_players = get_player_id_from_list_of_players(tournament_name)

    database = TinyDB(f'data/tournaments/tournaments.json', indent=4)
    tournament_table = database.table("all_tournaments")

    # update the list_of_player
    tournament_table.update({"list_of_players": get_list_of_players + [player_id]}, Query.name == tournament_name)


def create_player_controller(data_player):
    new_player = Player(data_player["player_id"], data_player["first_name"], data_player["last_name"],
                        data_player["birth_date"])
    data = {"player_id": new_player.player_id, "first_name": new_player.first_name,
            "last_name": new_player.last_name, "birth_date": new_player.birth_date,
            "rank": 0, "score": 0.0, "played_against": [], "played_tournaments": [data_player["name_of_tournament"]]}

    # add player_id to the tournament in tournaments.json inside list_of_players
    add_player_id_to_list_of_players_controller(new_player.player_id, data_player["name_of_tournament"])

    # create the database
    db = TinyDB(f'data/players/players.json', indent=4)
    # create a table and name the table
    all_players = db.table("all_players")
    all_players.insert(data)


def pair_players_controller(name_of_tournament):
    get_list_of_players = get_player_id_from_list_of_players(name_of_tournament)

    # k=2 choose two unique values
    paired_players = random.sample(get_list_of_players, k=2)

    # get player_id, first_name and last_name
    list_of_names = get_name_of_player(paired_players)

    return list_of_names


# add the player_id from pair_players_controller to players.json inside list played_against
#
# add Player to list_tours
