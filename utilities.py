import os, msvcrt

# Console colors
class colors:
    reset = '\033[0m'
    bold = '\033[01m'

    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'

# Console utilities
class fancy:
    clear = lambda: os.system('cls')
    dashes = "-" * 30

# Waiting for input
def waitForInput():
    print(colors.bold + colors.lightgrey + "\nPress any button to continue..." + colors.reset, end="", flush=True)
    msvcrt.getch()
    print()