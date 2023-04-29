from tinydb import TinyDB

from controllers.player import (
    pair_players_controller,
    update_score_controller,
    get_results_players_controller,
)
from controllers.tournament import (
    create_tournament_controller,
    reorganize_list_score_tournament_controller,
    add_player_score_to_list_rounds_controller,
    get_current_round_controller,
    get_list_round_info_controller,
    get_results_tournaments_controller,
    set_end_date_controller,
)


class TournamentView:

    def __init__(self):
        pass

    # get tournaments for option 1: create a player and option 3: start a tournament
    def get_tournaments_view(self):
        database = TinyDB("data/tournaments/tournaments.json")
        tournament_table = database.table("all_tournaments")

        tournament_id_name_list = []

        for db in tournament_table:
            tournament_id_name_list.append([db["tournament_id"], db["name"]])

        return tournament_id_name_list

    # option 2: create a tournament:
    def create_tournament_view(self):
        print("--------------------------------------------------------------------------")
        print(" ** CREATE A TOURNAMENT **", end="\n\n")

        tournament_id = int(input(" Tournament ID (example: 1234): "))
        name = str(input(" Name of tournament: "))
        city = str(input(" Location of tournament: "))
        comments = str(input(" Any comments? "))
        print()
        print(" You have just created this tournament:")
        print(f"   [Tournament ID]: {tournament_id}")
        print(f"   [name]: {name}")
        print(f"   [city]: {city}")
        print(f"   [comments]: {comments}", end="\n\n")

        data_tournament = {
            "tournament_id": tournament_id,
            "name": name,
            "city": city,
            "rounds": 4,
            "comments": comments,
        }

        create_tournament_controller(data_tournament)

    # option 3: start a tournament:
    def display_tournaments_view(self, tournament_id_name_list):
        print("--------------------------------------------------------------------------")
        print(" ** CHOOSE A TOURNAMENT **", end="\n\n")
        for db in tournament_id_name_list:
            print(f" [ID]: {db[0]}  -  [Name]: {db[1]}")
        print()
        print("   choose * to go back to menu", end="\n\n")

    def choose_tournament_view(self, tournament_id_name_list):
        print("--------------------------------------------------------------------------")
        print(" ** START A TOURNAMENT **", end="\n\n")

        while True:
            choice = input(" Enter the Tournament_ID of your choice: ")
            print()

            if choice == "*":
                break

            choice = int(choice)

            for tournament_id, name in tournament_id_name_list:
                current_round = get_current_round_controller(name)

                if choice == tournament_id:
                    print(f" You have chosen: {name}", end="\n\n")

                    if current_round > 0:
                        yes_no = str(
                            input(
                                f"   Do you want to continue with {name}  - [yes] or [no]?  "
                            )
                        )
                        print()

                        if yes_no == "yes":
                            get_last_round = get_list_round_info_controller(name)
                            get_last_round = int(get_last_round)

                            if get_last_round < 4:
                                next_round = get_last_round + 1
                                print(
                                    f"   The last time you was playing -{name}- in round {get_last_round}."
                                )
                                print(
                                    f"   You will continue with the round {next_round}.",
                                    end="\n\n",
                                )
                            else:
                                self.end_tournament_view(name)
                                return
                        elif yes_no == "no":
                            return
                        else:
                            print(
                                " Invalid answer. Please enter [yes] or [no].", end="\n\n"
                            )

                    # start the next round:
                    paired_players = pair_players_controller(name)

                    if paired_players is None:
                        return
                    else:
                        pair_players_names = paired_players["list_of_names"]
                        pair_players_ids = paired_players["paired_players"]

                        print(f"  The pairs for - {name} - are:", end="\n\n")
                        print(
                            f"   pair 1  - {pair_players_names[0]} and {pair_players_names[1]}"
                        )
                        print(
                            f"   pair 2  - {pair_players_names[2]} and {pair_players_names[3]}"
                        )
                        print(
                            f"   pair 3  - {pair_players_names[4]} and {pair_players_names[5]}"
                        )
                        print(
                            f"   pair 4  - {pair_players_names[6]} and {pair_players_names[7]}",
                            end="\n\n",
                        )

                        print("  You choose the score of each match.", end="\n\n")

                        print("   Please enter: 1, 2 or 3.")
                        print("   1 means first player has won the match.")
                        print("   2 means second player has won the match.")
                        print("   3 is for a draw.", end="\n\n")

                        print("  Enter the score for these matches: ", end="\n\n")

                        pair1 = int(
                            input(
                                f"  {pair_players_names[0]} and {pair_players_names[1]}: "
                            )
                        )
                        pair2 = int(
                            input(
                                f"  {pair_players_names[2]} and {pair_players_names[3]}: "
                            )
                        )
                        pair3 = int(
                            input(
                                f"  {pair_players_names[4]} and {pair_players_names[5]}: "
                            )
                        )
                        pair4 = int(
                            input(
                                f"  {pair_players_names[6]} and {pair_players_names[7]}: "
                            )
                        )

                        list_score_tournament = [
                            [
                                pair_players_ids[0],
                                pair1,
                                [pair_players_names[0], pair_players_names[1]],
                            ],
                            [
                                pair_players_ids[1],
                                pair2,
                                [pair_players_names[2], pair_players_names[3]],
                            ],
                            [
                                pair_players_ids[2],
                                pair3,
                                [pair_players_names[4], pair_players_names[5]],
                            ],
                            [
                                pair_players_ids[3],
                                pair4,
                                [pair_players_names[6], pair_players_names[7]],
                            ],
                            pair_players_ids,
                        ]
                        print()

                        list_of_scores = update_score_controller(list_score_tournament)

                        add_player_score_to_list_rounds_controller(
                            name, list_of_scores, current_round
                        )

                        dict_score_tournament = reorganize_list_score_tournament_controller(
                            list_score_tournament
                        )

                        self.display_tournament_results_view(
                            list_of_scores, dict_score_tournament, name
                        )

                        return

            print(" Invalid choice. Please enter the Tournament_ID.", end="\n\n")

    def display_tournament_results_view(
        self, list_of_scores, dict_score_tournament, name_of_tournament
    ):
        print("--------------------------------------------------------------------------")
        print(" ** RESULT OF A TOURNAMENT **", end="\n\n")

        print(
            f" These results are for the tournament:  - {name_of_tournament} - ", end="\n\n"
        )

        for i in dict_score_tournament:
            if dict_score_tournament[i]["score"] == 1:
                print(
                    f"   {i}: {dict_score_tournament[i]['names'][0]} against "
                    f"{dict_score_tournament[i]['names'][1]}  -- 1 : 0 "
                )

            elif dict_score_tournament[i]["score"] == 2:
                print(
                    f"   {i}: {dict_score_tournament[i]['names'][0]} against "
                    f"{dict_score_tournament[i]['names'][1]}  -- 0 : 1 "
                )

            else:
                print(
                    f"   {i}: {dict_score_tournament[i]['names'][0]} against "
                    f"{dict_score_tournament[i]['names'][1]}  -- 0.5 : 0.5 "
                )
        print()

        print(" The score of each player: ", end="\n\n")

        for k, v in list_of_scores.items():
            name = v["name"]
            score = float(v["score"])
            print(f"   {name} has {score} points.")

    def end_tournament_view(self, name_of_tournament):
        print(f"  The {name_of_tournament} is over.")

        set_end_date_controller(name_of_tournament)

        self.display_end_result_view()


    def display_end_result_view(self):
        print("--------------------------------------------------------------------------")
        print(" ** RESULT OF ALL TOURNAMENTS **", end="\n\n")

        results_tournaments = get_results_tournaments_controller()
        results_players = get_results_players_controller()

        player_names = []
        for i, name in results_players.items():
            player_names.append(name)
        player_names.sort()

        print(" -- ALL PLAYERS: --", end="\n\n")
        for i, name in enumerate(player_names):
            if i != len(player_names) - 1:
                if i % 5 == 4:
                    print(name + ", ")
                else:
                    print(name + ", ", end="")
            else:
                print("and " + name)
        print(end="\n\n")

        print(" -- NAMES OF TOURNAMENTS: --", end="\n\n")
        for name, values in results_tournaments.items():
            print(f' [ID] {values["tournament_id"]} [name] {name}')
        print(end="\n\n")

        print(" -- NAMES AND DATES OF TOURNAMENTS: --", end="\n\n")

        for name, info in results_tournaments.items():
            print(f" {name}")
            print(
                f'  [start]: {info["start_date"]} and [end]: {info["end_date"]}', end="\n\n"
            )

        print(" -- PLAYERS OF EACH TOURNAMENT: --", end="\n\n")

        for name_tournament, info in results_tournaments.items():
            print(f"[Name of tournament]: {name_tournament}", end="\n\n")
            print("[Name of players]: ")
            player_names = sorted(
                [player["name"] for player in info["player_data"].values()]
            )
            for name in player_names:
                print(f" {name}")
            print()

        print("  -- ALL MATCHES OF TOURNAMENT: --", end="\n\n")

        for name_of_tournament, data in results_tournaments.items():
            print(f"[Name of tournament]: {name_of_tournament}", end="\n\n")
            print("[Matches of players]: ")
            pair_count = 0
            for rounds in results_tournaments[name_tournament]["list_rounds"].values():
                for i, player in enumerate(rounds.keys()):
                    if i % 2 == 0:
                        pair = [
                            rounds[player]["name"],
                            rounds[list(rounds.keys())[i + 1]]["name"],
                        ]
                        print(f" {pair[0]}   played against   {pair[1]}")
                        pair_count += 1
                        if pair_count % 4 == 0:
                            print()
            print(end="\n\n")
