from tinydb import TinyDB

from model.player import Player


def create_player():
    player_id = str(input("Enter the ID of the player (example: AB12345): "))
    first_name = str(input("Enter the first name of the player: "))
    last_name = str(input(f"Enter {first_name}'s last name: "))
    birth_date = str(input(f"Enter the birth date of {first_name} {last_name} (dd-mm-yyyy): "))
    print(f"You have just created this player: [id]: {player_id}, [name]: {first_name} {last_name}, [birthday]: "
          f"{birth_date}")

    new_player = Player(player_id, first_name, last_name, birth_date)
    data = {"player_id": new_player.player_id, "first_name": new_player.first_name,
            "last_name": new_player.last_name, "birth_date": new_player.birth_date,
            "rank": 0, "score": 0.0, "played_against": [], "played_tournaments": []}

    # create the database
    # save players in data/players/{player_id}.json
    # db = TinyDB(f'data/players/{player_id}.json', indent=4)
    db = TinyDB(f'data/players/player.json', indent=4)
    db.insert(data)

