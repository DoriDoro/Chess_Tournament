

class Tournament:

    def __init__(
            self, name, city, comments, rounds=4):
        self.name = name
        self.city = city
        self.comments = comments
        self.rounds = rounds

        self.start_date = "start"
        self.end_date = "ongoing"
        self.list_rounds = {}
        self.list_of_players = []
        self.tournament_id = 0
        self.current_round = 0
