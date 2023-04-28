import os
import sys

from controllers.menu import MenuControllers


def main():
    # clear the terminal
    os.system("cls" if sys.platform == "win32" else "clear")
    print("  -- Welcome to Chess Tournament --")

    menu = MenuControllers()
    menu.run_menu()


if __name__ == "__main__":
    main()
