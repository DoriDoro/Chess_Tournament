import os
import sys

from controller.menu import run_menu


def main():
    # clear the terminal
    os.system("cls" if sys.platform == "win32" else "clear")
    print("Welcome to Chess Tournament")

    run_menu()


if __name__ == '__main__':
    main()
