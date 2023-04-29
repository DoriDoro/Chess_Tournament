from views.menu import MenuView
from views.player import (
    add_player_to_tournament_view,
)
from views.tournament import (
    choose_tournament_view,
    create_tournament_view,
    display_tournaments_view,
    get_tournaments_view,
)


class MenuControllers:

    def __init__(self):
        self.menu = MenuView()

    def handle_create_player(self):
        tournament_id_name_list = get_tournaments_view()

        display_tournaments_view(tournament_id_name_list)
        add_player_to_tournament_view(tournament_id_name_list)

    def handle_create_tournament(self):
        create_tournament_view()

    def handle_start_tournament(self):
        tournament_id_name_list = get_tournaments_view()

        display_tournaments_view(tournament_id_name_list)
        choose_tournament_view(tournament_id_name_list)

    def run_menu(self):
        while True:
            self.menu.display_menu()
            choice = self.menu.get_choice()

            if choice == "1":
                self.handle_create_player()
            elif choice == "2":
                self.handle_create_tournament()
            elif choice == "3":
                self.handle_start_tournament()
            elif choice == "4":
                self.menu.quitting_program()
                break
            else:
                print("  Invalid choice. Please enter a number between 1 and 4.")
