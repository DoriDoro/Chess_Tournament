
from datetime import datetime


# models
class Player:

	def __init__(self, player_id, first_name, last_name, birth_date):
		self.player_id = player_id
		self.first_name = first_name
		self.last_name = last_name
		self.birth_date = birth_date

		self.rank = 0
		self.score = 0.0
		self.played_against = []

	def __str__(self):
		return f"{self.first_name} {self.last_name}"

	@staticmethod
	def create_player():
		players = []

		player_id = str(input("Enter the ID of the player (example: AB12345): "))
		# check if the player_id is 2 letters and 5 numbers
		first_name = str(input("Enter the first name of the player: "))
		last_name = str(input(f"Enter {first_name}'s last name: "))
		birthday = str(input(f"Enter the birth date of {first_name} {last_name} (yyyy-mm-dd): "))
		birth_date = datetime.strptime(birthday, "%Y-%m-%d")

		new_player = Player(player_id, first_name, last_name, birth_date)
		players.append(new_player)

		return players

	# def create_player_id(self, player):
	# 	# example: AB12345 (2 letters and 5 numbers)
	#
	# 	available_numbers = list(string.digits)
	# 	letters = ['AB', 'BC', 'CD', 'DE', 'EF', 'FG', 'GH', 'HI', 'IJ', 'JK', 'KL', 'LM', 'MN', 'NO', 'OP', 'PR',
	# 				'RS', 'ST', 'TU', 'UV', 'VX', 'XY', 'YZ']
	# 	id_numbers = 5
	# 	# use one of the letters list and add it to the player_id
	# 	player_id = letters
	# 	for n in range(id_numbers):
	# 		print('n', n)
	# 		player_id += random.choice(available_numbers)
	# 	# replace the player_id = "" with this player_id
	# 	# check if player_id is unique
	# 	print(player_id)

# create player_id for created player
# connect a player/s with a Tournament, add_player_to_tournament
# save player in JSON data file


class Tournament:

	def __init__(
			self, name, city, start_date, end_date, list_rounds, comments, rounds=4):
		self.name = name
		self.city = city
		self.start_date = start_date
		self.end_date = end_date
		self.list_rounds = list_rounds
		self.comments = comments
		self.rounds = rounds

		self.list_of_players = []
		self.tournament_id = ""
		self.current_round = 0
		self.match_list = []

	@staticmethod
	def create_tournament():
		tournaments = []

		name = str(input("Enter the name of the Chess Tournament: "))
		city = str(input("Enter the location of the Chess Tournament: "))
		s_date = str(input("When does the Chess Tournament starts? (yyyy-mm-dd): "))
		start_date = datetime.strptime(s_date, "%Y-%m-%d")
		e_date = str(input("Please enter the end date of the Chess Tournament (yyyy-mm-dd): "))
		end_date = datetime.strptime(e_date, "%Y-%m-%d")
		rounds = int(input("How many rounds are possible for this Chess Tournament? "))
		comments = str(input("Do you have any comments concerning the Chess Tournament? "))

		new_tournament = Tournament(name, city, start_date, end_date, rounds, comments)
		tournaments.append(new_tournament)

	def get_tournament(self):
		pass

	# def get_tournament
	# def update_tournament
	# def update_match_list
	# def shuffle_players including the first match

