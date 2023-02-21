import json
import random
import string

from datetime import datetime


# models
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
        birthday = str(input(f"Enter the birth date of {first_name} {last_name} (yyyy-mm-dd): "))
        birth_date = datetime.strptime(birthday, "%Y-%m-%d")
        print(f"You have just created this player: [id]: {player_id}, [name]: {first_name} {last_name}, [birthday]: "
              f"{birth_date}")

        return {"player_id": player_id, "first_name": first_name, "last_name": last_name, "birth_date": birth_date}

    def save_player(self, list_of_players):
        pass

    # x = { 'first_name': 'John', 'last_name': 'Doe'}
    # y = json.dumps(x)
    # save player in JSON data file
    # save players in data/players/{name}.json

    def create_pairs(self):
        pass

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


class Tournament:

    def __init__(
            self, name, city, start_date, end_date, list_rounds, comments, rounds=4):
        self.name = name
        self.city = city
        self.start_date = start_date
        self.end_date = end_date
        self.list_rounds = list_rounds
        self.comments = comments
        self.rounds = rounds

        self.list_of_players = []  # add the players_id
        self.tournament_id = ""
        self.current_round = 0

    @staticmethod
    def create_tournament():
        tournament_id = int(input("Please enter the ID of the Tournament: "))
        name = str(input("Enter the name of the Chess Tournament: "))
        city = str(input("Enter the location of the Chess Tournament: "))
        s_date = str(input("When does the Chess Tournament starts? (yyyy-mm-dd): "))
        start_date = datetime.strptime(s_date, "%Y-%m-%d")
        e_date = str(input("Please enter the end date of the Chess Tournament (yyyy-mm-dd): "))
        end_date = datetime.strptime(e_date, "%Y-%m-%d")
        rounds = int(input("How many rounds are possible for this Chess Tournament? "))
        comments = str(input("Do you have any comments concerning the Chess Tournament? "))
        print(f"You have just created this tournament: [name]: {name}, [city]: {city}, [start date]: "
              f"{start_date}, [end date]: {end_date}, [rounds]: {rounds}, [comments]: {comments}")

        return {"tournament_id": tournament_id, "name": name, "city": city, "start_date": start_date,
                "end_date": end_date, "rounds": rounds, "comments": comments}

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
