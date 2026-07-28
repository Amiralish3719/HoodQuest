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