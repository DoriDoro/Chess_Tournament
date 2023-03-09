from tinydb import TinyDB

from model.player import Player


def create_player_controller(data_player):
    new_player = Player(data_player["player_id"], data_player["first_name"], data_player["last_name"],
                        data_player["birth_date"])
    data = {"player_id": new_player.player_id, "first_name": new_player.first_name,
            "last_name": new_player.last_name, "birth_date": new_player.birth_date,
            "rank": 0, "score": 0.0, "played_against": [], "played_tournaments": [data_player["name_of_tournament"]]}

    # add player_id to the tournament in tournaments.json inside list_of_players

    # create the database
    # save players in data/players/{player_id}.json
    db = TinyDB(f'data/players/players.json', indent=4)
    # create a table and name the table
    all_players = db.table("all_players")
    all_players.insert(data)
