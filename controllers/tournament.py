import json

from datetime import datetime
from tinydb import TinyDB, Query

from models.tournament import Tournament


class TournamentControllers:

    def __init__(self):
        pass

    # private functions:
    def _get_tournament_table(self):
        db_tournament = TinyDB("data/tournaments/tournaments.json", indent=4)
        return db_tournament.table("all_tournaments")

    def _get_tournament(self, name_of_tournament):
        db_tournament = TinyDB("data/tournaments/tournaments.json", indent=4)
        tournament_table = db_tournament.table("all_tournaments")

        return tournament_table.get(Query().name == name_of_tournament)

    def _get_player(self, player_id):
        db_player = TinyDB("data/players/players.json", indent=4)
        player_table = db_player.table("all_players")

        return player_table.get(Query().player_id == player_id)

    def _serialize_date(self):
        start_date = datetime.now().strftime("%Y-%m-%d %H:%M")

        json_data = json.dumps(start_date)
        return json.loads(json_data)

    # option 2: create tournament:
    def create_tournament_controller(self, data_tournament):
        new_tournament = Tournament(
            data_tournament["name"],
            data_tournament["city"],
            data_tournament["comments"],
            data_tournament["rounds"],
        )

        start_date = self._serialize_date()

        data = {
            "tournament_id": data_tournament["tournament_id"],
            "name": new_tournament.name,
            "city": new_tournament.city,
            "start_date": start_date,
            "end_date": new_tournament.end_date,
            "rounds": new_tournament.rounds,
            "comments": new_tournament.comments,
            "list_rounds": {},
            "list_of_players": [],
            "current_round": 0,
        }

        db = TinyDB("data/tournaments/tournaments.json", indent=4)
        all_tournaments = db.table("all_tournaments")
        all_tournaments.insert(data)
        # close the db and save all changes made
        db.close()

    # option 3: start a tournament:
    def add_player_score_to_list_rounds_controller(
        self, name_of_tournament, list_of_scores
    ):
        tournament_table = self._get_tournament_table()
        get_list_rounds = self._get_tournament(name_of_tournament)["list_rounds"]
        current_round = self._get_tournament(name_of_tournament)["current_round"]
        round_start_date = self._serialize_date()
        round_end_date = "ongoing"

        pair_player_score = [round_start_date, round_end_date]

        player_score = []
        for key, value in list_of_scores.items():
            get_player = self._get_player(key)
            player_score.append(get_player)
            score = get_player["score"]
            player_score.append({"score": score})

        for i in range(0, len(player_score), 2):
            sublist = player_score[i: i + 2]
            pair_player_score.append(sublist)

        round_end_date = self._serialize_date()
        pair_player_score.pop(1)
        pair_player_score.insert(1, round_end_date)

        get_list_rounds[current_round] = pair_player_score

        tournament_table.update(
            {"list_rounds": get_list_rounds}, Query().name == name_of_tournament
        )

    def get_current_round_controller(self, name_of_tournament):
        return self._get_tournament(name_of_tournament)["current_round"]

    def get_list_round_info_controller(self, name_of_tournament):
        list_rounds = self._get_tournament(name_of_tournament)["list_rounds"]

        for rounds in list_rounds.items():
            last_round = rounds[0]

        return last_round

    def get_results_tournaments_controller(self):
        tournaments = self._get_tournament_table()

        data_tournaments_players = {}
        for tournament in tournaments:
            name_of_tournament = tournament["name"]
            tournament_id = tournament["tournament_id"]
            start_date = tournament["start_date"]
            end_date = tournament["end_date"]
            list_of_players = tournament["list_of_players"]
            list_rounds = tournament["list_rounds"]

            data_list_rounds = {}
            for round_number, values in list_rounds.items():
                data_list_rounds_player = {}
                for data in values[2:]:
                    player_id = data[0]["player_id"]
                    fname = data[0]["first_name"]
                    lname = data[0]["last_name"]
                    name_of_player = f"{fname} {lname}"
                    data_list_rounds_player[player_id] = {"name": name_of_player}
                    data_list_rounds[round_number] = data_list_rounds_player

            data_player = {}
            for player_id in list_of_players:
                player_table = self._get_player(player_id)
                name = f'{player_table["first_name"]} {player_table["last_name"]}'
                data_player[player_id] = {"name": name}

            data_tournaments_players[name_of_tournament] = {
                "tournament_id": tournament_id,
                "start_date": start_date,
                "end_date": end_date,
                "list_rounds": data_list_rounds,
                "player_data": data_player,
            }

        return data_tournaments_players

    def set_end_date_controller(self, name_of_tournament):
        tournament_table = self._get_tournament_table()

        end_date = self._serialize_date()

        tournament_table.update({"end_date": end_date}, Query().name == name_of_tournament)
