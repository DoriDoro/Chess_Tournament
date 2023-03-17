from tinydb import TinyDB
from unidecode import unidecode


class Tournament:

    def __init__(
            self, name, city, start_date, end_date, comments, rounds=4):
        self.name = name
        self.city = city
        self.start_date = start_date
        self.end_date = end_date
        self.comments = comments
        self.rounds = rounds

        self.list_tours = []
        self.list_of_players = []  # add the players_id
        self.tournament_id = 0
        self.current_round = 0
