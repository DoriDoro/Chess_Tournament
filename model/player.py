
class Player:

    def __init__(self, player_id, first_name, last_name, birth_date):
        self.player_id = player_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date

        self.rank = 0
        self.score = 0
        self.played_tournaments = {}

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
