import sys
from colorama import init, Fore
init()

def error(text):
    msg = [Fore.RED, text, Fore.RESET]
    print(''.join(msg))
    sys.exit(1)