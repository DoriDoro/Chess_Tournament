from tinydb import TinyDB, Query

from model.player import Player

Tournament = Query()


def add_player_id_to_list_of_players_controller(player_id, tournament_name):
    database = TinyDB(f'data/tournaments/tournaments.json', indent=4)
    tournament_table = database.table("all_tournaments")

    # get the list_of_player from all_tournaments
    tournament = tournament_table.get(Tournament.name == tournament_name)
    get_list_of_players = tournament['list_of_players']

    # update the list_of_player
    tournament_table.update({"list_of_players": get_list_of_players + [player_id]}, Tournament.name == tournament_name)


def create_player_controller(data_player):
    new_player = Player(data_player["player_id"], data_player["first_name"], data_player["last_name"],
                        data_player["birth_date"])
    data = {"player_id": new_player.player_id, "first_name": new_player.first_name,
            "last_name": new_player.last_name, "birth_date": new_player.birth_date,
            "rank": 0, "score": 0.0, "played_against": [], "played_tournaments": [data_player["name_of_tournament"]]}

    # add player_id to the tournament in tournaments.json inside list_of_players
    add_player_id_to_list_of_players_controller(new_player.player_id, data_player["name_of_tournament"])

    # create the database
    # save players in data/players/{player_id}.json
    db = TinyDB(f'data/players/players.json', indent=4)
    # create a table and name the table
    all_players = db.table("all_players")
    all_players.insert(data)
