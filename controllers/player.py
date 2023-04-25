import random

from tinydb import TinyDB, Query

from models.player import Player


# private functions:
def _get_tournament_table():
    db_tournament = TinyDB('data/tournaments/tournaments.json', indent=4)
    return db_tournament.table("all_tournaments")


def _get_tournament(name_of_tournament):
    db_tournament = TinyDB('data/tournaments/tournaments.json', indent=4)
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


def _reorder_create_pairs(i, create_pairs):
    i += 1
    pop_element = create_pairs.pop(i)

    if i < 7:
        create_pairs.append(pop_element)
    else:
        create_pairs.insert(0, pop_element)

    return create_pairs


def _get_score_of_player(list_score_tournament):
    player_table = _get_player_table()

    player_ids_score = {}

    for pair in list_score_tournament[4]:
        for player_id in pair:
            score_table = player_table.get(Query().player_id == player_id)
            name = f'{score_table["first_name"]} {score_table["last_name"]}'
            score = score_table["score"]
            player_ids_score[player_id] = {"score": score, "name": name}

    return player_ids_score


# option 1: create player:
def create_player_controller(data_player):
    new_player = Player(data_player["player_id"], data_player["first_name"], data_player["last_name"],
                        data_player["birth_date"])
    data = {
        "player_id": new_player.player_id,
        "first_name": new_player.first_name,
        "last_name": new_player.last_name,
        "birth_date": new_player.birth_date,
        "rank": 0,
        "score": 0,
        "played_tournaments": {"name": data_player["name_of_tournament"], "played_against": []}
    }

    # add player_id to the tournament in tournaments.json inside list_of_players:
    add_player_id_to_list_of_players_controller(new_player.player_id, data_player["name_of_tournament"])

    all_players = _get_player_table()
    all_players.insert(data)


def add_player_id_to_list_of_players_controller(player_id, name_of_tournament):
    get_list_of_players = _get_tournament(name_of_tournament)["list_of_players"]

    tournament_table = _get_tournament_table()

    tournament_table.update({"list_of_players": get_list_of_players + [player_id]}, Query().name == name_of_tournament)


# option 3: start a tournament:
def pair_players_first_round_controller(name_of_tournament):
    list_of_players = _get_tournament(name_of_tournament)["list_of_players"]
    random.shuffle(list_of_players)
    # convert to a tuple
    pair_players = list(zip(list_of_players[0::2], list_of_players[1::2]))

    return pair_players


def pair_players_next_rounds_controller(name_of_tournament, current_round):
    list_rounds_tournament = _get_tournament(name_of_tournament)['list_rounds']
    current_list_rounds = list_rounds_tournament[f"{current_round}"]

    player_id_played_score_against = []
    for list_rounds in current_list_rounds:
        for player in list_rounds:
            if "played_tournaments" in player:
                player_id = player["player_id"]
                score = player["score"]
                opponents = player["played_tournaments"]["played_against"]
                player_id_played_score_against\
                    .append({"player_id": player_id, "played_against": opponents, "score": score})

    sorted_list_rounds = sorted(player_id_played_score_against, key=lambda x: x['score'])

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
                            reordered_create_pairs = _reorder_create_pairs(i, create_pairs)
                            already_played_against = True
                            break
                    if already_played_against:
                        create_pairs = reordered_create_pairs
                        already_played_against = False
                        continue

    # convert to tuple:
    pair_players = list(zip(create_pairs[0::2], create_pairs[1::2]))

    return pair_players


def pair_players_controller(name_of_tournament):
    from views.tournament import end_tournament_view

    current_round = _get_tournament(name_of_tournament)["current_round"]
    rounds = _get_tournament(name_of_tournament)["rounds"]

    verify_number_of_player_controller(name_of_tournament)

    if current_round == 0:
        paired_players = pair_players_first_round_controller(name_of_tournament)

        add_player_id_to_played_against_controller(paired_players, name_of_tournament)
        list_of_names = get_name_of_player_controller(paired_players)

    elif current_round < rounds:
        paired_players = pair_players_next_rounds_controller(name_of_tournament, current_round)

        add_player_id_to_played_against_controller(paired_players, name_of_tournament)
        list_of_names = get_name_of_player_controller(paired_players)

    else:
        return end_tournament_view(name_of_tournament)

    # update rounds in tournament
    tournament_table = _get_tournament_table()
    tournament_table.update({"current_round": (current_round + 1)}, Query().name == name_of_tournament)

    return {"paired_players": paired_players, "list_of_names": list_of_names}


