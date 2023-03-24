import random

from tinydb import TinyDB, Query

from model.player import Player


# private functions:
def _get_tournament_table():
    db_tournament = TinyDB(f'data/tournaments/tournaments.json', indent=4)
    return db_tournament.table("all_tournaments")


def _get_tournament(name_of_tournament):
    db_tournament = TinyDB(f'data/tournaments/tournaments.json', indent=4)
    tournament_table = db_tournament.table("all_tournaments")

    return tournament_table.get(Query().name == name_of_tournament)


def _get_player_table():
    db_player = TinyDB('data/players/players.json', indent=4)
    player_table = db_player.table("all_players")

    return player_table


def _get_player(player_id):
    db_player = TinyDB('data/players/players.json', indent=4)
    player_table = db_player.table("all_players")

    return player_table.get(Query().player_id == player_id)


# option 1: create player:
def create_player_controller(data_player):
    new_player = Player(data_player["player_id"], data_player["first_name"], data_player["last_name"],
                        data_player["birth_date"])
    data = {"player_id": new_player.player_id, "first_name": new_player.first_name,
            "last_name": new_player.last_name, "birth_date": new_player.birth_date,
            "rank": 0, "score": 0.0,
            "played_tournaments": {"name": data_player["name_of_tournament"], "played_against": []}}

    # add player_id to the tournament in tournaments.json inside list_of_players:
    add_player_id_to_list_of_players_controller(new_player.player_id, data_player["name_of_tournament"])

    all_players = _get_player_table()
    all_players.insert(data)


def add_player_id_to_list_of_players_controller(player_id, tournament_name):
    get_list_of_players = get_player_id_from_list_of_players(tournament_name)

    tournament_table = _get_tournament_table()

    # update the list_of_player list in tournaments.json:
    tournament_table.update({"list_of_players": get_list_of_players + [player_id]}, Query().name == tournament_name)
    # database.close()


# option 1: create player and option 3: start a tournament:
# this function is not necessary
def get_player_id_from_list_of_players(name_of_tournament):
    tournament = _get_tournament(name_of_tournament)
    get_list_of_players = tournament['list_of_players']

    return get_list_of_players


# option 3: start a tournament:
def pair_players_first_round_controller(name_of_tournament):
    list_of_players = _get_tournament(name_of_tournament)["list_of_players"]

    pair_players = []
    for i in range(0, len(list_of_players), 2):
        pair = [list_of_players[i], list_of_players[i+1]]
        pair_players.append(pair)
        print("pair_players", pair_players)

    return pair_players


def pair_players_next_rounds_controller(name_of_tournament):
    list_of_players = _get_tournament(name_of_tournament)["list_of_players"]

    get_played_against = []
    for player_id in list_of_players:
        # print("list", _get_player(player_id)['played_tournaments']['played_against'])
        get_played_against_of_player = _get_player(player_id)['played_tournaments']['played_against']

        data = {"player_id": player_id, "played_against": get_played_against_of_player}
        get_played_against.append(data)

    paired_players = random.sample(list_of_players, k=2)
    # [['JI98563', 'YU60023'], ['JJ10203', 'DE75321'], ['ER11102', 'HG11102'], ['ER30003', 'WE15453']]
    print("paired", paired_players)

    for player in get_played_against:
        if player["player_id"] == paired_players[0]:
            print("player", player)
            if paired_players[1] in player["played_against"]:
                print("player 2", paired_players[1])
                print("list played against", player["played_against"])
                paired_players = random.sample(list_of_players, k=2)
                print("paired 2", paired_players)
        elif player["player_id"] == paired_players[1]:
            print("player", player)
            if paired_players[0] in player["played_against"]:
                print("player 1", paired_players[0])
                print("list played against", player["played_against"])
                paired_players = random.sample(list_of_players, k=2)
                print("else paired", paired_players)

    return get_played_against


def pair_players_controller(name_of_tournament):
    current_round = _get_tournament(name_of_tournament)["current_round"]
    rounds = _get_tournament(name_of_tournament)["rounds"]

    verify_number_of_player(name_of_tournament)

    if current_round == 0:
        paired_players = pair_players_first_round_controller(name_of_tournament)

        add_player_id_to_played_against_controller(paired_players, name_of_tournament, current_round)
        list_of_names = get_name_of_player(paired_players)

    elif current_round <= rounds:
        paired_players = pair_players_next_rounds_controller(name_of_tournament)
        print("next pairs", paired_players)

        add_player_id_to_played_against_controller(paired_players, name_of_tournament, current_round)
        list_of_names = get_name_of_player(paired_players)

    # TODO: if current_round is more than rounds do something...
    else:
        print("The tournament is over!")

    # update rounds in tournament
    # TODO create private function
    tournament_table = _get_tournament_table()
    tournament_table.update({"current_round": (current_round + 1)}, Query().name == name_of_tournament)

    return list_of_names


