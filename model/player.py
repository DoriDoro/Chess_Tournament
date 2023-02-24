from datetime import datetime


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

    def create_player(self):
        player_id = str(input("Enter the ID of the player (example: AB12345): "))
        first_name = str(input("Enter the first name of the player: "))
        last_name = str(input(f"Enter {first_name}'s last name: "))
        birthday = str(input(f"Enter the birth date of {first_name} {last_name} (dd-mm-yyyy): "))
        birth_date = datetime.strptime(birthday, "%d-%m-%Y")
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
