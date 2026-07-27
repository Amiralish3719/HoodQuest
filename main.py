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