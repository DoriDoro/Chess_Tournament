from tinydb import TinyDB
from unidecode import unidecode


class Tournament:

    def __init__(
            self, name, city, start_date, end_date, list_tours, comments, rounds=4):
        self.name = name
        self.city = city
        self.start_date = start_date
        self.end_date = end_date
        self.list_tours = list_tours
        self.comments = comments
        self.rounds = rounds

        self.list_of_players = []  # add the players_id
        self.tournament_id = ""
        self.current_round = 0



    def save_tournament(self):
        pass
    # take the dict from create_tournament and save it
    # save in json in data/tournaments/{name}.json

    def get_tournaments(self, name_of_tournament):
        pass
    # get a tournament by tournament_id from json file
    # update the list_of_players of tournament, add the players_id

    def calculate_current_round(self):
        pass
# update current_round, add 1
