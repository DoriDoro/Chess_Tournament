import random

from tinydb import TinyDB, Query

from models.player import Player


class PlayerControllers:

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

    def _get_player_table(self):
        db_player = TinyDB("data/players/players.json", indent=4)
        player_table = db_player.table("all_players")

        return player_table

    def _get_player(self, player_id):
        db_player = TinyDB("data/players/players.json", indent=4)
        player_table = db_player.table("all_players")

        return player_table.get(Query().player_id == player_id)

    def _reorder_create_pairs(self, i, create_pairs):
        i += 1
        pop_element = create_pairs.pop(i)

        if i < 7:
            create_pairs.append(pop_element)
        else:
            create_pairs.insert(0, pop_element)

        return create_pairs

    def _get_score_of_player(self, list_score_tournament):
        player_table = self._get_player_table()

        player_ids_score = {}

        for pair in list_score_tournament[4]:
            for player_id in pair:
                score_table = player_table.get(Query().player_id == player_id)
                name = f'{score_table["first_name"]} {score_table["last_name"]}'
                score = score_table["score"]
                player_ids_score[player_id] = {"score": score, "name": name}

        return player_ids_score

    # option 1: create player:
    def create_player_controller(self, data_player):
        new_player = Player(
            data_player["player_id"],
            data_player["first_name"],
            data_player["last_name"],
            data_player["birth_date"],
        )
        data = {
            "player_id": new_player.player_id,
            "first_name": new_player.first_name,
            "last_name": new_player.last_name,
            "birth_date": new_player.birth_date,
            "rank": 0,
            "score": 0,
            "played_tournaments": {
                "name": data_player["name_of_tournament"],
                "played_against": [],
            },
        }

        # add player_id to the tournament in tournaments.json inside list_of_players:
        self.add_player_id_to_list_of_players_controller(
            new_player.player_id, data_player["name_of_tournament"]
        )

        all_players = self._get_player_table()
        all_players.insert(data)

    def add_player_id_to_list_of_players_controller(self, player_id, name_of_tournament):
        get_list_of_players = self._get_tournament(name_of_tournament)["list_of_players"]

        tournament_table = self._get_tournament_table()

        tournament_table.update(
            {"list_of_players": get_list_of_players + [player_id]},
            Query().name == name_of_tournament,
        )

    # option 3: start a tournament:
    def pair_players_first_round_controller(self, name_of_tournament):
        list_of_players = self._get_tournament(name_of_tournament)["list_of_players"]
        random.shuffle(list_of_players)
        # convert to a tuple
        pair_players = list(zip(list_of_players[0::2], list_of_players[1::2]))

        return pair_players

    def pair_players_next_rounds_controller(self, name_of_tournament, current_round):
        list_rounds_tournament = self._get_tournament(name_of_tournament)["list_rounds"]
        current_list_rounds = list_rounds_tournament[f"{current_round}"]

        player_id_played_score_against = []
        for list_rounds in current_list_rounds:
            for player in list_rounds:
                if "played_tournaments" in player:
                    player_id = player["player_id"]
                    score = player["score"]
                    opponents = player["played_tournaments"]["played_against"]
                    player_id_played_score_against.append(
                        {
                            "player_id": player_id,
                            "played_against": opponents,
                            "score": score,
                        }
                    )

        sorted_list_rounds = sorted(
            player_id_played_score_against, key=lambda x: x["score"]
        )

        create_pairs = []
        # match players, avoid already paired:
        for player in sorted_list_rounds:
            player_id = player["player_id"]
            create_pairs.append(player_id)

        already_played_against = False
        for i, p_id in enumerate(create_pairs):
            if i % 2 == 0:
                for player_data in sorted_list_rounds:
                    if player_data["player_id"] == p_id:
                        for player in player_data["played_against"]:
                            if player == create_pairs[i + 1]:
                                reordered_create_pairs = self._reorder_create_pairs(
                                    i, create_pairs
                                )
                                already_played_against = True
                                break
                        if already_played_against:
                            create_pairs = reordered_create_pairs
                            already_played_against = False
                            continue

        # convert to tuple:
        pair_players = list(zip(create_pairs[0::2], create_pairs[1::2]))

        return pair_players

    def pair_players_controller(self, name_of_tournament):
        from views.tournament import TournamentView
        tournament_view = TournamentView()

        current_round = self._get_tournament(name_of_tournament)["current_round"]
        rounds = self._get_tournament(name_of_tournament)["rounds"]

        self.verify_number_of_player_controller(name_of_tournament)

        if current_round == 0:
            paired_players = self.pair_players_first_round_controller(name_of_tournament)

            self.add_player_id_to_played_against_controller(paired_players, name_of_tournament)
            list_of_names = self.get_name_of_player_controller(paired_players)

        elif current_round < rounds:
            paired_players = self.pair_players_next_rounds_controller(
                name_of_tournament, current_round
            )

            self.add_player_id_to_played_against_controller(paired_players, name_of_tournament)
            list_of_names = self.get_name_of_player_controller(paired_players)

        else:
            return tournament_view.end_tournament_view(name_of_tournament)

        # update rounds in tournament
        tournament_table = self._get_tournament_table()
        tournament_table.update(
            {"current_round": (current_round + 1)}, Query().name == name_of_tournament
        )

        return {"paired_players": paired_players, "list_of_names": list_of_names}

    def verify_number_of_player_controller(self, name_of_tournament):
        from views.player import PlayerView
        player_view = PlayerView()

        get_verified_list_of_players_before = self._get_tournament(name_of_tournament)[
            "list_of_players"
        ]

        number_of_players = len(get_verified_list_of_players_before)

        # TODO
        while number_of_players < 8:
            player_view.add_additional_player_to_tournament_view(name_of_tournament)
            number_of_players += 1

        get_verified_list_of_players = self._get_tournament(name_of_tournament)[
            "list_of_players"
        ]

        return get_verified_list_of_players

    def add_player_id_to_played_against_controller(self, player_ids, name_of_tournament):
        player_table = self._get_player_table()

        for player in player_ids:
            player_tmp1 = self._get_player(player[0])["played_tournaments"]["played_against"] + [
                player[1]
            ]
            player_tmp2 = self._get_player(player[1])["played_tournaments"]["played_against"] + [
                player[0]
            ]

            player_table.update(
                {
                    "played_tournaments": {
                        "name": name_of_tournament,
                        "played_against": player_tmp1,
                    }
                },
                Query().player_id == player[0],
            )
            player_table.update(
                {
                    "played_tournaments": {
                        "name": name_of_tournament,
                        "played_against": player_tmp2,
                    }
                },
                Query().player_id == player[1],
            )

    def get_name_of_player_controller(self, player_ids):
        player_table = self._get_player_table()

        pair_table = []
        for pair in player_ids:
            player_tmp1 = player_table.get(Query().player_id == pair[0])
            p1_name = f"{player_tmp1['first_name']} {player_tmp1['last_name']}"
            pair_table.append(p1_name)

            player_tmp2 = player_table.get(Query().player_id == pair[1])
            p2_name = f"{player_tmp2['first_name']} {player_tmp2['last_name']}"
            pair_table.append(p2_name)

        return pair_table

    def update_score_controller(self, list_score_tournament):
        player_table = self._get_player_table()

        player_ids_score = self._get_score_of_player(list_score_tournament)

        for i in range(0, 4):
            if list_score_tournament[i][1] == 1:
                for player_id in list_score_tournament[i][0]:
                    if player_id == list_score_tournament[i][0][0]:
                        player_table.update(
                            {"score": (player_ids_score[player_id]["score"] + 1)},
                            Query().player_id == player_id,
                        )
            elif list_score_tournament[i][1] == 2:
                for player_id in list_score_tournament[i][0]:
                    if player_id == list_score_tournament[i][0][1]:
                        player_table.update(
                            {"score": (player_ids_score[player_id]["score"] + 1)},
                            Query().player_id == player_id,
                        )
            elif list_score_tournament[i][1] == 3:
                for player_id in list_score_tournament[i][0]:
                    player_table.update(
                        {"score": (player_ids_score[player_id]["score"] + 0.5)},
                        Query().player_id == player_id,
                    )

        updated_player_ids_score = self._get_score_of_player(list_score_tournament)

        return updated_player_ids_score

    def get_results_players_controller(self):
        players = self._get_player_table()

        data_players = {}
        for player in players:
            name = f'{player["first_name"]} {player["last_name"]}'
            data_players[player["player_id"]] = name

        return data_players
