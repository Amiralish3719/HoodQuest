from user_system import UserSystem
import sys
DIVIDER = "=" * 60
def print_header(title):
    print(DIVIDER)
    print(title.center(60))
    print(DIVIDER)

def prompt(msg):
    try:
        return input(msg)
    except (EOFError, KeyboardInterrupt):
        print("\nExiting the program...")
        sys.exit(0)

def handle_sign_up(user_system: UserSystem):
    print_header("Create a New Account")
    username = prompt("New username: ")
    password = prompt("Password: ")
    ok, message = user_system.sign_up(username, password)
    print((">> " if ok else "!! ") + message)
    print()

def handle_login(user_system: UserSystem):
    print_header("Log In")
    username = prompt("Username: ")
    password = prompt("Password: ")
    ok, message, user = user_system.login(username, password)
    print((">> " if ok else "!! ") + message)
    print()
    if ok:
        return user.username
    return None

def print_tutorial():

    print_header("How to Play")
    prompt("Press Enter to go back...")
    
    print()

def show_top_player(user_system: UserSystem):
    top = user_system.top_player()
    if top:
        score  , name = top
        print(f"\nCurrent top player: {name}  (score: {score})")

def show_leaderboard(user_system: UserSystem):
    print_header("Top Players")
    top = user_system.top_players(10)
    if not top:
        print("No player has scored any points yet.")
    else:
        print(f"{'Rank':<6}{'Username':<20}{'Score':<10}")
        for i, (score, name) in enumerate(top, start=1):
            print(f"{i:<6}{name:<20}{score:<10}")
    print()

def user_dashboard(user_system: UserSystem, username):
    while True:
        show_top_player(user_system)
        print_header(f"Player Dashboard: {username}")
        my_score = user_system.get_score(username)
        print(f"Your total score: {my_score}")
        print("1) Start game")
        print("2) Show leaderboard")
        print("3) How to play")
        print("4) Log out")
        choice = prompt("Your choice: ").strip()

        if choice == "1":
            play_game(user_system, username)
        elif choice == "2":
            show_leaderboard(user_system)
        elif choice == "3":
            print_tutorial()
        elif choice == "4":
            print(f"Goodbye, {username}!\n")
            return
        else:
            print(">> Invalid option.\n")

def play_game(user_system: UserSystem, username):
    print("  Coming soon... ")

def main_menu(user_system: UserSystem):
    while True:
        print_header("HoodQuest: The Algorithm Forest")
        print("1) Create a new account")
        print("2) Log in to an existing account")
        print("3) How to play")
        print("4) Exit")
        choice = prompt("Your choice: ").strip()

        if choice == "1":
            username = handle_login(user_system)
            if username:
                user_dashboard(user_system, username)
        elif choice == "2":
            handle_sign_up(user_system)
        elif choice == "3":
            print_tutorial()
        elif choice == "4":
            print("  Goodbye! Don't forget the cookies... ")
            user_system.save()
            sys.exit(0)
        else:
            print(">> Invalid option. Please enter a number between 1 and 4.\n")