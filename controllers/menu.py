from views.menu import MenuView
from views.player import PlayerView
from views.tournament import TournamentView


class MenuControllers:

    def __init__(self):
        self.menu_view = MenuView()
        self.tournament_view = TournamentView()
        self.player_view = PlayerView()

    def handle_create_player(self):
        tournament_id_name_list = self.tournament_view.get_tournaments_view()

        self.tournament_view.display_tournaments_view(tournament_id_name_list)
        self.player_view.add_player_to_tournament_view(tournament_id_name_list)

    def handle_create_tournament(self):
        self.tournament_view.create_tournament_view()

    def handle_start_tournament(self):
        tournament_id_name_list = self.tournament_view.get_tournaments_view()

        self.tournament_view.display_tournaments_view(tournament_id_name_list)
        self.tournament_view.choose_tournament_view(tournament_id_name_list)

    def run_menu(self):
        while True:
            self.menu_view.display_menu()
            choice = self.menu_view.get_choice()

            if choice == "1":
                self.handle_create_player()
            elif choice == "2":
                self.handle_create_tournament()
            elif choice == "3":
                self.handle_start_tournament()
            elif choice == "4":
                self.menu_view.quitting_program()
                break
            else:
                print("  Invalid choice. Please enter a number between 1 and 4.")
