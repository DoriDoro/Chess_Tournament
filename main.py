import os
import sys

from tinydb import TinyDB, Query

from model.player import Player


def main():
    # clear the terminal
    os.system("cls" if sys.platform == "win32" else "clear")
    print("Welcome to Chess Tournament")

    Player.create_player()
    # Player.create_pairs()


if __name__ == '__main__':
    main()
