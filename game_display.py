import os


def clear_screen():
    # Check if the operating system is Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix/Linux/macOS
    else:
        os.system('clear')


def display_separator(length=30, character="-"):
    print("\n" + character * length)