def verify_number_of_player(name_of_tournament):
    from views.player import add_additional_player_to_tournament_view

    get_verified_list_of_players_before = get_player_id_from_list_of_players(name_of_tournament)

    # check if 8 players are inside the list_of_players:
    number_of_players = len(get_verified_list_of_players_before)

    while number_of_players < 8:
        add_additional_player_to_tournament_view(name_of_tournament)
        number_of_players += 1

    get_verified_list_of_players = get_player_id_from_list_of_players(name_of_tournament)

    return get_verified_list_of_players


def add_player_id_to_played_against_controller(player_ids, name_of_tournament, current_round):
    tournament_table = _get_tournament_table()
    player_table = _get_player_table()

    # TODO: simplify this function  for i in range(0, 4)
    get_played_against_player_1 = _get_player(player_ids[0][0])["played_tournaments"]["played_against"]
    get_played_against_player_1 += [player_ids[0][1]]

    get_played_against_player_2 = _get_player(player_ids[0][1])["played_tournaments"]["played_against"]
    get_played_against_player_2 += [player_ids[0][0]]

    get_played_against_player_3 = _get_player(player_ids[1][0])["played_tournaments"]["played_against"]
    get_played_against_player_3 += [player_ids[1][1]]

    get_played_against_player_4 = _get_player(player_ids[1][1])["played_tournaments"]["played_against"]
    get_played_against_player_4 += [player_ids[1][0]]

    get_played_against_player_5 = _get_player(player_ids[2][0])["played_tournaments"]["played_against"]
    get_played_against_player_5 += [player_ids[2][1]]

    get_played_against_player_6 = _get_player(player_ids[2][1])["played_tournaments"]["played_against"]
    get_played_against_player_6 += [player_ids[2][0]]

    get_played_against_player_7 = _get_player(player_ids[3][0])["played_tournaments"]["played_against"]
    get_played_against_player_7 += [player_ids[3][1]]

    get_played_against_player_8 = _get_player(player_ids[3][1])["played_tournaments"]["played_against"]
    get_played_against_player_8 += [player_ids[3][0]]

    data = {current_round: player_ids}

    tournament_table.update({"list_rounds": data}, Query().name == name_of_tournament)

    # TODO simplify this function
    player_table.update({"played_tournaments": {"name": name_of_tournament,
                                                "played_against": get_played_against_player_1}},
                        Query().player_id == player_ids[0][1])
    player_table.update({'played_tournaments': {'name': name_of_tournament,
                                                'played_against': get_played_against_player_2}},
                        Query().player_id == player_ids[0][0])

    player_table.update({"played_tournaments": {"name": name_of_tournament,
                                                "played_against": get_played_against_player_3}},
                        Query().player_id == player_ids[1][1])
    player_table.update({'played_tournaments': {'name': name_of_tournament,
                                                'played_against': get_played_against_player_4}},
                        Query().player_id == player_ids[1][0])

    player_table.update({"played_tournaments": {"name": name_of_tournament,
                                                "played_against": get_played_against_player_5}},
                        Query().player_id == player_ids[2][1])
    player_table.update({'played_tournaments': {'name': name_of_tournament,
                                                'played_against': get_played_against_player_6}},
                        Query().player_id == player_ids[2][0])

    player_table.update({"played_tournaments": {"name": name_of_tournament,
                                                "played_against": get_played_against_player_7}},
                        Query().player_id == player_ids[3][1])
    player_table.update({'played_tournaments': {'name': name_of_tournament,
                                                'played_against': get_played_against_player_8}},
                        Query().player_id == player_ids[3][0])


def get_name_of_player(player_ids):
    player_table = _get_player_table()

    player_1 = player_table.get(Query().player_id == player_ids[0][0])
    p1_name = f"{player_1['first_name']} {player_1['last_name']}"

    player_2 = player_table.get(Query().player_id == player_ids[0][1])
    p2_name = f"{player_2['first_name']} {player_2['last_name']}"

    player_3 = player_table.get(Query().player_id == player_ids[1][0])
    p3_name = f"{player_3['first_name']} {player_3['last_name']}"

    player_4 = player_table.get(Query().player_id == player_ids[1][1])
    p4_name = f"{player_4['first_name']} {player_4['last_name']}"

    player_5 = player_table.get(Query().player_id == player_ids[2][0])
    p5_name = f"{player_5['first_name']} {player_5['last_name']}"

    player_6 = player_table.get(Query().player_id == player_ids[2][1])
    p6_name = f"{player_6['first_name']} {player_6['last_name']}"

    player_7 = player_table.get(Query().player_id == player_ids[3][0])
    p7_name = f"{player_7['first_name']} {player_7['last_name']}"

    player_8 = player_table.get(Query().player_id == player_ids[3][1])
    p8_name = f"{player_8['first_name']} {player_8['last_name']}"

    return p1_name, p2_name, p3_name, p4_name, p5_name, p6_name, p7_name, p8_name
