from tinydb import TinyDB

from controller.player import pair_players_controller, create_score_controller
from controller.tournament import create_tournament_controller, reorganize_list_score_tournament_controller


# get tournaments for option 1: create a player and option 3: start a tournament
def get_tournaments_view():
    database = TinyDB(f'data/tournaments/tournaments.json')
    tournament_table = database.table("all_tournaments")

    tournament_id_name_list = []

    for db in tournament_table:
        tournament_id_name_list.append([db['tournament_id'], db['name']])

    return tournament_id_name_list


# option 2: create a tournament:
def create_tournament_view():
    print("------------------------------------------------")
    print(" ** CREATE A TOURNAMENT **", end="\n\n")

    tournament_id = int(input(" Tournament ID (example: 1234): "))
    name = str(input(" Name of tournament: "))
    city = str(input(" Location of tournament: "))
    start_date = str(input(" Start date (dd-mm-yyyy): "))
    end_date = str(input(" End date (dd-mm-yyyy): "))
    comments = str(input(" Any comments? "))
    print()
    print(f" You have just created this tournament:")
    print(f"   [Tournament ID]: {tournament_id}")
    print(f"   [name]: {name}")
    print(f"   [city]: {city}")
    print(f"   [start date]: {start_date} and [end date]: {end_date}")
    print(f"   [comments]: {comments}", end="\n\n")

    data_tournament = {"tournament_id": tournament_id, "name": name, "city": city, "start_date": start_date,
                       "end_date": end_date, "rounds": 4, "comments": comments}

    create_tournament_controller(data_tournament)


# option 3: start a tournament:
def display_tournaments_view(tournament_id_name_list):
    print("------------------------------------------------")
    print(" ** CHOOSE A TOURNAMENT **", end="\n\n")
    for db in tournament_id_name_list:
        print(f" [ID]: {db[0]}  -  [Name]: {db[1]}")
    print()
    print("   choose * to go back to menu", end="\n\n")


# option 3: start a tournament:
def choose_tournament_view(tournament_id_name_list):
    print("------------------------------------------------")
    print(" ** START A TOURNAMENT **", end="\n\n")

    while True:
        choice = input(" Enter the Tournament_ID of your choice: ")
        print()

        if choice == "*":
            break

        choice = int(choice)

        for tournament_id, name in tournament_id_name_list:
            if choice == tournament_id:
                print(f" You have chosen: {name}", end="\n\n")

                paired_players = pair_players_controller(name)
                if paired_players is None:
                    return
                else:
                    pair_players_names = paired_players["list_of_names"]
                    pair_players_ids = paired_players["paired_players"]

                    # TODO if tournament is over the print below are not working anymore
                    print(f"  The pairs for - {name} - are:", end="\n\n")
                    print(f"   pair 1  - {pair_players_names[0]} and {pair_players_names[1]}")
                    print(f"   pair 2  - {pair_players_names[2]} and {pair_players_names[3]}")
                    print(f"   pair 3  - {pair_players_names[4]} and {pair_players_names[5]}")
                    print(f"   pair 4  - {pair_players_names[6]} and {pair_players_names[7]}", end="\n\n")

                    print("  You choose the score of each match.", end="\n\n")

                    print("   Please enter: 1, 2 or 3.")
                    print("   1 means first player has won the match.")
                    print("   2 means second player has won the match.")
                    print("   3 is for a draw.", end="\n\n")

                    print("  Enter your choice for these matches: ", end="\n\n")

                    pair1 = int(input(f"  {pair_players_names[0]} and {pair_players_names[1]}: "))
                    pair2 = int(input(f"  {pair_players_names[2]} and {pair_players_names[3]}: "))
                    pair3 = int(input(f"  {pair_players_names[4]} and {pair_players_names[5]}: "))
                    pair4 = int(input(f"  {pair_players_names[6]} and {pair_players_names[7]}: "))

                    list_score_tournament = [[pair_players_ids[0], pair1,
                                             [pair_players_names[0], pair_players_names[1]]],
                                             [pair_players_ids[1], pair2,
                                             [pair_players_names[2], pair_players_names[3]]],
                                             [pair_players_ids[2], pair3,
                                             [pair_players_names[4], pair_players_names[5]]],
                                             [pair_players_ids[3], pair4,
                                             [pair_players_names[6], pair_players_names[7]]],
                                             pair_players_ids
                                             ]

                    print()

                    list_of_scores = create_score_controller(list_score_tournament)
                    reorganise_result = reorganize_list_score_tournament_controller(list_score_tournament, list_of_scores)

                    display_tournament_results_view(list_of_scores, reorganise_result, name)

                    return

        print(" Invalid choice. Please enter the Tournament_ID.", end="\n\n")


def display_tournament_results_view(list_of_scores, dict_score_tournament, name_of_tournament):
    print("------------------------------------------------")
    print(" ** RESULT OF A TOURNAMENT **", end="\n\n")

    print(f" These results are for the tournament:  - {name_of_tournament} - ", end="\n\n")

    for i in dict_score_tournament:
        if dict_score_tournament[i]["score"] == 1:
            print(f"   {i}: {dict_score_tournament[i]['names'][0]} against "
                  f"{dict_score_tournament[i]['names'][1]}  -- 1 : 0 ")

        elif dict_score_tournament[i]["score"] == 2:
            print(f"   {i}: {dict_score_tournament[i]['names'][0]} against "
                  f"{dict_score_tournament[i]['names'][1]}  -- 0 : 1 ")

        else:
            print(f"   {i}: {dict_score_tournament[i]['names'][0]} against "
                  f"{dict_score_tournament[i]['names'][1]}  -- 0.5 : 0.5 ")
    print()

    print(f" The score of each player: ", end="\n\n")

    for k, v in list_of_scores.items():
        name = v["name"]
        score = v["score"]
        print(f"   {name} has {score} points.")


def end_tournament_view(name_of_tournament):
    print(f"  The {name_of_tournament} is over.")
