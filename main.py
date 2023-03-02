import os
import sys

from views.player import create_player
from views.tournament import create_tournament


def main():
    # clear the terminal
    os.system("cls" if sys.platform == "win32" else "clear")
    print("Welcome to Chess Tournament")

    # create_player()
    create_tournament()


if __name__ == '__main__':
    main()