def verify_number_of_player_controller(name_of_tournament):
    from views.player import add_additional_player_to_tournament_view

    get_verified_list_of_players_before = _get_tournament(name_of_tournament)['list_of_players']

    number_of_players = len(get_verified_list_of_players_before)

    while number_of_players < 8:
        add_additional_player_to_tournament_view(name_of_tournament)
        number_of_players += 1

    get_verified_list_of_players = _get_tournament(name_of_tournament)['list_of_players']

    return get_verified_list_of_players


def add_player_id_to_played_against_controller(player_ids, name_of_tournament):
    player_table = _get_player_table()

    # TODO: simplify this function  for i in range(0, 4)
    player_1 = _get_player(player_ids[0][0])["played_tournaments"]["played_against"]
    player_1 += [player_ids[0][1]]
    player_2 = _get_player(player_ids[0][1])["played_tournaments"]["played_against"]
    player_2 += [player_ids[0][0]]

    player_3 = _get_player(player_ids[1][0])["played_tournaments"]["played_against"]
    player_3 += [player_ids[1][1]]
    player_4 = _get_player(player_ids[1][1])["played_tournaments"]["played_against"]
    player_4 += [player_ids[1][0]]

    player_5 = _get_player(player_ids[2][0])["played_tournaments"]["played_against"]
    player_5 += [player_ids[2][1]]
    player_6 = _get_player(player_ids[2][1])["played_tournaments"]["played_against"]
    player_6 += [player_ids[2][0]]

    player_7 = _get_player(player_ids[3][0])["played_tournaments"]["played_against"]
    player_7 += [player_ids[3][1]]
    player_8 = _get_player(player_ids[3][1])["played_tournaments"]["played_against"]
    player_8 += [player_ids[3][0]]

    # TODO simplify this function
    player_table.update({"played_tournaments": {"name": name_of_tournament, "played_against": player_1}},
                        Query().player_id == player_ids[0][0])
    player_table.update({'played_tournaments': {'name': name_of_tournament, 'played_against': player_2}},
                        Query().player_id == player_ids[0][1])

    player_table.update({"played_tournaments": {"name": name_of_tournament, "played_against": player_3}},
                        Query().player_id == player_ids[1][0])
    player_table.update({'played_tournaments': {'name': name_of_tournament, 'played_against': player_4}},
                        Query().player_id == player_ids[1][1])

    player_table.update({"played_tournaments": {"name": name_of_tournament, "played_against": player_5}},
                        Query().player_id == player_ids[2][0])
    player_table.update({'played_tournaments': {'name': name_of_tournament, 'played_against': player_6}},
                        Query().player_id == player_ids[2][1])

    player_table.update({"played_tournaments": {"name": name_of_tournament, "played_against": player_7}},
                        Query().player_id == player_ids[3][0])
    player_table.update({'played_tournaments': {'name': name_of_tournament, 'played_against': player_8}},
                        Query().player_id == player_ids[3][1])


def get_name_of_player_controller(player_ids):
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


def update_score_controller(list_score_tournament):
    player_table = _get_player_table()

    player_ids_score = _get_score_of_player(list_score_tournament)

    for i in range(0, 4):
        if list_score_tournament[i][1] == 1:
            for player_id in list_score_tournament[i][0]:
                if player_id == list_score_tournament[i][0][0]:
                    player_table.update({"score": (player_ids_score[player_id]["score"] + 1)},
                                        Query().player_id == player_id)
        elif list_score_tournament[i][1] == 2:
            for player_id in list_score_tournament[i][0]:
                if player_id == list_score_tournament[i][0][1]:
                    player_table.update({"score": (player_ids_score[player_id]["score"] + 1)},
                                        Query().player_id == player_id)
        elif list_score_tournament[i][1] == 3:
            for player_id in list_score_tournament[i][0]:
                player_table.update({"score": (player_ids_score[player_id]["score"] + 0.5)},
                                    Query().player_id == player_id)

    updated_player_ids_score = _get_score_of_player(list_score_tournament)

    return updated_player_ids_score


def get_results_players_controller():
    players = _get_player_table()

    data_players = {}
    for player in players:
        name = f'{player["first_name"]} {player["last_name"]}'
        data_players[player["player_id"]] = name

    return data_players
