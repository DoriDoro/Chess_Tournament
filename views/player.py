from tinydb import TinyDB, Query
from controllers.player import PlayerControllers


class PlayerView:

    def __init__(self):
        self.player_controllers = PlayerControllers()

    # private function:
    def _get_tournament(self, name_of_tournament):
        db_tournament = TinyDB("data/tournaments/tournaments.json", indent=4)
        tournament_table = db_tournament.table("all_tournaments")

        return tournament_table.get(Query().name == name_of_tournament)

    # option 1: create player:
    def add_player_to_tournament_view(self, tournament_id_name_list):
        while True:
            choice = input(" Enter the Tournament_ID of your choice: ")
            print()

            # check if the user choice "*" to quit:
            if choice == "*":
                break

            # check if choice is an int and display the Tournament name or display error:
            choice = int(choice)

            tournament_found = False
            for tournament_id, name in tournament_id_name_list:
                get_number_players = self._get_tournament(name)["list_of_players"]
                number_players = len(get_number_players)

                if choice == tournament_id:
                    print(f" You have chosen: {name}", end="\n\n")
                    tournament_found = True

                    # TODO
                    if number_players == 8:
                        print(f"  {name} has already 8 players. Please choose an other tournament.")
                        print("   or choose * to go back to menu", end="\n\n")
                        break

                    else:
                        # TODO
                        number_of_player = 8
                        while number_of_player > 0:
                            self.create_player_view(name)
                            number_of_player -= 1
                            if number_of_player == 0:
                                return
            if not tournament_found:
                print(" Invalid choice. Please enter the Tournament_ID.", end="\n\n")

    # option 1: create player and option 3: start a tournament:
    def create_player_view(self, name_of_tournament):
        print("--------------------------------------------------------------------------")
        print(" ** CREATE A PLAYER **", end="\n\n")

        player_id = str(input(" Player ID (example: AB12345): "))
        first_name = str(input(" First name: "))
        last_name = str(input(f" Enter {first_name}'s last name: "))
        birth_date = str(
            input(f" Enter the birth date of {first_name} {last_name} (dd-mm-yyyy): ")
        )
        print()
        print(" You have just created this player: ")
        print(f"   [id]: {player_id}")
        print(f"   [name]: {first_name} {last_name}")
        print(f"   [birthday]: {birth_date}", end="\n\n")

        data_player = {
            "name_of_tournament": name_of_tournament,
            "player_id": player_id,
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
        }

        self.player_controllers.create_player_controller(data_player)

    # option 3: start tournament:
    def add_additional_player_to_tournament_view(self, name_of_tournament):
        print("   There are not enough players available for this tournament.", end="\n\n")
        self.create_player_view(name_of_tournament)
