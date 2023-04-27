def display_menu():
    print("--------------------------------------------------------------------------")
    print(" ** MAIN MENU **", end="\n\n")
    print(" 1. Create a Player")
    print(" 2. Create a Tournament")
    print(" 3. Start a Tournament")
    print(" 4. Quit program", end="\n\n")
    print("--------------------------------------------------------------------------")


def get_choice():
    choice = input(" Enter your choice of Options between 1 and 4: ")
    return choice


def quitting_program():
    print("--------------------------------------------------------------------------")
    print("  Quitting program...", end="\n\n")
