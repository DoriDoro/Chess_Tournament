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

    def update_played_against(self, opponent):
        db = TinyDB(f'data/players/player.json')
        query = Query()
        db.update({'played_against': [opponent]}, query.player_id == self.player_id)

    def update_played_tournaments(self, tournament_name):
        db = TinyDB(f'data/players/player.json')
        query = Query()
        db.update({'played_tournaments': [tournament_name]}, query.played_tournaments == self.player_id)

    def create_pairs(self):
        # get the all players from database: player.json
        db = TinyDB(f'data/players/player.json')

        # get the number of players in the database to give it as param to the randint function
        random_player_id = db.all()[randint(1, len(db))]
        player1 = random_player_id
        player2 = random_player_id
        if player1 == player2:
            player2 = random_player_id

        create_pairs = [player1, player2]

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
