from random import randint

from tinydb import TinyDB, Query
from unidecode import unidecode


class Player:

    def __init__(self, player_id, first_name, last_name, birth_date):
        self.player_id = player_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date

        self.rank = 0
        self.score = 0.0
        self.played_against = []  # add the player_id
        self.played_tournaments = []  # add the tournament_id

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def create_player():
        player_id = str(input("Enter the ID of the player (example: AB12345): "))
        first_name = str(input("Enter the first name of the player: "))
        last_name = str(input(f"Enter {first_name}'s last name: "))
        birth_date = str(input(f"Enter the birth date of {first_name} {last_name} (dd-mm-yyyy): "))
        print(f"You have just created this player: [id]: {player_id}, [name]: {first_name} {last_name}, [birthday]: "
              f"{birth_date}")

        new_player = Player(player_id, first_name, last_name, birth_date)
        data = {"player_id": new_player.player_id, "first_name": new_player.first_name,
                "last_name": new_player.last_name, "birth_date": new_player.birth_date}

        # create the database
        # save players in data/players/{player_id}.json
        # db = TinyDB(f'data/players/{player_id}.json', indent=4)
        db = TinyDB(f'data/players/player.json', indent=4)
        db.insert(data)

        # save the number of players in the database
        players_in_db = 1
        players_in_db += 1
        return players_in_db

    @staticmethod
    def create_pairs(players_in_db):
        # get the all players from database: player.json
        db = TinyDB(f'data/players/player.json')

        # get the number of players in the database to give it as param to the randint function
        player1 = db.all()[randint(1, 100)]
        print(player1)

        # create pairs to play against
        # check if they played already against each other
        # update played_against, add the players_id
        # update played_tournaments, add the tournament_id

    def check_opponents(self):
        # check if the player played already against the opponent
        pass

    def calculate_score(self):
        pass

    def calculate_rank(self):
        pass
