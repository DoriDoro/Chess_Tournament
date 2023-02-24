import json

from datetime import datetime


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

    def create_tournament(self):
        tournament_id = int(input("Please enter the ID of the Tournament: "))
        name = str(input("Enter the name of the Chess Tournament: "))
        city = str(input("Enter the location of the Chess Tournament: "))
        s_date = str(input("When does the Chess Tournament starts? (dd-mm-yyyy): "))
        start_date = datetime.strptime(s_date, "%d-%m-%Y")
        e_date = str(input("Please enter the end date of the Chess Tournament (dd-mm-yyyy): "))
        end_date = datetime.strptime(e_date, "%d-%m-%Y")
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
