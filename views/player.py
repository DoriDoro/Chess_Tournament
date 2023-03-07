from tinydb import TinyDB

from model.player import Player


def create_player(name_of_tournament):
    print("------------------------------------------------")
    print("CREATE A PLAYER:", end="\n\n")

    player_id = str(input("Enter the ID of the player (example: AB12345): "))
    first_name = str(input("Enter the first name of the player: "))
    last_name = str(input(f"Enter {first_name}'s last name: "))
    birth_date = str(input(f"Enter the birth date of {first_name} {last_name} (dd-mm-yyyy): "))
    print()
    print(f"You have just created this player: ")
    print(f"  [id]: {player_id}")
    print(f"  [name]: {first_name} {last_name}")
    print(f"  [birthday]: {birth_date}", end="\n\n")

    new_player = Player(player_id, first_name, last_name, birth_date)
    data = {"player_id": new_player.player_id, "first_name": new_player.first_name,
            "last_name": new_player.last_name, "birth_date": new_player.birth_date,
            "rank": 0, "score": 0.0, "played_against": [], "played_tournaments": [name_of_tournament]}

    # create the database
    # save players in data/players/{player_id}.json
    db = TinyDB(f'data/tournaments/{name_of_tournament}.json', indent=4)
    db.insert(data)
